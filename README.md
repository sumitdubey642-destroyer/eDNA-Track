# 🧬 eDNA Track: Decentralized eDNA & Zero-Knowledge Biodiversity Network

eDNA Track turns standard smartphones into cryptographically verified **environmental DNA (eDNA)** field sensors. By combining WebRTC optical strip scanning, **SHA-256 Zero-Knowledge Telemetry Attestation**, and **k-mer Neural Sequence Alignment**, it detects invasive pathogens and endangered species in seconds without centralized lab delays.

## 🔬 Core Technical Pillars
1. **Optical WebRTC Biosensor:** Captures real-time RGB fluorometric band ratios from lateral-flow eDNA strips and decodes 64-bp Mitochondrial COI sequences.
2. **Cryptographic Anti-Spoofing (SHA-256 ZKP):** Locks GPS coordinates, UTC timestamps, and nucleotide reads into an immutable hash—preventing falsified ecological reports.
3. **Hybrid AI Alignment:** Combines Python Scikit-Learn 3-mer oligonucleotide classification (`train_edna_classifier.py`) with in-browser Smith-Waterman edit-distance alignment.