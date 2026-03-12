# ⭐ SSUM-AIM Formula Kernel (AIMFK)

A **~25 KB deterministic formula intelligence kernel** implementing the **Artificial Intelligence Manifest (AIM)** model within the **Shunyaya Structural Universal Mathematics (SSUM)** framework.

[![Release Verification](https://github.com/OMPSHUNYAYA/SSUM-AIM-Formula-Kernel/actions/workflows/release_verify.yml/badge.svg)](https://github.com/OMPSHUNYAYA/SSUM-AIM-Formula-Kernel/actions/workflows/release_verify.yml)

![SSUM-AIM](https://img.shields.io/badge/SSUM--AIM-Artificial%20Intelligence%20Manifest-black)
![Deterministic](https://img.shields.io/badge/Deterministic-Computation-green)
![Replay-Verifiable](https://img.shields.io/badge/Replay--Verifiable-Yes-brightgreen)
![Manifest-Bound](https://img.shields.io/badge/Manifest-Bound-blue)
![Kernel-Size](https://img.shields.io/badge/Kernel-~25KB-orange)
![Offline](https://img.shields.io/badge/Execution-Offline-lightgrey)
![Open-Standard](https://img.shields.io/badge/Standard-Open-blue)

Run it. Evaluate formulas. Verify results. Inspect proof traces.  
The architecture remains fully transparent for deeper exploration.

**Replay-Verifiable • Deterministic • Manifest-Bound • Tiny Deterministic Kernel**

---

# 🔎 What AIMFK Is (and Is Not)

AIMFK is **not a large language model** or probabilistic AI system.

It is a **tiny deterministic formula intelligence kernel** that performs symbolic computation through explicit rule transformations.

The system requires:

• zero training data  
• zero model weights  
• zero probabilistic inference  

Instead, AIMFK computes results using **deterministic symbolic rules** and produces **replay-verifiable proof traces**.

This makes AIMFK a **highly compact (~25 KB) verifiable formula intelligence kernel** capable of transparent, reproducible symbolic computation.

---

# ⚡ 30-Second Demo

Create a task file:

`TASKS/TASK_PAYLOAD.json`

Example:

```
{
  "task": "EVAL",
  "expression": "3*(5+2)^2"
}
```

Run the kernel:

```
python CORE\aimfk_router.py
```

Example output:

```
{
  "task": "EVAL",
  "expression": "3*(5+2)^2",
  "result": 147,
  "proof_trace_mode": "deterministic_proof_trace"
}
```

Run again → same result  
Change the expression → deterministic new result

---

# ⚡ Run It in 10 Seconds

Typical usage:

```
python CORE\aimfk_router.py
```

Or:

```
RUN\RUN_AIMFK.cmd
```

CLI payload execution mode:

```
python CORE\aimfk_router.py EXAMPLES\example_eval.json
```

Example tasks are located in:

`EXAMPLES\`

Each execution produces:

• deterministic results  
• replay-verifiable proof traces  
• deterministic outputs  

---

## 🔗 Quick Links

### 📘 Documentation

- [Quickstart Guide](docs/Quickstart.md) — Run the kernel in under a minute  
- [FAQ](docs/FAQ.md) — Conceptual overview and common questions  

---

### 📂 Repository Navigation

Explore the main project components:

[`CORE`](CORE/) • [`MANIFESTS`](MANIFESTS/) • [`EXAMPLES`](EXAMPLES/) • [`RUN`](RUN/) • [`TASKS`](TASKS/) • [`release`](release/) • [`docs`](docs/)

---

### 🔐 Release Verification

The frozen release boundary can be verified deterministically.

Run:

```
python CORE\aimfk_router.py --verify-release
```

Verification reads:

`release/VERIFY_SHA256.txt`

and confirms the integrity of all frozen artifacts.

---

### 📜 License

- [`LICENSE`](LICENSE)

---

# 🚀 Why This Is Interesting

Most modern AI systems depend on:

• training datasets  
• probabilistic inference  
• large model weights  

AIMFK demonstrates a **different approach**.

Formula intelligence can operate through:

• deterministic rules  
• symbolic transformations  
• manifest-bounded computation  

Instead of predicting answers, AIMFK **computes them deterministically**.

---

# 🧩 Four Integrity Properties of AIMFK

AIMFK is designed around four architectural properties that ensure reliable symbolic computation.

**Determinism**  
Identical inputs always produce identical outputs.

`same input → same result`

**Observability**  
Each computation can produce explicit proof traces describing the transformation steps used to derive the result.

**Reproducibility**  
Anyone can rerun the same computation using the frozen release and reproduce the same result.

**Verifiability**  
Results reduce directly to classical mathematics and can be independently checked using standard algebraic rules.

Together these properties create a **deterministic symbolic computation kernel that is observable, reproducible, and mathematically verifiable in a footprint of ~25 KB**.

---

# 📦 Kernel Size Overview

AIMFK demonstrates that meaningful symbolic computation can exist in a **very small deterministic kernel**.

Component | File | Size
---|---|---
Core formula kernel | CORE/aimfk_router.py | ~25 KB
Arithmetic manifest | MANIFESTS/core_arithmetic_manifest.json | ~710 B
Example workloads | EXAMPLES/ | small JSON examples
Run script | RUN/RUN_AIMFK.cmd | ~41 B

Release metadata:

File | Purpose
---|---
AIMFK_RELEASE_NOTES.txt | Release history and architecture notes
FREEZE_NOTE.txt | Freeze boundary declaration
VERIFY_SHA256.txt | Release verification hashes

The formula intelligence kernel itself is **~25 KB**.

---

# 📦 What Just Happened

AIMFK executed a **deterministic symbolic computation**.

Conceptually:

`Result = Phi(Task, Rules, Inputs)`

Where:

Task = requested symbolic operation  
Rules = deterministic transformation rules  
Inputs = supplied parameters  

The kernel performs a deterministic transformation and produces:

• result  
• proof trace  
• deterministic output  

---

# 🔬 Deterministic Computation Model

AIMFK computations follow deterministic transformations.

Conceptually:

`Phi(x) = deterministic_transformation(x)`

For identical task inputs:

`same input → same transformation → same output`

This property enables **replay-verifiable computation**.

---

# 🔁 Deterministic Replay

Running the same task again produces the same result.

Condition:

`same task payload → same result`

Changing any input changes the output:

• expression  
• coefficients  
• matrices  
• variable assignments  

This ensures **strict deterministic behavior**.

---

# ⚙ 60-Second Verification

Run:

```
python CORE\aimfk_router.py EXAMPLES\example_eval.json
```

Try additional examples:

example_subst.json  
example_verify.json  
example_poly_eval.json  
example_matrix_add.json  
example_solve_linear.json  

Each demonstrates **deterministic symbolic computation**.

---

# 🔐 Deterministic Release Verification

AIMFK supports **deterministic release verification**.

Run:

```
python CORE\aimfk_router.py --verify-release
```

This command reads:

`release/VERIFY_SHA256.txt`

The kernel then:

• recomputes SHA256 hashes  
• verifies frozen release files  
• detects missing or modified files  
• produces a deterministic verification receipt  

This allows **independent verification of the release boundary**.

---

# 🧠 SSUM-AIM Terminology

Within the Shunyaya framework, AI refers to **AIM — Artificial Intelligence Manifest**.

AIM represents a deterministic form of intelligence built on:

• explicit rule manifests  
• symbolic transformations  
• replay-verifiable computation  

Unlike conventional AI systems, AIMFK does not use:

• neural networks  
• training datasets  
• probabilistic inference  
• machine learning models  

AIMFK is therefore **not a chatbot or neural AI system**.

It is a **deterministic symbolic intelligence kernel**.

---

# 🌍 Kernel to System Evolution

The architecture expands gradually:

Formula  
→ Symbolic Transformation  
→ Deterministic Intelligence  
→ Verifiable Computation  
→ Reproducible Systems  

AIMFK implements the **first deterministic layer**.

---

# 🔒 Deterministic Scope

AIMFK certifies:

**deterministic formula computation**

AIMFK does **not certify**:

• algorithm correctness  
• domain validity  
• numerical conditioning  
• runtime environment hermeticity  
• system performance  

The kernel guarantees **deterministic symbolic computation only**.

---

# 🔍 Positioning

Aspect | AIMFK | Conventional AI
---|---|---
Model size | ~25 KB kernel | Large models
Computation | Deterministic formulas | Probabilistic inference
Transparency | Fully observable | Often opaque
Verification | Replay-verifiable | Difficult to verify
Scope | Symbolic tasks | Open-ended generation

---

# 📜 Open Standard

AIMFK is published as an **open deterministic formula intelligence kernel**.

Attribution is recommended but not required.

Preferred form:

Implements the **SSUM-AIM Formula Kernel (AIMFK)** methodology.

---

# One-Line Summary

A **tiny deterministic formula intelligence kernel (~25 KB)** enabling **replay-verifiable symbolic computation** within the **Shunyaya Structural Universal Mathematics (SSUM)** framework.
