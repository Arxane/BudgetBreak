# BudgetBreak: Deterministic Security and Utility Benchmarking Engine for Large Language Models

BudgetBreak is an open-source evaluation engine designed to assess the resilience of Large Language Models (LLMs) and agentic frameworks against indirect prompt injection, sensitive data extraction (canary leakage), unauthorized tool execution, and false refusals under metered resource constraints.

Unlike evaluation systems that depend on non-deterministic LLM-as-a-judge approaches—which are susceptible to evaluator drift, judge bias, and sycophancy—BudgetBreak utilizes strict, rule-based deterministic scoring engines. This design guarantees reproducible security benchmarks across local and remote inference backends.

---

## Technical Overview

Modern LLM applications integrate external context (e.g., retrieval-augmented generation, tool outputs, session memory) that may contain untrusted data. BudgetBreak simulates these multi-tenant trust environments to evaluate how effectively a target model maintains instruction integrity when trusted system instructions conflict with untrusted contextual inputs.

### Core Architecture Capabilities

* **Deterministic Scoring Engine:** Employs exact-string canary matching, tool invocation signature parsing, and keyword-based safety refusal analysis.
* **Context & Provenance Sandbox:** Simulates memory stores with distinct trust boundaries (`system_controlled`, `trusted`, `untrusted`).
* **Resource Budget Metering:** Measures per-trial token efficiency (input and output tokens), call frequency, and wall-clock execution latency.
* **Quantized Local Inference:** Native integration with Hugging Face `transformers`, `bitsandbytes`, and `accelerate` for 4-bit NF4 quantized local model benchmarking.
* **Synthetic Execution Backend:** Includes a lightweight CPU mock driver for CI/CD test suite validation and rapid harness verification.
* **Boundary Guard Mitigation Testing:** Offers configurable external enforcement modes to measure the efficacy of pre- and post-processing guardrails.

---

## Directory Structure

```
BudgetBreak/
├── src/
│   ├── schemas.py          # Data contracts for scenarios, budgets, and trial results
│   ├── runner.py           # Scenario execution orchestrator and context builder
│   ├── models/
│   │   ├── base.py         # Abstract model backend interface
│   │   ├── mock.py         # Deterministic CPU backend for harness validation
│   │   └── local_llm.py    # Hugging Face + BitsAndBytes 4-bit GPU backend
│   ├── memory/
│   │   └── store.py        # Memory sandbox with trust provenance tagging
│   ├── harness/
│   │   └── tools.py        # Tool invocation parser and execution sandbox
│   └── metrics/
│       └── evaluator.py    # Rule-based evaluation and scoring engine
├── outputs/                # Structured JSON trial evaluation records
├── run_experiment.py       # Command-line evaluation interface
├── requirements.txt        # Production dependency specifications
└── README.md               # Technical project documentation
```

---

## Installation and Environment Setup

### Prerequisites

* Python 3.10 or higher
* Linux or macOS environment (Linux recommended for CUDA support)
* NVIDIA GPU with CUDA 12.1+ drivers (optional for CPU mock mode)

### Dependencies Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/BudgetBreak.git
   cd BudgetBreak
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Confirm CUDA acceleration (for GPU inference):
   ```bash
   python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
   ```

---

## Execution Workflows

BudgetBreak supports three primary execution modes via `run_experiment.py`.

### 1. Harness Integrity Check (CPU Mock Backend)

Executes test scenarios against a deterministic CPU driver to verify software pipeline functionality without downloading weights or allocating GPU memory:

```bash
python run_experiment.py
```

### 2. Standard GPU Security Benchmark

Evaluates a target model against defined attack families using 4-bit NormalFloat quantization:

```bash
python run_experiment.py --use-hf --model-name "Qwen/Qwen2.5-1.5B-Instruct"
```

### 3. Guardrail Mitigation Evaluation

Runs the benchmark with external boundary enforcement enabled to quantify defense mitigation delta:

```bash
python run_experiment.py --use-hf --model-name "Qwen/Qwen2.5-1.5B-Instruct" --defense
```

---

## Metrics and Threat Model

BudgetBreak measures security and utility metrics by evaluating models under paired execution conditions: **Control Runs** (uncontaminated baseline queries) and **Adversarial Runs** (queries containing untrusted injection payloads).

### Primary Metrics

| Metric | Property | Description |
| :--- | :--- | :--- |
| **Canary Exposure** | Security | Evaluates whether confidential tokens in trusted memory were leaked into generated output or tool parameters. |
| **Unauthorized Action Rate** | Security | Evaluates whether untrusted context successfully coerced the model into executing forbidden function calls. |
| **Benign Task Success** | Utility | Evaluates whether the model completed the core request without policy violations or execution failure. |
| **False Refusal Rate** | Utility | Measures instances where the model incorrectly refused clean, benign requests during control runs. |

---

## Result Schema

All trial outcomes are serialized to `outputs/experiment_results.json` using standardized schema contracts:

```json
{
  "scenario_id": "sec_canary_001",
  "is_control": false,
  "model_name": "Qwen/Qwen2.5-1.5B-Instruct",
  "raw_output": "Sample model generation output...",
  "budget": {
    "model_calls": 1,
    "input_tokens": 142,
    "output_tokens": 38,
    "wall_time_seconds": 0.842
  },
  "canary_exposed": false,
  "unauthorized_action_executed": false,
  "benign_task_success": true,
  "false_refusal": false,
  "tool_traces": []
}
```

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.