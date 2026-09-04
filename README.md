<div align="center">

# 🧠 LLM Prompt Optimisation & Evaluation System

### Automatically generate, evaluate, compare, and select better prompts.

A modular Python system that uses an LLM to analyze a task, generate multiple prompt candidates, test them against the same evaluation scenarios, score their effectiveness, track token usage, and select the strongest prompt.

<br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Prompt Engineering](https://img.shields.io/badge/Prompt%20Engineering-LLM-orange?style=for-the-badge)
![LLM Evaluation](https://img.shields.io/badge/LLM--as--a--Judge-Evaluation-purple?style=for-the-badge)

</div>

---

## 🚀 Overview

Writing a prompt that works once is easy.

Writing a prompt that consistently produces high-quality results is harder.

This project treats **prompt engineering as an evaluation and optimization problem**.

Instead of manually deciding whether a prompt is better, the system automatically:

1. Analyzes the original task
2. Generates 3 optimized prompt candidates
3. Creates 2 neutral evaluation scenarios
4. Executes the baseline and candidates on the same scenarios
5. Evaluates the generated outputs
6. Evaluates prompt effectiveness
7. Tracks token usage
8. Selects the most effective prompt

### 🔄 System Workflow

```text
                         USER PROMPT
                              │
                              ▼
                    ┌──────────────────┐
                    │   TASK ANALYZER  │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
      ┌──────────────────┐      ┌──────────────────┐
      │ CANDIDATE        │      │ SCENARIO         │
      │ GENERATOR        │      │ GENERATOR        │
      │                  │      │                  │
      │ Candidate 1      │      │ Scenario 1       │
      │ Candidate 2      │      │ Scenario 2       │
      │ Candidate 3      │      │                  │
      └────────┬─────────┘      └────────┬─────────┘
               │                         │
               └────────────┬────────────┘
                            ▼
                 ┌─────────────────────┐
                 │  PROMPT EXECUTOR    │
                 │                     │
                 │ Baseline            │
                 │ Candidate 1         │
                 │ Candidate 2         │
                 │ Candidate 3         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    LLM-AS-A-JUDGE   │
                 │                     │
                 │ Output Quality      │
                 │ Prompt Effectiveness│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  METRIC AGGREGATION │
                 │                     │
                 │ Quality             │
                 │ Effectiveness       │
                 │ Token Usage         │
                 └──────────┬──────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ 🏆 BEST PROMPT│
                    └───────────────┘
