# ⭐ SSUM-AIM Formula Kernel (AIMFK) — Quickstart

**Deterministic • Replay-Verifiable • Tiny Formula Intelligence Kernel**

**No Probability • No Randomness • No Hidden State**

---

# What You Need to Know First

The **SSUM-AIM Formula Kernel (AIMFK)** is a minimal deterministic symbolic computation kernel built on the **Shunyaya Structural Universal Mathematics (SSUM)** framework.

AIMFK executes **bounded symbolic mathematical tasks** through deterministic rule transformations.

AIMFK **does not predict results**.

AIMFK **computes them deterministically**.

---

# What AIMFK Does Not Do

AIMFK does **not**:

• perform machine learning  
• perform probabilistic inference  
• train statistical models  
• inject randomness  
• predict outcomes  
• alter classical mathematical semantics  

The kernel performs **deterministic symbolic computation only**.

---

# What AIMFK Does

AIMFK:

• accepts **manifest-bounded symbolic tasks**  
• evaluates symbolic mathematical expressions  
• performs deterministic transformations  
• produces **replay-verifiable results**  
• optionally records **proof traces**  

All computations are **fully deterministic**.

---

# Core Deterministic Rules

**Deterministic execution invariant**

`same task input -> same result`

**Mutation rule**

`changed input -> changed result`

**Replay rule**

`re-execution of identical task -> identical output`

There is **no probabilistic tolerance**.

Outputs must **match exactly**.

---

# Minimum Requirements

**Environment**

• Python 3.9+ (CPython recommended)  
• Standard library only  
• No external dependencies  

AIMFK runs **entirely offline**.

---

# Repository Structure

```
Public_Release/

├── README.md
├── LICENSE

├── CORE/
│   └── aimfk_router.py

├── MANIFESTS/
│   └── core_arithmetic_manifest.json

├── RUN/
│   └── RUN_AIMFK.cmd

├── EXAMPLES/
│   ├── example_eval.json
│   ├── example_subst.json
│   ├── example_verify.json
│   ├── example_poly_eval.json
│   ├── example_poly_sum.json
│   ├── example_poly_mul.json
│   ├── example_matrix_add.json
│   ├── example_matrix_sub.json
│   ├── example_matrix_mul.json
│   ├── example_solve_linear.json
│   └── example_solve_quadratic.json

├── TASKS/
│   └── TASK_RESULT.json

├── release/
│   ├── AIMFK_RELEASE_NOTES.txt
│   ├── FREEZE_NOTE.txt
│   └── VERIFY_SHA256.txt

└── docs/
    ├── Quickstart.md
    └── FAQ.md
```

---

# Freeze Boundary

The **frozen computational boundary** includes:

`CORE`  
`MANIFESTS`  
`RUN`  
`EXAMPLES`  
`release`

Hashes of frozen artifacts are recorded in:

`release/VERIFY_SHA256.txt`

---

# Runtime Folder

The **TASKS folder** stores runtime task outputs generated during kernel execution.

Files inside `TASKS` are **not part of the frozen release boundary** and may change during execution.

---

# Documentation

Documentation files remain **outside the frozen boundary** and may evolve independently of the deterministic kernel implementation.

---

# 30-Second Demo

Navigate to the project directory.

Run the kernel using an example task.

```
python CORE\aimfk_router.py EXAMPLES\example_eval.json
```

Example output:

```
task: EVAL  
expression: 3*(5+2)^2  
result: 147
```

You just executed a **deterministic symbolic computation**.

---

# Run Additional Examples

Try other symbolic operations:

```
python CORE\aimfk_router.py EXAMPLES\example_subst.json
```

```
python CORE\aimfk_router.py EXAMPLES\example_verify.json
```

```
python CORE\aimfk_router.py EXAMPLES\example_poly_eval.json
```

```
python CORE\aimfk_router.py EXAMPLES\example_matrix_add.json
```

Each task demonstrates **deterministic symbolic transformations**.

---

# Fallback Execution Mode

AIMFK also supports **fallback execution** using a task payload file.

Create:

`TASKS/TASK_PAYLOAD.json`

Example:

```
{
  "task": "EVAL",
  "expression": "3*(5+2)^2"
}
```

Run:

```
python CORE\aimfk_router.py
```

The kernel will read the payload and produce:

`TASKS/TASK_RESULT.json`

---

# Replay Demonstration

Replay verification means **identical tasks produce identical outputs**.

Example:

```
python CORE\aimfk_router.py EXAMPLES\example_eval.json
```

```
python CORE\aimfk_router.py EXAMPLES\example_eval.json
```

Results must match **exactly**.

Replay rule:

`same task input -> same result`

---

# Mutation Demonstration

Changing the task input changes the output **deterministically**.

Example:

Modify the task file:

`3*(5+2)^2`

to

`3*(5+3)^2`

Run again.

The result will change **deterministically**.

Mutation rule:

`changed input -> changed result`

---

# Structural Computation Model

AIMFK performs **deterministic symbolic transformations**.

Conceptually:

`Result = Φ(Task, Rules, Inputs)`

Where:

Task = symbolic operation requested  
Rules = deterministic transformation rules  
Inputs = task parameters  

The transformation produces:

• deterministic results  
• symbolic transformation records  
• replay-verifiable outputs  

---

# What AIMFK Certifies

AIMFK certifies:

• deterministic symbolic computation  
• replay-verifiable formula evaluation  
• manifest-bounded rule execution  

AIMFK **does not certify**:

• algorithm correctness  
• domain validity  
• numerical conditioning  
• regulatory compliance  

The kernel demonstrates **deterministic formula intelligence only**.

---

# One-Line Summary

**AIMFK** is a tiny deterministic symbolic computation kernel that performs **replay-verifiable formula intelligence** through explicit rule transformations within the **SSUM framework**.
