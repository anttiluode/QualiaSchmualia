"""
Neural Reynolds Number Simulator
=================================
Demonstrates the laminar → turbulent transition in the Takens delay manifold.

Core physics:
  Re_n      = sqrt(2 * omega * tau_m)       membrane-level Reynolds number
  Re_delay  = (sigma^2/A^2) * omega*tau*L   delay-manifold Reynolds number
  R_AIS     ≈ 1 / (1 + Re_delay)            AIS resonance (laminar filter output)

At f=8 Hz (theta), tau_m=10 ms  →  Re_n ≈ 1.0  (critical point)
Add noise  →  orbit fills delay space  →  Re_delay rises  →  R_AIS collapses

No audio hardware needed. Pure numpy simulation.
"""

import numpy as np
from scipy import signal as sp_signal
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk


# ═══════════════════════════════════════════════════════════════════
# NOISE GENERATOR  (from slider2.py, adapted for simulation rate)
# ═══════════════════════════════════════════════════════════════════

class NoiseGenerator:
    """Spectral noise types for turbulence injection into the delay manifold."""

    def __init__(self, sample_rate=1000):
        self.sample_rate = sample_rate
        self._brown_state = 0.0

    def generate(self, noise_type, N, amplitude=1.0):
        fn = {
            'white':    self._white,
            'pink':     self._pink,
            'brown':    self._brown,
            'blue':     self._blue,
            'violet':   self._violet,
            'gaussian': self._white,
            'perlin':   self._perlin,
        }.get(noise_type, self._white)
        return fn(N) * amplitude

    def _white(self, N):
        return np.random.normal(0, 1, N)

    def _pink(self, N):
        # FFT method: shape spectrum as 1/sqrt(f)
        f = np.fft.rfftfreq(N)
        f[0] = 1.0
        power = 1.0 / np.sqrt(f)
        power[0] = 0.0
        phases = np.random.uniform(0, 2 * np.pi, len(power))
        spectrum = power * np.exp(1j * phases)
        return np.fft.irfft(spectrum, N)

    def _brown(self, N):
        white = np.random.normal(0, 1, N)
        out = np.zeros(N)
        s = self._brown_state
        for i in range(N):
            s = s * 0.999 + white[i] * 0.1
            out[i] = s
        self._brown_state = s
        # Normalise
        std = out.std() + 1e-9
        return out / std

    def _blue(self, N):
        w = np.random.normal(0, 1, N)
        b, a = sp_signal.butter(1, 0.1, 'high')
        return sp_signal.filtfilt(b, a, w)

    def _violet(self, N):
        w = np.random.normal(0, 1, N)
        b, a = sp_signal.butter(2, 0.1, 'high')
        return sp_signal.filtfilt(b, a, w)

    def _perlin(self, N):
        t = np.arange(N) / self.sample_rate
        out = np.zeros(N)
        for i in range(5):
            f = 2.0 * (2 ** i)
            a = 1.0 / (2 ** i)
            ph = np.random.uniform(0, 2 * np.pi)
            out += a * np.sin(2 * np.pi * f * t + ph)
        return out


# ═══════════════════════════════════════════════════════════════════
# SIGNAL GENERATOR  (pure numpy, no audio)
# ═══════════════════════════════════════════════════════════════════

class SignalGenerator:
    """
    Generates a sinusoid + optional noise.
    sample_rate = 1000 Hz (neural simulation rate, not audio).
    """

    def __init__(self, sample_rate=1000, buffer_size=1000):
        self.sr = sample_rate
        self.N  = buffer_size
        self.phase = 0.0

        # Parameters (set by UI)
        self.base_freq     = 8.0    # Hz — theta by default
        self.amplitude     = 1.0
        self.tau_m_ms      = 10.0   # membrane time constant in ms
        self.noise_enabled = False
        self.noise_type    = 'white'
        self.noise_amp     = 0.3
        self.mix_ratio     = 0.2    # 0 = pure signal, 1 = pure noise

        self._noise_gen = NoiseGenerator(sample_rate)

    def generate(self):
        """Returns (mixed, clean_signal, noise)."""
        N  = self.N
        dt = 1.0 / self.sr
        t  = np.arange(N) * dt
        omega = 2 * np.pi * self.base_freq

        # Clean sinusoid with continuous phase
        clean = self.amplitude * np.sin(omega * t + self.phase)
        self.phase = (self.phase + omega * N * dt) % (2 * np.pi)

        if self.noise_enabled:
            noise = self._noise_gen.generate(self.noise_type, N,
                                             amplitude=self.noise_amp)
            mixed = (1 - self.mix_ratio) * clean + self.mix_ratio * noise
        else:
            noise = np.zeros(N)
            mixed = clean

        return mixed, clean, noise


# ═══════════════════════════════════════════════════════════════════
# DELAY EMBEDDING
# ═══════════════════════════════════════════════════════════════════

def delay_embedding(x, L=40, tau=5, alpha=0.93):
    """
    X_k(t) = alpha^k * x(t - k*tau)
    Returns shape (n_valid, L).
    """
    N = len(x)
    n_valid = N - (L - 1) * tau
    if n_valid <= 0:
        return np.zeros((1, L))
    X = np.zeros((n_valid, L))
    for k in range(L):
        start = (L - 1 - k) * tau
        X[:, k] = (alpha ** k) * x[start:start + n_valid]
    return X


# ═══════════════════════════════════════════════════════════════════
# REYNOLDS NUMBER PHYSICS
# ═══════════════════════════════════════════════════════════════════

def re_n(f_hz, tau_m_ms):
    """
    Membrane-level neural Reynolds number.
    Re_n = sqrt(2 * omega * tau_m)
    Critical at Re_n = 1.0  (f=8 Hz, tau_m=10 ms).
    """
    omega = 2 * np.pi * f_hz
    tau_m = tau_m_ms / 1000.0
    return float(np.sqrt(2.0 * omega * tau_m))


def re_delay(mixed, noise_amp_eff, f_hz, tau_samples, L, sr=1000):
    """
    Delay-manifold Reynolds number.
    Re_delay = (sigma^2 / A^2) * omega * tau_sec * L
    Measures how turbulent the delay-space orbit is.
    """
    A_sq     = np.var(mixed) + 1e-9
    sigma_sq = noise_amp_eff ** 2
    omega    = 2 * np.pi * f_hz
    tau_sec  = tau_samples / sr
    return float((sigma_sq / A_sq) * omega * tau_sec * L)


def ais_resonance(x, f0, L=40, tau=5, alpha=0.93, sr=1000):
    """
    Project delay embedding onto AIS grating tuned to f0.
    R = mean(|X_norm . g|)  — the laminar filter output.
    """
    X = delay_embedding(x, L, tau, alpha)
    if len(X) < 2:
        return 0.0
    k       = np.arange(L)
    tau_sec = tau / sr
    g       = (alpha ** k) * np.sin(2 * np.pi * f0 * k * tau_sec)
    norm_g  = np.linalg.norm(g)
    if norm_g < 1e-9:
        return 0.0
    g /= norm_g
    X_norm = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    return float(np.mean(np.abs(X_norm @ g)))


def regime(re):
    """Returns (label, hex_colour) for the Re_n value."""
    if re < 0.5:
        return "VISCOUS",    "#4488cc"
    elif re < 2.0:
        return "LAMINAR ★",  "#22aa66"
    else:
        return "TURBULENT",  "#cc4444"


# ═══════════════════════════════════════════════════════════════════
# MAIN UI
# ═══════════════════════════════════════════════════════════════════

BG   = '#070710'
BG2  = '#0d0d1a'
TC   = '#666677'
GOLD = '#ffaa33'


class ReynoldsSimulator:
    """
    Tkinter + Matplotlib simulator showing:
      • 3D delay-manifold orbit (the money shot)
      • Signal + noise time series
      • Koopman spectrum (laminar = sharp peak, turbulent = broadband)
      • Re_n gauge (viscous / laminar / turbulent zones)
      • AIS resonance meter
    """

    SAMPLE_RATE  = 1000   # Hz — neural simulation rate
    BUFFER_SIZE  = 1000   # samples = 1 second
    L            = 40     # delay embedding depth
    TAU          = 5      # delay step (samples = ms at 1 kHz)
    ALPHA        = 0.93   # decay factor
    MAX_ORBIT_PTS = 4000  # 3D scatter history

    def __init__(self, root):
        self.root = root
        self.root.title("Neural Reynolds Number Simulator — Delay Manifold Flow")
        self.root.configure(bg=BG2)

        self.gen      = SignalGenerator(self.SAMPLE_RATE, self.BUFFER_SIZE)
        self.running  = False
        self._orbit_buf  = []   # list of (n,3) arrays
        self._re_history = []   # for sparkline

        self._setup_vars()
        self._build_layout()
        # Start immediately
        self.running = True
        self._tick()

    # ──────────────────────────────────────────────
    # Variable setup
    # ──────────────────────────────────────────────
    def _setup_vars(self):
        self.v_freq    = tk.DoubleVar(value=8.0)
        self.v_tau_m   = tk.DoubleVar(value=10.0)
        self.v_noise_on = tk.BooleanVar(value=False)
        self.v_noise_t  = tk.StringVar(value='white')
        self.v_noise_a  = tk.DoubleVar(value=0.3)
        self.v_mix      = tk.DoubleVar(value=0.2)

    # ──────────────────────────────────────────────
    # Layout construction
    # ──────────────────────────────────────────────
    def _build_layout(self):
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)
        self.root.columnconfigure(0, weight=1)

        # ── Plot frame ──
        plot_frame = tk.Frame(self.root, bg=BG)
        plot_frame.grid(row=0, column=0, sticky='nsew')

        self.fig = plt.Figure(figsize=(15, 8), facecolor=BG)
        gs = gridspec.GridSpec(2, 3, figure=self.fig,
                               width_ratios=[2.2, 1.0, 1.0],
                               hspace=0.42, wspace=0.32,
                               left=0.04, right=0.97,
                               top=0.93, bottom=0.07)

        # 3D orbit — spans both rows on the left
        self.ax3d  = self.fig.add_subplot(gs[:, 0], projection='3d')
        # Time series — top middle
        self.ax_ts = self.fig.add_subplot(gs[0, 1])
        # Koopman spectrum — top right
        self.ax_sp = self.fig.add_subplot(gs[0, 2])
        # Re_n gauge — bottom middle
        self.ax_re = self.fig.add_subplot(gs[1, 1])
        # AIS resonance — bottom right
        self.ax_rs = self.fig.add_subplot(gs[1, 2])

        self._init_axes()

        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # ── Control panel ──
        ctrl = tk.Frame(self.root, bg='#0d0d1a', pady=6, padx=8)
        ctrl.grid(row=1, column=0, sticky='ew')

        # Signal params
        sig_box = ttk.LabelFrame(ctrl, text='Signal  (Re_n = √(2ωτ_m))', padding=6)
        sig_box.pack(side='left', padx=8)

        self._make_slider(sig_box, 'f₀ frequency (Hz)', self.v_freq,
                          lo=1, hi=50, fmt='.1f')
        self._make_slider(sig_box, 'τ_m membrane (ms)', self.v_tau_m,
                          lo=1, hi=80, fmt='.0f')

        # Noise / turbulence
        noise_box = ttk.LabelFrame(ctrl, text='Turbulence injection', padding=6)
        noise_box.pack(side='left', padx=8)

        top_row = tk.Frame(noise_box, bg='#0d0d1a')
        top_row.pack(fill='x', pady=2)
        ttk.Checkbutton(top_row, text='Enable noise',
                        variable=self.v_noise_on,
                        command=self._sync).pack(side='left')
        ttk.Label(top_row, text='  type:').pack(side='left')
        cb = ttk.Combobox(top_row, textvariable=self.v_noise_t, width=9, state='readonly',
                          values=['white', 'pink', 'brown', 'blue', 'violet', 'gaussian', 'perlin'])
        cb.pack(side='left', padx=4)
        cb.bind('<<ComboboxSelected>>', lambda _: self._sync())

        self._make_slider(noise_box, 'Noise amplitude  σ', self.v_noise_a,
                          lo=0.0, hi=2.0, fmt='.2f')
        self._make_slider(noise_box, 'Signal/noise mix ratio', self.v_mix,
                          lo=0.0, hi=1.0, fmt='.2f')

        # Live Re_n readout
        info_box = tk.Frame(ctrl, bg='#0d0d1a')
        info_box.pack(side='right', padx=20)

        self.lbl_re = tk.Label(info_box, text='Re_n = —',
                               bg='#0d0d1a', fg='#88ccff',
                               font=('Courier', 13, 'bold'))
        self.lbl_re.pack()
        self.lbl_regime = tk.Label(info_box, text='—',
                                   bg='#0d0d1a', fg='#888888',
                                   font=('Courier', 12))
        self.lbl_regime.pack()

        self.btn = tk.Button(info_box, text='■ Running',
                             bg='#1a5c3a', fg='#aaffcc',
                             font=('Courier', 10, 'bold'),
                             width=12, command=self._toggle)
        self.btn.pack(pady=6)

        # Physics reminder label
        note = tk.Label(info_box,
                        text='Re_n≈1 at θ=8Hz, τ_m=10ms',
                        bg='#0d0d1a', fg='#444466',
                        font=('Courier', 8))
        note.pack()

    def _make_slider(self, parent, label, var, lo, hi, fmt='.2f'):
        row = tk.Frame(parent, bg='#0d0d1a')
        row.pack(fill='x', pady=2)
        tk.Label(row, text=label, width=24, anchor='w',
                 bg='#0d0d1a', fg='#9999bb',
                 font=('Courier', 8)).pack(side='left')
        val_lbl = tk.Label(row, text=format(var.get(), fmt), width=6,
                           bg='#0d0d1a', fg='#44ddaa',
                           font=('Courier', 8, 'bold'))
        val_lbl.pack(side='right')
        def on_move(v):
            val_lbl.config(text=format(float(v), fmt))
            self._sync()
        ttk.Scale(row, from_=lo, to=hi, orient='horizontal',
                  variable=var, command=on_move,
                  length=200).pack(side='left', fill='x', expand=True)

    # ──────────────────────────────────────────────
    # Axis initialisation
    # ──────────────────────────────────────────────
    def _init_axes(self):
        self._style_3d(self.ax3d)
        for ax, title, xl, yl in [
            (self.ax_ts, 'Signal + noise', 'time (ms)', 'amplitude'),
            (self.ax_sp, 'Koopman spectrum', 'Hz', 'power'),
            (self.ax_re, '', '', ''),
            (self.ax_rs, '', '', ''),
        ]:
            self._style_2d(ax, title, xl, yl)

    def _style_3d(self, ax):
        ax.set_facecolor(BG)
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor('#1a1a2a')
        ax.tick_params(colors=TC, labelsize=6)
        for lbl in (ax.xaxis.label, ax.yaxis.label, ax.zaxis.label):
            lbl.set_color(TC)
            lbl.set_fontsize(8)
        ax.set_xlabel('X(t)')
        ax.set_ylabel('X(t−τ)')
        ax.set_zlabel('X(t−2τ)')

    def _style_2d(self, ax, title, xl, yl):
        ax.set_facecolor(BG)
        ax.tick_params(colors=TC, labelsize=7)
        for sp in ax.spines.values():
            sp.set_edgecolor('#222234')
        if title:
            ax.set_title(title, color='#aaaacc', fontsize=9, pad=4)
        if xl:
            ax.set_xlabel(xl, color=TC, fontsize=8)
        if yl:
            ax.set_ylabel(yl, color=TC, fontsize=8)

    # ──────────────────────────────────────────────
    # Controls
    # ──────────────────────────────────────────────
    def _sync(self):
        g = self.gen
        g.base_freq     = self.v_freq.get()
        g.tau_m_ms      = self.v_tau_m.get()
        g.noise_enabled = self.v_noise_on.get()
        g.noise_type    = self.v_noise_t.get()
        g.noise_amp     = self.v_noise_a.get()
        g.mix_ratio     = self.v_mix.get()

    def _toggle(self):
        self.running = not self.running
        if self.running:
            self.btn.config(text='■ Running', bg='#1a5c3a', fg='#aaffcc')
        else:
            self.btn.config(text='▶ Paused', bg='#2a2a44', fg='#8888aa')

    # ──────────────────────────────────────────────
    # Main update loop (every 60 ms via after())
    # ──────────────────────────────────────────────
    def _tick(self):
        if self.running:
            self._sync()
            self._update()
        self.root.after(60, self._tick)

    def _update(self):
        try:
            # ── Generate signal ──
            mixed, clean, noise = self.gen.generate()
            f0     = self.gen.base_freq
            tau_m  = self.gen.tau_m_ms

            # ── Compute Re numbers ──
            Rn     = re_n(f0, tau_m)
            sigma_eff = (self.v_noise_a.get() * self.v_mix.get()
                         if self.v_noise_on.get() else 0.0)
            Rd     = re_delay(mixed, sigma_eff, f0, self.TAU, self.L, self.SAMPLE_RATE)
            R_ais  = ais_resonance(mixed, f0, self.L, self.TAU, self.ALPHA, self.SAMPLE_RATE)

            rg_lbl, rg_col = regime(Rn)
            self._re_history.append(Rn)
            if len(self._re_history) > 120:
                self._re_history.pop(0)

            # Update Tkinter labels
            self.lbl_re.config(text=f'Re_n = {Rn:.3f}')
            self.lbl_regime.config(text=rg_lbl, fg=rg_col)

            # ── Accumulate orbit history ──
            X = delay_embedding(mixed, self.L, self.TAU, self.ALPHA)
            if len(X) > 10:
                step = max(1, len(X) // 600)
                self._orbit_buf.append(X[::step, :3].copy())
                total = sum(len(b) for b in self._orbit_buf)
                while total > self.MAX_ORBIT_PTS and self._orbit_buf:
                    total -= len(self._orbit_buf.pop(0))

            # ── Draw 3D orbit ──
            self.ax3d.clear()
            self._style_3d(self.ax3d)

            if self._orbit_buf:
                pts   = np.vstack(self._orbit_buf)
                c_idx = np.linspace(0, 1, len(pts))
                cmap  = plt.cm.plasma if Rd > 0.8 else plt.cm.winter
                self.ax3d.scatter(pts[:,0], pts[:,1], pts[:,2],
                                  c=c_idx, cmap=cmap, s=2, alpha=0.45)

            title_color = rg_col
            self.ax3d.set_title(
                f'Delay manifold orbit  [{rg_lbl}]\n'
                f'Re_n={Rn:.2f}   Re_delay={Rd:.3f}   R_AIS={R_ais:.3f}',
                color=title_color, fontsize=9, pad=6)
            self.ax3d.set_xlabel('X(t)',     color=TC, fontsize=8)
            self.ax3d.set_ylabel('X(t−τ)',   color=TC, fontsize=8)
            self.ax3d.set_zlabel('X(t−2τ)',  color=TC, fontsize=8)

            # ── Time series ──
            self.ax_ts.clear()
            self._style_2d(self.ax_ts, 'Signal + noise', 'time (ms)', 'amplitude')
            t_ms = np.arange(300)
            self.ax_ts.plot(t_ms, clean[:300],
                            color='#44aaff', lw=1.2, label='clean', alpha=0.9)
            if self.v_noise_on.get():
                self.ax_ts.plot(t_ms, mixed[:300],
                                color='#ff6644', lw=0.8, label='mixed', alpha=0.7)
            self.ax_ts.legend(fontsize=7, facecolor='#111',
                              edgecolor='none', labelcolor='#ccc', loc='upper right')
            self.ax_ts.set_xlim(0, 300)

            # ── Koopman spectrum ──
            self.ax_sp.clear()
            self._style_2d(self.ax_sp, 'Koopman spectrum', 'Hz', 'power (norm)')
            freqs = np.fft.rfftfreq(len(mixed), d=1.0 / self.SAMPLE_RATE)
            psd   = np.abs(np.fft.rfft(mixed)) ** 2
            psd   = psd / (psd.max() + 1e-9)
            mask  = freqs < 80
            # Color: sharp peak → laminar (green);  broadband → turbulent (red)
            sp_col = '#22aa66' if Rd < 0.5 else ('#ff8833' if Rd < 1.5 else '#cc4444')
            self.ax_sp.fill_between(freqs[mask], psd[mask], color=sp_col, alpha=0.4)
            self.ax_sp.plot(freqs[mask], psd[mask], color=sp_col, lw=1.0)
            self.ax_sp.axvline(f0, color=GOLD, lw=1.5, ls='--', alpha=0.8)
            self.ax_sp.text(f0 * 1.05, 0.88, f'f₀\n{f0:.1f}Hz',
                            color=GOLD, fontsize=7)
            # Label discrete vs continuous spectrum
            sp_state = 'discrete eigenvalue' if Rd < 0.5 else 'continuous spectrum'
            self.ax_sp.text(0.97, 0.94, sp_state, transform=self.ax_sp.transAxes,
                            ha='right', color=sp_col, fontsize=7)
            self.ax_sp.set_ylim(0, 1.1)

            # ── Re_n gauge ──
            self._draw_re_gauge(self.ax_re, Rn, rg_lbl, rg_col)

            # ── AIS resonance meter ──
            self._draw_resonance_meter(self.ax_rs, R_ais, Rd, rg_col)

            self.fig.canvas.draw_idle()

        except Exception as exc:
            import traceback
            print(f"[update error] {exc}")
            traceback.print_exc()

    # ──────────────────────────────────────────────
    # Gauge / meter rendering helpers
    # ──────────────────────────────────────────────
    def _draw_re_gauge(self, ax, Rn, rg_lbl, rg_col):
        ax.clear()
        ax.set_facecolor(BG)
        ax.set_xlim(0, 4.0)
        ax.set_ylim(-0.8, 1.8)
        ax.axis('off')

        # Three background zones
        ax.barh(0, 0.5,  left=0.0,  height=0.5, color='#1a3a55', alpha=0.7)
        ax.barh(0, 1.5,  left=0.5,  height=0.5, color='#1a3a25', alpha=0.7)
        ax.barh(0, 2.0,  left=2.0,  height=0.5, color='#3a1a1a', alpha=0.7)

        # Filled bar to current Re_n
        Rn_c = min(Rn, 3.95)
        ax.barh(0, Rn_c, left=0.0,  height=0.45, color=rg_col, alpha=0.92)

        # Critical point tick
        ax.axvline(1.0, ymin=0.25, ymax=0.75,
                   color='#ffff44', lw=1.5, ls='--', alpha=0.85)
        ax.text(1.0, 0.75, 'Re=1\ncritical', ha='center',
                color='#ffff44', fontsize=7)

        # Zone labels
        ax.text(0.25, -0.3, 'viscous',   ha='center', color='#4488cc', fontsize=7)
        ax.text(1.25, -0.3, 'laminar ★', ha='center', color='#22aa66', fontsize=7)
        ax.text(3.0,  -0.3, 'turbulent', ha='center', color='#cc4444', fontsize=7)

        # Numeric readout
        ax.text(2.0, 1.45,
                f'Re_n = {Rn:.3f}  [{rg_lbl}]',
                ha='center', color=rg_col,
                fontsize=10, fontweight='bold', fontfamily='monospace')
        ax.text(2.0, 1.05,
                f'= √(2·ω·τ_m)   τ_m={self.v_tau_m.get():.0f}ms  f₀={self.v_freq.get():.1f}Hz',
                ha='center', color='#666688', fontsize=7, fontfamily='monospace')

    def _draw_resonance_meter(self, ax, R_ais, Rd, rg_col):
        ax.clear()
        ax.set_facecolor(BG)
        ax.set_xlim(0, 1.0)
        ax.set_ylim(-0.8, 1.8)
        ax.axis('off')

        # Background track
        ax.barh(0, 1.0, height=0.5, color='#1a1a2a', alpha=0.8)

        # Filled bar
        res_col = '#22aa66' if R_ais > 0.35 else ('#ff8833' if R_ais > 0.2 else '#cc4444')
        ax.barh(0, R_ais, height=0.45, color=res_col, alpha=0.92)

        # Theory expectation: 1/(1+Re_delay)
        R_theory = 1.0 / (1.0 + Rd)
        ax.axvline(R_theory, ymin=0.1, ymax=0.9,
                   color='#ffaa33', lw=1.5, ls=':', alpha=0.8)
        ax.text(R_theory, 0.75, f'{R_theory:.2f}\n(theory)', ha='center',
                color='#ffaa33', fontsize=6)

        # Labels
        ax.text(0.5, 1.45, f'AIS resonance  R = {R_ais:.3f}',
                ha='center', color=res_col,
                fontsize=10, fontweight='bold', fontfamily='monospace')
        ax.text(0.5, 1.05,
                f'≈ 1/(1+Re_delay)   Re_delay={Rd:.3f}',
                ha='center', color='#666688', fontsize=7, fontfamily='monospace')

        ax.text(0.05, -0.3, 'no reconstruction', color='#cc4444', fontsize=7)
        ax.text(0.65, -0.3, 'clean hologram',    color='#22aa66', fontsize=7)


# ═══════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    root.geometry("1440x920")
    root.minsize(1100, 720)
    app = ReynoldsSimulator(root)
    root.protocol("WM_DELETE_WINDOW",
                  lambda: (root.quit(), root.destroy()))
    root.mainloop()


if __name__ == '__main__':
    main()