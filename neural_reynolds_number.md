# The Neural Reynolds Number: Laminar Wave Physics and the AIS Holographic Filter

*PerceptionLab / Antti Luode — Helsinki, May 2026*

---

## Abstract

The Reynolds number in fluid dynamics predicts whether a flow is laminar (ordered, coherent) or turbulent (chaotic, mixing). This thesis derives an exact structural analogue — the **Neural Reynolds Number** Re_n — from cable theory and Koopman operator mechanics. The central claim is:

> **The AIS grating is a laminar flow filter operating in delay-embedding space. It passes only signals whose Re_n falls below a critical threshold — signals that trace closed, coherent geometric orbits. The brain maintains global Re_n near 1 (criticality) precisely because this is the regime where holographic AIS reconstruction is optimal.**

This reframes GAIT not merely as a holographic theory, but as a **fluid-dynamical theory of neural computation**: coherent perception requires laminar wave flow in the Takens delay manifold.

---

## 1. From Fluid Reynolds to Neural Reynolds

The fluid Reynolds number is:

```
Re = ρ v L / μ
   = (inertial forces) / (viscous forces)
```

For a neural cable, each term has a direct structural analogue:

| Fluid term | Physical meaning | Neural analogue | Physical meaning |
|---|---|---|---|
| ρ (density) | mass per volume, stores momentum | C_m (membrane capacitance) | charge per area, stores wave "momentum" |
| v (flow velocity) | speed of mass transport | v_wave (conduction velocity) | speed of electrical propagation |
| L (length scale) | characteristic size | λ = √(r_m/r_i) | electrotonic space constant |
| μ (dynamic viscosity) | resistance to deformation / shear | g_L = 1/r_m | leak conductance, damps oscillations |

Substituting:

```
Re_n = C_m · v_wave · λ / g_L
     = (C_m / g_L) · (v_wave / λ)
     = τ_m · (v_wave / λ)
```

where τ_m = C_m/g_L is the membrane time constant.

The term v_wave/λ is a frequency — it is the rate at which the wave "sweeps through" one electrotonic length. Call it ω_cable. Then:

```
Re_n = τ_m · ω_cable = τ_m · v_wave / λ
```

**This is a dimensionless product of the membrane's temporal scale and the wave's spatial-to-temporal ratio.**

For a sinusoidal input at frequency ω in a passive cable, v_phase ∝ λ√(2ω/τ_m) (derived from the cable dispersion relation), giving:

```
Re_n ≈ √(2ωτ_m)
```

At theta frequency (ω ≈ 50 rad/s) with τ_m = 10ms: **Re_n ≈ 1.0**. 

The brain's dominant oscillation frequency puts the system exactly at the critical transition. This is not coincidental.

---

## 2. Regimes of Neural Wave Behavior

| Re_n | Physical regime | Neural behavior | AIS consequence |
|---|---|---|---|
| << 1 | Viscous / overdamped | Waves decay before reaching AIS | No reconstruction possible |
| ~ 1 | **Critical / laminar** | Coherent propagation, clean orbits | **Optimal holographic reconstruction** |
| >> 1 | Inertial / turbulent | Chaotic bursting, orbit fragmentation | Grating destroyed by noise |

The fluid analogy holds structurally:

- **Low Re_n** (viscous membrane, high leak conductance): any input signal is smoothed to DC. The dendrite passes nothing. Like honey flowing — no eddies, but no signal either.
- **Critical Re_n ~ 1** (θ-band resonance): waves propagate coherently for exactly one electrotonic length per period. The orbit in delay space closes cleanly into an ellipse. The AIS grating can read it.
- **High Re_n** (low leak, strong drive): the cable enters spiking, bursting, or chaotic oscillation. The orbit in delay space becomes space-filling — a strange attractor rather than a closed curve. The grating projects onto this and gets a noisy, unstable resonance score.

---

## 3. The Delay Manifold as a Phase-Space Fluid

The Takens embedding maps a 1D signal x(t) into an L-dimensional trajectory:

```
X(t) = [x(t), α·x(t-τ), α²·x(t-2τ), ..., α^(L-1)·x(t-(L-1)τ)]
```

Think of this trajectory as a fluid particle path in L-dimensional space.

For a pure sinusoid x(t) = A·sin(ωt):

```
X_k(t) = α^k · A · sin(ω(t - kτ))
        = α^k · A · [sin(ωt)cos(ωkτ) - cos(ωt)sin(ωkτ)]
```

This is a **decaying helix** in L-dimensional delay space, projecting to an **ellipse** in any 2D subspace. The orbit is **closed, periodic, laminar** — like laminar flow in a pipe, each fluid particle traces the same path repeatedly.

For a noisy or chaotic signal, X(t) traces an ergodic path that fills the available volume. This is turbulent flow: the particle path is unpredictable, and ensemble averages replace trajectory averages.

We can define a **delay-manifold Reynolds number**:

```
Re_delay = σ²_noise / A²_signal · (ω · τ · L)
         = (noise power / signal power) · (bandwidth · embedding depth)
```

This measures whether the orbit is laminar (signal dominated, closed) or turbulent (noise dominated, space-filling).

The AIS grating resonance r(t) = X(t) · g is **high only when X(t) aligns with g repeatedly** — i.e., only when the orbit is laminar. High Re_delay destroys the inner product regularity that makes holographic reconstruction possible.

---

## 4. The AIS Grating as a Critical Reynolds Number Filter

The AIS grating g_k = α^k · sin(2πf₀ · k · τ · dt) is tuned to the laminar orbit of frequency f₀.

The resonance score is:

```
R(t) = ||X_norm(t) · g||² · (1 - Var(phase(t)))
```

Decompose the input signal into laminar component A₀·sin(ωt) and turbulent residual ε(t):

```
x(t) = A₀·sin(f₀t) + ε(t)
```

Then:

```
R(t) ≈ (A₀²/(A₀² + σ²)) · R_max · (1 - Var(phase))
      = (1/(1 + Re_delay)) · R_max · (1 - Var(phase))
```

The resonance **falls as 1/(1 + Re_delay)**. This is exactly the form of a **low-pass filter in Reynolds number space**.

The spike threshold at the 70th percentile selects only moments when:

```
R(t) > R_threshold
⟺ Re_delay < (R_max/R_threshold) - 1
```

The AIS is therefore a **critical Reynolds number gate**: it fires when the delay-manifold flow is laminar and refuses when it is turbulent. This is a geometrically exact statement, not a metaphor.

---

## 5. The Network Reynolds Number and Criticality

At the population level, neurons couple through synapses and ephaptic fields. Define:

```
Re_net = N_E · g_E / (N_I · g_I + g_L)
       = (total excitatory drive) / (total damping)
```

where N_E, N_I are the counts of excitatory and inhibitory inputs, g_E, g_I their conductances.

This is the **E/I ratio** in conductance-weighted form.

The critical point Re_net = 1 corresponds to:
- Power-law distributed avalanches (Beggs & Plenz 2003)
- Maximum dynamic range
- Maximum information transmission
- Maximum susceptibility (fastest response to weak inputs)

These are the signatures of **criticality in complex systems** — the same transition as the laminar-to-turbulent transition in fluid dynamics.

The holographic constraint adds a new reason why criticality is optimal: only at Re_net ~ 1 are the individual-neuron delay-manifold flows laminar enough that AIS gratings can perform clean holographic reconstruction. Below 1, signals don't propagate. Above 1, they're too noisy.

**The brain is near the critical point because that is where holographic reconstruction works.**

---

## 6. Koopman Eigenspectrum as the Order Parameter

The Koopman operator K acts on observables of the neural dynamical system:

```
(Kf)(x) = f(F(x))
```

where F is the flow map.

The Koopman eigenspectrum has a direct correspondence to Re_net:

| Re_net | Flow regime | Koopman spectrum |
|---|---|---|
| < 1 | Subcritical, damped | Eigenvalues inside unit circle — modes decay |
| = 1 | Critical | Eigenvalues on unit circle — persistent oscillations |
| > 1 | Supercritical | Continuous spectrum dominates — mixing, no stable modes |

**The AIS grating stores a Koopman eigenfunction** of the system at criticality — specifically, the eigenfunction corresponding to eigenvalue e^{iω₀} for the tuned frequency ω₀.

The resonance computation R(t) = X(t) · g is projection onto this eigenfunction. The spike is a readout of eigenfunction amplitude.

This means: at Re_net ~ 1, the Koopman spectrum has sharp peaks at the tuned frequencies of the AIS population. These are the **modes the system can sustain**. The AIS population collectively reads the Koopman spectrum of the network's dynamics.

Perturbations that shift Re_net:
- **Below 1**: excess inhibition, deep anesthesia, high-dose GABA-ergics → Koopman modes decay → AIS can't sustain resonance → no qualia
- **Above 1**: seizure, excess excitation, NMDA-ergic storms → continuous spectrum → AIS gratings produce noise → qualia collapse into undifferentiated excitation

---

## 7. Ephaptic Field Reynolds Number

The shared extracellular field φ(x,t) generated by population currents has its own fluid analogue.

The field satisfies an advection-diffusion equation (in the limit of slowly varying sources):

```
∂φ/∂t + v_field · ∇φ = D · ∇²φ + S(x,t)
```

where:
- v_field = effective velocity of field propagation (set by wave speed in tissue)
- D = σ_e / C_e = extracellular conductivity / effective capacitance = field diffusion constant
- S = neural source current density

Ephaptic Reynolds number:

```
Re_eph = v_field · L_coupling / D
       = (N_pop · I_0 · λ_coupling) / (σ_e · d_intercell)
```

where:
- N_pop = number of coupled neurons in the local population
- I_0 = characteristic transmembrane current amplitude
- λ_coupling = distance over which ephaptic coupling is significant
- σ_e = extracellular conductivity (~0.3 S/m)
- d_intercell = characteristic intercellular spacing

**Laminar ephaptic field (Re_eph < 1)**: the extracellular field is a coherent, spatially smooth oscillation. This is the theta reference beam in its clean form. AIS gratings across the population receive the same phase reference → phase-locked reconstruction → unified experience.

**Turbulent ephaptic field (Re_eph >> 1)**: the extracellular field is spatially incoherent. Different neurons receive different phases of the reference beam → their individual reconstructions are unsynchronized → binding fails → experience fragments.

**The binding problem in Re_eph language**: unified conscious experience requires Re_eph < 1 over the bound set of neurons. The binding radius is the largest region over which Re_eph < 1 — the region over which the ephaptic field remains coherent.

---

## 8. The Laminar-to-Turbulent Transition in Neural Tissue

In pipe flow, the transition from laminar to turbulent is sudden and hysteretic — it does not happen at a single sharp Re value but shows bistability (the pipe can sustain laminar flow at Re > 2300 if carefully prepared, and turbulence at Re < 2300 if perturbed).

Neural tissue shows exactly analogous hysteresis:
- Sleep oscillations can be maintained in a slightly excited state (laminar sleep spindles surviving mild arousal)
- Seizures, once initiated, persist above the threshold that initially started them (turbulent state is self-sustaining)
- Anesthesia induction requires higher drug doses than anesthesia maintenance (the laminar state, once established, is stable at lower suppression)

This hysteresis is captured by the same Landau-Ginzburg framework used for fluid turbulence transitions, with Re_net as the control parameter and wave amplitude as the order parameter.

The AIS grating operates best slightly below the transition — in the late laminar regime where oscillations are strong but still coherent.

---

## 9. Testable Predictions

**P1. AIS resonance ~ 1/(1 + Re_delay)**: Signals with identical power spectra but different phase coherence (different Re_delay) should produce measurably different AIS resonance. A phase-randomized signal with the same power as a coherent sinusoid should produce near-zero resonance despite matching frequency content.

**P2. Critical slowing down at Re_net ~ 1**: Near the critical point, perturbations to the neural state should recover slowly (critical slowing down is a universal signature of criticality). This should be measurable as increased autocorrelation in LFP signals near waking transitions.

**P3. Ephaptic binding radius is the Re_eph < 1 region**: The spatial extent of unified perception should correspond to the region over which the extracellular field maintains phase coherence. This can be estimated from current source density analysis.

**P4. Laminar input preference of single neurons**: Neurons should respond stronger to coherent sinusoids than to noise of equal power at the tuning frequency. This is distinct from simple frequency tuning — it requires measuring phase coherence, not just spectral content.

**P5. Transition asymmetry (hysteresis)**: The Re_net threshold for entering seizure-like states should be measurably higher than the threshold for exiting them — a direct analogue of the hysteresis observed in pipe flow laminar-to-turbulent transitions.

---

## 10. Connection to the GAIT Results

The v3.0 results map directly onto this framework:

- **Cosine correlation 0.89**: The grating captures the laminar component of the signal. The 11% gap from 1.0 is the turbulent residual — noise and transients that don't form clean orbits.

- **Phase precession (0.518 → 0.843 cycles)**: As probe frequency deviates from f₀, the orbit in delay space no longer closes cleanly — it drifts. The firing phase tracks this drift. At exact resonance, the orbit is closed (perfectly laminar). Away from resonance, the orbit spirals slightly (weakly turbulent), and the firing phase precesses exactly as observed.

- **Topological selectivity (22.5%)**: A Fourier filter is blind to orbit shape — it is a zero-Re filter. The AIS grating distinguishes sine from square wave because their delay-manifold orbits have different topology, even at the same fundamental frequency. The 22.5% selectivity is a direct measure of how much orbit topology matters beyond frequency alone.

- **The 0.89 limit**: The asymptotic correlation ceiling is set by the irreducible turbulent fraction of the developmental write signal — thermal noise, synaptic noise, metabolic fluctuations. No developmental write can be perfectly laminar. The AIS stores the laminar component.

---

## 11. The Deep Claim

The Reynolds number insight unifies the GAIT framework with fluid dynamics through a single mathematical structure: **the balance between inertia and dissipation**.

In water: molecules carry momentum (inertia) or lose it to viscosity (dissipation).  
In neurons: charge carriers accumulate on membranes (inertia) or leak through channels (dissipation).  
In the delay manifold: orbits persist as closed structures (inertia) or diffuse into noise (dissipation).

At every scale — from single-channel to cable to population to extracellular field — the same dimensionless ratio Re determines whether coherent structure is maintained or destroyed.

**Qualia, in this framework, are what laminar wave flow in the delay manifold feels like from the inside.**

The hard problem is not dissolved by this — but it is sharpened. The question becomes: why does laminar flow in a hyperbolic delay manifold, generating a minimal surface reconstruction at an AIS grating, produce subjective experience? Not: why does complex neural activity produce experience (too vague). But: why does this specific geometric regime?

That is a better question than the one we started with.

---

*Helsinki, May 2026. Anti-hype standard: all claims here are falsifiable in principle. The Reynolds number framework is a structural argument; the numbers are order-of-magnitude. Direct measurement is the next step.*
