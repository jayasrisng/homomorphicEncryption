# Homomorphic Encryption for VR Motion Telemetry

This repository demonstrates a small CKKS homomorphic-encryption pipeline for privacy-preserving analytics over VR motion telemetry.

The current scripts focus on one real-valued telemetry feature, `controllerSpeed`, from normalized user-motion CSV files. The goal is to test whether a telemetry field can be encrypted and prepared for privacy-preserving aggregate computation without exposing raw motion values during the analytics step.

## Why this exists

XR systems can produce sensitive behavioral traces: controller speed, hand motion, timing, reach patterns, and repeated interaction behavior. Even simple telemetry can become identifying when collected at scale.

This project explores a narrow research question:

> Can real-valued VR telemetry be prepared for encrypted analytics using CKKS-style approximate homomorphic encryption?

## Project overview

```text
testscript.py   Local SEAL/Python wrapper smoke test using a sample normalized CSV
he.py           Encrypts controllerSpeed values across normalized user/session files
requirements.txt
```

Expected input layout:

```text
chunk1/
├── user1/
│   └── session1_normalized.csv
├── user2/
│   └── session2_normalized.csv
└── ...
```

Each CSV is expected to contain:

```text
controllerSpeed
```

## What is encrypted

The `controllerSpeed` column is encrypted with CKKS parameters suitable for demo-scale approximate arithmetic:

- Polynomial modulus degree: `8192`
- Coefficient modulus bits: `[60, 40, 40, 60]`
- Scale: `2^40`

Encrypted values are kept in memory as ciphertext objects. The current demo does not persist ciphertext batches to disk.

## Tech stack

- Python 3.9+
- Microsoft SEAL via Python bindings / wrapper
- CKKS approximate homomorphic encryption
- pandas for CSV loading
- pybind11 for native binding support

## How to run

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Ensure Microsoft SEAL and its Python bindings are installed and available in the active environment.

Run a local setup smoke test:

```bash
python testscript.py
```

Run the encryption pipeline:

```bash
python he.py
```

## Case study

See [docs/case-study.md](docs/case-study.md) for the research context, implementation decisions, and current limitations.

## Current limitations

- This is a research prototype, not a production privacy system.
- The pipeline currently focuses on one real-valued feature.
- Ciphertexts are not persisted or passed into a complete encrypted aggregation service.
- CKKS introduces approximate numerical behavior; results require careful interpretation.
- Production use would require security review, parameter validation, key management, and threat modeling.

## Future work

- Add a small synthetic sample dataset so the pipeline can be tested without private telemetry.
- Add encrypted aggregate examples such as mean controller speed.
- Persist ciphertext outputs in a documented format.
- Add a diagram connecting this repository to the broader VR telemetry privacy workflow.
- Add unit tests around CSV validation and parameter setup.

## License

MIT License — use and adapt with attribution.
