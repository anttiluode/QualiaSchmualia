"""
Pribram's Dream - The Ephaptic Symphony
=======================================
"The brain is a hologram. Memory is interference. Thought is resonance."

This system reads the ephaptic field directly - not spikes, not LFPs,
but the actual geometric orbits that constitute thought.

Input: Any signal (EEG, audio, image, video)
Output: The evolving geometric attractor - the "music of thought"

You don't count spikes. You LISTEN to the field.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from scipy import signal
from scipy.ndimage import gaussian_filter
import threading
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. THE EPHAPTIC FIELD READER - The "Symphony Conductor"
# ============================================================

class EphapticFieldReader:
    """
    Reads the geometric orbits directly from the field.
    No spike counting. No rate coding. Just pure interference patterns.
    
    This is the instrument Pribram wished he had.
    """
    def __init__(self, n_dim=64, delay_steps=3, alpha=0.95):
        self.n_dim = n_dim          # Dimensionality of delay space
        self.delay_steps = delay_steps
        self.alpha = alpha          # Cable attenuation
        
        # The evolving field state
        self.field_state = np.zeros(n_dim)
        self.field_history = []
        
        # Stored attractors (memories)
        self.memory_attractors = []
        self.memory_names = []
        
        # Current reading
        self.current_orbit = None
        self.current_resonance = None
        
    def embed_signal(self, signal_stream):
        """
        Takens embedding of incoming signal.
        This unfolds the 1D time series into an orbit in delay space.
        """
        # Rolling delay embedding
        embedded = np.zeros(self.n_dim)
        for k in range(min(self.n_dim, len(signal_stream))):
            idx = -(k+1) * self.delay_steps
            if abs(idx) <= len(signal_stream):
                embedded[k] = (self.alpha ** k) * signal_stream[idx]
        return embedded
    
    def read_field(self, signal_sample, history_window=100):
        """
        Read the current ephaptic field state.
        One sample at a time - real-time.
        """
        # Maintain rolling history
        if not hasattr(self, 'signal_history'):
            self.signal_history = np.zeros(history_window)
        
        self.signal_history = np.roll(self.signal_history, -1)
        self.signal_history[-1] = signal_sample
        
        # Embed the current history
        self.current_orbit = self.embed_signal(self.signal_history)
        
        # Update field state (field = smoothed orbit)
        self.field_state = 0.97 * self.field_state + 0.03 * self.current_orbit
        
        # Store history
        self.field_history.append(self.field_state.copy())
        if len(self.field_history) > 1000:
            self.field_history.pop(0)
        
        return self.field_state, self.current_orbit
    
    def store_memory(self, orbit, name):
        """Store a geometric attractor as a memory."""
        # Normalize
        memory = orbit / (np.linalg.norm(orbit) + 1e-9)
        self.memory_attractors.append(memory)
        self.memory_names.append(name)
        return len(self.memory_attractors) - 1
    
    def recall(self, orbit):
        """
        Find which stored memory resonates with current orbit.
        This is content-addressable memory - no address, just pattern.
        """
        if not self.memory_attractors:
            return None, 0
        
        orbit_norm = orbit / (np.linalg.norm(orbit) + 1e-9)
        
        best_match = None
        best_resonance = -1
        
        for idx, memory in enumerate(self.memory_attractors):
            # Resonance = cosine similarity in delay space
            resonance = np.abs(np.dot(orbit_norm, memory))
            if resonance > best_resonance:
                best_resonance = resonance
                best_match = idx
        
        return best_match, best_resonance
    
    def compose_attractor(self, memories, weights):
        """
        Create a new attractor by interfering multiple memories.
        This is how thoughts are composed - as interference patterns.
        """
        composite = np.zeros(self.n_dim)
        total_weight = 0
        for mem, w in zip(memories, weights):
            composite += self.memory_attractors[mem] * w
            total_weight += w
        
        if total_weight > 0:
            composite /= total_weight
        
        # Normalize
        composite = composite / (np.linalg.norm(composite) + 1e-9)
        return composite


# ============================================================
# 2. THE HOLOGRAPHIC PROJECTOR - Seeing the Orbits
# ============================================================

class HolographicProjector:
    """
    Visualizes geometric orbits in 3D space.
    What Pribram would have put on his wall.
    """
    def __init__(self, n_points=200):
        self.n_points = n_points
        self.history = []
        
    def project_orbit(self, orbit_state, ax):
        """Project a high-D orbit into 3D for visualization."""
        if len(orbit_state) >= 3:
            # Take first 3 dimensions as projection
            x = orbit_state[0] * 2
            y = orbit_state[1] * 2
            z = orbit_state[2] * 2
            
            # Add to history
            self.history.append([x, y, z])
            if len(self.history) > self.n_points:
                self.history.pop(0)
            
            # Plot trajectory
            hist_array = np.array(self.history)
            if len(hist_array) > 1:
                ax.plot3D(hist_array[:, 0], hist_array[:, 1], hist_array[:, 2], 
                         'c-', alpha=0.5, linewidth=0.5)
            
            # Plot current point
            ax.scatter([x], [y], [z], c='yellow', s=50, alpha=1)
            
            return x, y, z
        return 0, 0, 0


# ============================================================
# 3. THE SYMPHONY ORCHESTRATOR - Converting Orbits to Sound
# ============================================================

class NeuralSymphony:
    """
    Converts geometric orbits into sound.
    Because Pribram was a musician, and he knew thought IS music.
    """
    def __init__(self, sample_rate=8000):
        self.sample_rate = sample_rate
        self.oscillators = []
        self.harmonics = 8
        
    def orbit_to_pitch(self, orbit):
        """Convert orbit geometry to musical pitch."""
        # Energy distribution across dimensions determines pitch
        energy = np.mean(np.abs(orbit))
        # Wrap angle determines note (circle of fifths)
        if len(orbit) >= 2:
            angle = np.arctan2(orbit[1], orbit[0])
        else:
            angle = 0
        
        # Pitch range: 100 Hz to 1000 Hz
        pitch = 100 + energy * 900
        # Angle modulates pitch (vibrato)
        modulation = 0.05 * np.sin(angle * 2)
        
        return pitch * (1 + modulation)
    
    def orbit_to_timbre(self, orbit):
        """Orbit curvature determines harmonic richness."""
        if len(orbit) < 3:
            return [1.0] + [0.5] * (self.harmonics - 1)
        
        # Curvature = second derivative in delay space
        curvature = orbit[2] - 2*orbit[1] + orbit[0]
        curvature = np.abs(curvature)
        
        # Harmonics decay with curvature
        harmonics = [1.0]
        for h in range(1, self.harmonics):
            harmonics.append(np.exp(-curvature * h / 2))
        
        return harmonics
    
    def render_audio_frame(self, orbit, t):
        """Generate audio from current orbit geometry."""
        pitch = self.orbit_to_pitch(orbit)
        harmonics = self.orbit_to_timbre(orbit)
        
        # Synthesize
        sample = 0
        for h, amp in enumerate(harmonics):
            freq = pitch * (h + 1)
            sample += amp * np.sin(2 * np.pi * freq * t)
        
        # Normalize
        return np.tanh(sample / len(harmonics))


# ============================================================
# 4. THE COMPLETE PRIBRAM DREAM MACHINE
# ============================================================

class PribramDreamMachine:
    """
    The complete system:
    - Reads ephaptic field
    - Visualizes geometric orbits in 3D
    - Converts thoughts to sound
    - Stores and recalls memories as attractors
    
    This is what Pribram would have stayed up all night building.
    """
    def __init__(self):
        self.reader = EphapticFieldReader(n_dim=32, delay_steps=2, alpha=0.95)
        self.projector = HolographicProjector(n_points=300)
        self.symphony = NeuralSymphony(sample_rate=8000)
        
        self.running = False
        self.audio_buffer = []
        
        # Pre-store some example attractors
        self._init_example_memories()
        
    def _init_example_memories(self):
        """Create initial geometric attractors (like primitive concepts)."""
        # Create a sine wave attractor
        t = np.linspace(0, 2*np.pi, self.reader.n_dim)
        sine_attractor = np.sin(t * 2)
        self.reader.store_memory(sine_attractor, "sine_wave")
        
        # Create a cosine wave attractor
        cosine_attractor = np.cos(t * 2)
        self.reader.store_memory(cosine_attractor, "cosine_wave")
        
        # Create a harmonic attractor
        harmonic = np.sin(t * 3) + 0.5 * np.sin(t * 6)
        self.reader.store_memory(harmonic, "harmonic")
        
        # Create a noise attractor (chaos)
        np.random.seed(42)
        noise_attractor = np.random.randn(self.reader.n_dim)
        noise_attractor = signal.savgol_filter(noise_attractor, 11, 3)
        self.reader.store_memory(noise_attractor, "noise")
        
    def feed(self, sample):
        """Feed a single sample into the dream machine."""
        field, orbit = self.reader.read_field(sample)
        
        # Check for memory resonance
        match_idx, resonance = self.reader.recall(orbit)
        
        return {
            'field': field,
            'orbit': orbit,
            'resonance': resonance,
            'memory_match': self.reader.memory_names[match_idx] if match_idx is not None else None
        }
    
    def compose_thought(self, memory_indices, weights):
        """Compose a new thought by interfering stored memories."""
        composite = self.reader.compose_attractor(memory_indices, weights)
        return composite


# ============================================================
# 5. THE INTERACTIVE VISUALIZATION
# ============================================================

class PribramDreamUI:
    def __init__(self):
        self.machine = PribramDreamMachine()
        self.is_recording = False
        self.recorded_signal = []
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.patch.set_facecolor('#050510')
        
        # Create layout
        gs = GridSpec(2, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # 3D Orbit visualization
        self.ax_orbit = self.fig.add_subplot(gs[0, :2], projection='3d')
        self.ax_orbit.set_facecolor('#0a0a18')
        self.ax_orbit.set_title('GEOMETRIC ORBIT - The Shape of Thought', 
                               color='#ffcc44', fontsize=12, fontweight='bold')
        self.ax_orbit.set_xlabel('Dimension 1', color='#888')
        self.ax_orbit.set_ylabel('Dimension 2', color='#888')
        self.ax_orbit.set_zlabel('Dimension 3', color='#888')
        
        # Field strength meter
        self.ax_field = self.fig.add_subplot(gs[0, 2])
        self.ax_field.set_title('EPHAPTIC FIELD STRENGTH', color='#ffcc44', fontsize=10)
        self.ax_field.set_xlim(0, 1)
        self.ax_field.set_ylim(0, 1)
        self.field_bar = self.ax_field.barh(0, 0, color='#00ffcc', alpha=0.8)
        self.ax_field.set_facecolor('#0a0a18')
        self.ax_field.set_xticks([])
        self.ax_field.set_yticks([])
        
        # Memory resonance display
        self.ax_memory = self.fig.add_subplot(gs[1, 0])
        self.ax_memory.set_title('MEMORY RESONANCE', color='#ffcc44', fontsize=10)
        self.ax_memory.set_xlim(0, 1)
        self.ax_memory.set_ylim(-0.5, len(self.machine.reader.memory_names) - 0.5)
        self.ax_memory.set_facecolor('#0a0a18')
        self.ax_memory.set_yticks(range(len(self.machine.reader.memory_names)))
        self.ax_memory.set_yticklabels(self.machine.reader.memory_names, color='#aaa')
        self.resonance_bars = self.ax_memory.barh(range(len(self.machine.reader.memory_names)), 
                                                   [0]*len(self.machine.reader.memory_names), 
                                                   color='#ff6644', alpha=0.7)
        
        # Input waveform
        self.ax_waveform = self.fig.add_subplot(gs[1, 1])
        self.ax_waveform.set_title('INPUT WAVEFORM', color='#ffcc44', fontsize=10)
        self.ax_waveform.set_xlim(0, 200)
        self.ax_waveform.set_ylim(-1.5, 1.5)
        self.ax_waveform.set_facecolor('#0a0a18')
        self.waveform_line, = self.ax_waveform.plot([], [], 'c-', alpha=0.7)
        self.waveform_buffer = np.zeros(200)
        
        # Thought composition panel
        self.ax_compose = self.fig.add_subplot(gs[1, 2])
        self.ax_compose.set_title('THOUGHT COMPOSER', color='#ffcc44', fontsize=10)
        self.ax_compose.set_facecolor('#0a0a18')
        self.ax_compose.axis('off')
        
        # Status text
        self.status_text = self.ax_compose.text(0.1, 0.9, 'Ready', transform=self.ax_compose.transAxes,
                                                color='#00ffcc', fontsize=10, fontfamily='monospace')
        
        self.canvas = plt.gcf().canvas
        
        # Start animation
        self.animation = FuncAnimation(self.fig, self.update, interval=50, cache_frame_data=False)
        
    def generate_test_signal(self, t):
        """Generate a test signal that evolves over time."""
        # Sweep frequency from 2Hz to 15Hz
        freq = 2 + 13 * (1 + np.sin(t * 0.5)) / 2
        return 0.8 * np.sin(2 * np.pi * freq * t)
    
    def update(self, frame):
        """Update all displays."""
        t = frame * 0.05
        
        # Generate or use recorded signal
        if self.is_recording:
            # Use recorded signal (from microphone or file)
            if len(self.recorded_signal) > 0:
                idx = frame % len(self.recorded_signal)
                sample = self.recorded_signal[idx]
            else:
                sample = self.generate_test_signal(t)
        else:
            sample = self.generate_test_signal(t)
        
        # Process through dream machine
        result = self.machine.feed(sample)
        
        # Update waveform display
        self.waveform_buffer = np.roll(self.waveform_buffer, -1)
        self.waveform_buffer[-1] = sample
        self.waveform_line.set_data(range(200), self.waveform_buffer)
        
        # Update 3D orbit
        self.ax_orbit.clear()
        self.ax_orbit.set_facecolor('#0a0a18')
        self.ax_orbit.set_title('GEOMETRIC ORBIT - The Shape of Thought', 
                               color='#ffcc44', fontsize=12, fontweight='bold')
        self.ax_orbit.set_xlabel('Dimension 1', color='#888')
        self.ax_orbit.set_ylabel('Dimension 2', color='#888')
        self.ax_orbit.set_zlabel('Dimension 3', color='#888')
        
        # Project orbit into 3D
        orbit = result['orbit']
        if len(orbit) >= 3:
            # Create trajectory
            hist = getattr(self, 'orbit_history', [])
            hist.append([orbit[0], orbit[1], orbit[2]])
            if len(hist) > 100:
                hist.pop(0)
            setattr(self, 'orbit_history', hist)
            
            if len(hist) > 1:
                hist_arr = np.array(hist)
                self.ax_orbit.plot3D(hist_arr[:, 0], hist_arr[:, 1], hist_arr[:, 2], 
                                    'c-', alpha=0.4, linewidth=0.8)
            self.ax_orbit.scatter([orbit[0]], [orbit[1]], [orbit[2]], 
                                 c='yellow', s=80, alpha=1)
        
        # Update field meter
        field_strength = np.linalg.norm(result['field']) / np.sqrt(len(result['field']))
        self.field_bar[0].set_width(field_strength)
        self.ax_field.set_xlim(0, 1)
        
        # Update memory resonance
        for idx, bar in enumerate(self.resonance_bars):
            # Compute resonance with each memory
            _, res = self.machine.reader.recall(orbit)
            bar.set_width(res * 0.8)
            if res > 0.7:
                bar.set_color('#ff4444')
            elif res > 0.4:
                bar.set_color('#ffaa44')
            else:
                bar.set_color('#4466ff')
        
        # Update status
        match_str = result['memory_match'] if result['memory_match'] else 'no match'
        res_str = f"{result['resonance']:.2f}" if result['resonance'] else '0.00'
        self.status_text.set_text(f"Resonance: {res_str}\nMatch: {match_str}\nField: {field_strength:.2f}")
        
        # Auto-refresh
        self.canvas.draw_idle()


# ============================================================
# 6. THE AUDIO OUTPUT (Real-time sound)
# ============================================================

class AudioDreamMachine(PribramDreamMachine):
    """
    Extended version with real-time audio output.
    """
    def __init__(self):
        super().__init__()
        self.audio_time = 0
        self.sample_rate = 44100
        
    def generate_audio_stream(self, duration=5.0):
        """Generate an audio stream from the geometric orbits."""
        n_samples = int(duration * self.sample_rate)
        audio = np.zeros(n_samples)
        
        # Create a thought trajectory
        t_thought = np.linspace(0, 2*np.pi, n_samples)
        
        # Compose a thought by interfering memories
        thought = self.compose_thought([0, 1, 2], [0.6, 0.3, 0.1])
        
        for i in range(n_samples):
            # Modulate with time
            mod = 0.5 + 0.5 * np.sin(t_thought[i] * 2)
            orbit = thought * (0.8 + 0.2 * np.sin(t_thought[i] * 5))
            
            # Convert to sound
            t = i / self.sample_rate
            sample = self.symphony.render_audio_frame(orbit, t)
            audio[i] = sample * mod
        
        return audio


# ============================================================
# 7. MAIN
# ============================================================

def main():
    print("=" * 70)
    print("PRIBRAM'S DREAM - The Ephaptic Symphony")
    print("=" * 70)
    print()
    print("'The brain is a hologram. Memory is interference. Thought is resonance.'")
    print()
    print("Watching the geometric orbits...")
    print("Each point in 3D space is a THOUGHT taking shape.")
    print("The colors show which memories are resonating.")
    print()
    print("Close the window to exit.")
    print("=" * 70)
    
    # Run the visualization
    ui = PribramDreamUI()
    plt.show()
    
    # Optional: Generate and save audio
    # audio_machine = AudioDreamMachine()
    # audio = audio_machine.generate_audio_stream(10.0)
    # from scipy.io import wavfile
    # wavfile.write('pribrams_dream.wav', 44100, (audio * 32767).astype(np.int16))
    # print("Audio saved: pribrams_dream.wav")


if __name__ == "__main__":
    main()