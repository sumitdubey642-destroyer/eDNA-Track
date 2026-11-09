"""
eDNA Track - eDNA Mitochondrial COI k-mer Classifier Training Pipeline
-----------------------------------------------------------------------
Converts raw nucleotide sequences (A, T, C, G) into 64-dimensional 3-mer
codon frequency vectors and trains a RandomForestClassifier to identify
endangered and invasive species from noisy environmental DNA reads.
"""

import itertools
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Reference COI Barcodes
SPECIES_DB = {
    "Hypophthalmichthys_molitrix": "ATGCGTTACGGACTATTCGGACCTAAGTGCCATGGACTTGACCGATTCGATCGATCGCTAGCTA",
    "Batrachochytrium_dendrobatidis": "TTGCATGCTAGCTAGCTGATCGATCGATCGATGCTAGCTAGCATCGATCGATCGATGCTAGCTA",
    "Panthera_uncia": "GGCCTTAAGGCCTTAAGGCCTTAAGGCCTTAAGGCCTTAAGGCCTTAAGGCCTTAAGGCCTTAA",
    "Platanista_gangetica": "CGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTA"
}

ALL_3MERS = [''.join(p) for p in itertools.product('ATCG', repeat=3)]


def sequence_to_kmer_vector(seq: str) -> list:
    counts = {kmer: 0 for kmer in ALL_3MERS}
    for i in range(len(seq) - 2):
        kmer = seq[i:i+3]
        if kmer in counts:
            counts[kmer] += 1
    total = max(1, len(seq) - 2)
    return [round(counts[k] / total, 4) for k in ALL_3MERS]


def mutate_sequence(seq: str, mutation_rate: float = 0.08) -> str:
    bases = ['A', 'T', 'C', 'G']
    seq_list = list(seq)
    for i in range(len(seq_list)):
        if np.random.rand() < mutation_rate:
            seq_list[i] = np.random.choice(bases)
    return ''.join(seq_list)


def main():
    print("[1/3] Synthesizing 2,000 noisy field eDNA reads with PCR/strip mutation noise...")
    np.random.seed(42)
    X, y = [], []

    for label, barcode in SPECIES_DB.items():
        for _ in range(500):
            noisy_read = mutate_sequence(barcode, mutation_rate=0.10)
            X.append(sequence_to_kmer_vector(noisy_read))
            y.append(label)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("[2/3] Training 3-mer Oligonucleotide RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=150, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"      -> Test Set Classification Accuracy: {acc * 100:.2f}%")

    print("[3/3] Exporting trained bioinformatics metadata to 'edna_model_metadata.json'...")
    output = {
        "model": "RandomForest-3mer-eDNA-Classifier",
        "accuracy_pct": round(acc * 100, 2),
        "kmer_features": len(ALL_3MERS),
        "classes": list(SPECIES_DB.keys())
    }
    with open("edna_model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("✅ SUCCESS! Saved 'edna_model_metadata.json'")


if __name__ == "__main__":
    main()