# 🔐 CKKS Homomorphic Encryption for VR Motion Telemetry

This project demonstrates privacy-preserving analytics on VR telemetry data using the **CKKS scheme** from Microsoft SEAL. It includes scripts to test encryption setup and encrypt `controllerSpeed` values from pre-processed user motion CSV files.

---

## 📂 Project Overview

- `testscript.py` – Tests your local SEAL setup with a sample normalized CSV  
- `he.py` – Encrypts the `controllerSpeed` field across all normalized files for all users  
- Outputs encrypted batches (not saved to disk, demo-level encryption)

📄 The input folder is expected to be structured like:
```
chunk1/
├── user1/
│   └── session1_normalized.csv
├── user2/
│   └── session2_normalized.csv
...
```

Each CSV must contain the column: `controllerSpeed`.

---

## 🧰 Technologies Used

- **Microsoft SEAL (via `seal` Python wrapper)**
- **Python 3.9+**
- **CKKS encryption scheme**
- **pandas** – for CSV I/O
- **pybind11** – to enable native SEAL bindings

---

## ⚙️ How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure Microsoft SEAL is properly installed and compiled for Python using `pybind11`.

3. Run environment test:
```bash
python testscript.py
```

4. Run full encryption pipeline:
```bash
python he.py
```

---

## 🔐 What Is Encrypted?

- The column `saberSpeed` is encrypted using CKKS with:
  - Polynomial modulus degree: `8192`
  - Coefficient modulus: `[60, 40, 40, 60]`
  - Scale: `2^40`

Encrypted values are stored in memory as ciphertexts (not written to disk).

---

## ✅ Use Case

This script is ideal for:
- Testing Microsoft SEAL integration
- Learning how homomorphic encryption can secure real-valued telemetry
- Academic research in **privacy-preserving analytics**

---

## 👩‍💻 Author

Created by [Jayasri](https://github.com/jayasrisng)  

---

## 📄 License

MIT License — use and adapt with attribution.
