# AB Testing – Appointment Reminder Experiment

A clean, modular Python toolkit for designing, running, and analyzing A/B tests, focused on an **SMS appointment reminder** experiment.

The goal of the experiment is to answer:

> Will adding SMS reminders (on top of email) increase appointment attendance rates?

---

## Project Structure
```
AB_testing/
├── src/
│   └── ab_testing/
│       ├── init.py          # Public API
│       ├── assignment.py        # Experiment assignment + ReminderExperiment
│       ├── experiment.py        # Experiment definition (hypotheses, metrics)
│       ├── metrics.py           # MetricsCalculator + confidence intervals
│       └── reporting.py         # Report generation
├── scripts/
│   └── run_analysis.py          # End-to-end analysis script
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Features

- **Deterministic user assignment** using SHA-256 hashing
- Traffic allocation control (e.g. 50% of users in the experiment)
- Eligibility rules (phone number + SMS preference + has appointments)
- Attendance rate calculation via SQL
- Confidence interval for the difference in proportions (`statsmodels`)
- Business impact estimation (savings vs SMS cost)
- Clean report generation

---

## Installation

```bash
# Clone the repository
git clone https://github.com/ewangila/AB_testing.git
cd AB_testing

# Recommended: create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install in editable mode
pip install -e .

# Or with development tools
pip install -e ".[dev]"
```
## Quick Start

### 1. Run the full analysis

```bash
python scripts/run_analysis.py
```
This will:

* Calculate attendance rates for control & treatment
* Compute the 95% confidence interval for the lift
* Estimate projected annual savings

### 2. Use the library in your own code

```python
from ab_testing import MetricsCalculator, ReminderExperiment, generate_experiment_report
from datetime import datetime, timedelta

# Assignment
experiment = ReminderExperiment()
variant = experiment.get_variant("user_123")
print(variant)  # 'treatment', 'control', or 'excluded'

# Metrics
calculator = MetricsCalculator()
start = datetime.now() - timedelta(days=28)
end = datetime.now()

control_rate = calculator.calculate_attendance_rate("control", start, end)
treatment_rate = calculator.calculate_attendance_rate("treatment", start, end)

print(f"Control: {control_rate:.1f}% | Treatment: {treatment_rate:.1f}%")
```
## Experiment Definition

| Item                      | Value                                                             |
| ------------------------- | ----------------------------------------------------------------- |
| Business Question         | Will SMS reminders increase attendance?                           |
| Null Hypothesis           | SMS reminders have no effect                                      |
| Alternative Hypothesis    | SMS reminders increase attendance                                 |
| Primary Metric            | Appointment attendance rate                                       |
| Minimum Detectable Effect | 5 percentage points                                               |
| Secondary Metrics         | Patient satisfaction, provider satisfaction, support contact rate |
| Guardrail Metrics         | App crash rate, system error rate                                 |

---

## Current Results (Mock Data)

| Metric                  | Control | Treatment | Lift           |
| ----------------------- | ------- | --------- | -------------- |
| Attendance Rate         | 75.0%   | 80.5%     | +5.5 pp        |
| Relative Improvement    | –       | –         | +7.3%          |
| 95% Confidence Interval | –       | –         | [~4.8%, ~6.2%] |

> **Note**: The current implementation uses simulated data (10,000 appointments per group). Replace the mock database in `metrics.py` with real data for production use.

---

## Development

```bash
# Run tests (once you add them)
pytest

# Linting
ruff check src scripts
```
## License

MIT © 2026 Eugin Wangila
