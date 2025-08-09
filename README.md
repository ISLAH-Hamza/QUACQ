# QUACQ – Constraint Acquisition Implementation  

This repository provides an **implementation of the QUACQ algorithm** for **constraint acquisition**.  
QUACQ is an interactive learning method designed to acquire constraints of a target problem through **queries** to an oracle (user or simulated system).  

**Original paper:** [QUACQ: A System for Constraint Acquisition](https://hal.science/lirmm-04028358/)  

---

## 🔍 Overview  

- **Purpose:** Learn constraints of a CSP (Constraint Satisfaction Problem) from examples, without requiring the complete model beforehand.  
- **Algorithm:** Implements the **QUACQ** method, which iteratively generates examples, queries an oracle, and narrows down the possible constraint set.  
- **Solver:** Uses [OR-Tools CP-SAT solver](https://developers.google.com/optimization) for satisfiability checks.  
- **Relations Supported:**  
  - Unary: `==val`, `!=val`, `<val`, `<=val`, `>val`, `>=val`  
  - Binary: `==`, `!=`, `<`, `<=`, `>`, `>=`  
  - Distance-based: `||==val`, `||!=val`, `||<val`, `||<=val`, `||>val`, `||>=val`  

---

## 📦 Features  

- Interactive constraint acquisition loop.  
- Support for **directed** and **undirected** relations.  
- Modular design:
  - `core.py` – Core classes: Variables, Relations, Constraints, Bias generation.
  - `quacq.py` – Implementation of QUACQ logic and supporting functions.
- Compatible with **Python ≥ 3.8**.  
- Logging support for monitoring the acquisition process.  

---

## 🚀 Getting Started  

### 1️⃣ Installation  
Clone the repository and install the dependencies using **pyproject.toml**:  
```bash
git clone https://github.com/yourusername/quacq.git
cd quacq
pip install .
