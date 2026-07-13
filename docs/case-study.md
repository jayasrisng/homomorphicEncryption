# Homomorphic Encryption Telemetry Case Study

## Summary

This project demonstrates a CKKS-based encryption pipeline for VR motion telemetry. It focuses on encrypting a real-valued controller-speed feature from normalized session CSV files so privacy-preserving analytics can be explored without exposing raw motion values during computation.

## Problem

VR telemetry can expose more than product usage. Motion traces can reveal behavior, ability, identity patterns, fatigue, and interaction style. Analytics over this data need stronger privacy boundaries than ordinary logging.

The project asks:

> Can a real-valued VR motion feature be encrypted in a form suitable for approximate encrypted analytics?

## Approach

The prototype uses Microsoft SEAL-style CKKS encryption because controller speed is a real-valued signal and CKKS supports approximate arithmetic over encrypted real numbers.

The current workflow is:

1. Load normalized session CSV files from a user/session folder structure.
2. Validate the expected telemetry column, `controllerSpeed`.
3. Configure CKKS encryption parameters.
4. Encode and encrypt controller-speed values.
5. Keep ciphertexts in memory for demo-scale experimentation.

## Technical choices

### CKKS for real-valued telemetry

Controller speed is continuous, not integer-only. CKKS is a natural fit for approximate encrypted arithmetic over real-valued signals.

### Narrow feature scope

The project starts with one feature instead of an entire telemetry schema. This keeps the prototype easier to reason about and makes encryption setup issues easier to isolate.

### In-memory ciphertexts

The current version does not persist ciphertexts. That avoids introducing incomplete storage/key-management claims before the encrypted analytics path is fully designed.

## Challenges

### Binding setup

Microsoft SEAL Python usage depends on native bindings and environment setup. The README documents this clearly instead of implying a simple pure-Python install.

### Approximate arithmetic

CKKS results are approximate. Any downstream analytics must account for scale, precision loss, and parameter choices.

### Production security

A production system would need threat modeling, key management, parameter validation, serialization policy, and security review. This repository is intentionally framed as a research prototype.

## What this demonstrates

- Applied homomorphic-encryption experimentation.
- Awareness of privacy risks in embodied telemetry.
- Practical CKKS parameter setup for real-valued signals.
- A narrow, testable path toward encrypted XR analytics.

## Future work

- Add a synthetic sample dataset.
- Add encrypted aggregate operations.
- Persist ciphertexts in a documented format.
- Add tests for CSV validation and encryption setup.
- Connect the pipeline to a larger telemetry-processing backend.
