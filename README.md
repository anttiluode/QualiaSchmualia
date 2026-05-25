# QualiaSchmualia

**Live Interactive Engine:** [https://anttiluode.github.io/QualiaSchmualia/](https://anttiluode.github.io/QualiaSchmualia/)

## The Brain as a Holographic Wave Computer

This repository explores the physical and mathematical foundations of perception and memory. The core insight driving this project is that **frequency is not a number; it is a GEOMETRIC ORBIT in delay space**. 

Rather than acting as digital switches, neurons operate as a network of adaptive lenses. They focus specific wave patterns via their Axon Initial Segment (AIS) gratings. Time windows set "fluid vector" addresses in delay space, where the address *is* the memory, the read *is* the computation, and the write *is* the learning. 

### The Physical Framework
This work identifies the specific biological mechanisms required to validate Pribram's holographic memory theory:
* **The Substrate (Holographic Plate):** The 190nm periodic actin rings of the AIS.
* **The Write Mechanism:** Moiré interference between Takens-embedded dendritic input and the theta reference clock.
* **The Read Mechanism:** Cosine similarity within delay space (phase-invariant resonance).
* **Communication:** The ephaptic field naturally broadcasts the collective address space to phase-lock distributed gratings.

### Mathematical Proof (`ais_holographic_proof3.py`)

[pic](geometric_orbit_proof_v3.png)

The `ais_holographic_proof3.py` script computationally validates this framework, demonstrating that the AIS stores attractors rather than acting as a simple Fourier filter. 
* **Quadrature Grating Correlation:** The cosine grating achieves a 0.8898 correlation with theoretical predictions, proving the mechanism captures full phase information.
* **Topological Selectivity:** The system demonstrates 22.5% selectivity to waveform shape (easily distinguishing matched sines from square waves of the same fundamental frequency), confirming it detects geometric orbits.
* **Continuous Phase Precession:** Firing phase systematically precesses through the theta cycle (ranging from 0.518 to 0.843 cycles) as probe frequencies change, emerging entirely naturally from geometric orbit matching.

### Holographic Qualia Engine (`index.html`)
A real-time WebGL simulation that physically maps these computational concepts into an interactive visualizer:
* **Object Beam (Sensory Input):** Live webcam feed convolved with delay embedding.
* **Reference Beam (Clock):** Theta/Gamma global oscillation.
* **Holographic Plate:** The simulated AIS grating scaffold.
* **Qualia:** The reconstructed wavefront emerging as vibrant Moiré interference.

## License
This project is licensed under the MIT License - Copyright (c) 2026 anttiluode.
