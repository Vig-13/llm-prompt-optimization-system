<div align="center">

# 🧠 LLM Prompt Optimisation & Evaluation System

### Automatically generate, evaluate, compare, and select better prompts.

A modular Python system that uses an LLM to analyze a task, generate multiple prompt candidates, test them against the same evaluation scenarios, score their effectiveness, track token usage, and select the strongest prompt.

<br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Prompt Engineering](https://img.shields.io/badge/Prompt%20Engineering-LLM-orange?style=for-the-badge)
![LLM Evaluation](https://img.shields.io/badge/LLM--as--a--Judge-Evaluation-purple?style=for-the-badge)

</div>

---

## 🚀 Overview

Writing a prompt that works once is easy.

Writing a prompt that consistently produces high-quality results is harder.

This project treats prompt engineering as an **evaluation and optimization problem**.

Instead of manually deciding whether a prompt is better, the system:

```text
User Prompt
     │
     ▼
┌─────────────────────┐
│   Task Analysis     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Generate 3 Candidates│
│  • Clarity           │
│  • Structure         │
│  • Constraints       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Generate 2 Neutral   │
│ Evaluation Scenarios │
└─────────┬───────────┘
          │
          ▼
┌──────────────────────────────┐
│ Execute Baseline + Candidates│
│ on the SAME scenarios        │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│       LLM-as-a-Judge         │
│                              │
│ • Output Quality             │
│ • Prompt Effectiveness       │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│ Compare Scores + Token Usage │
└─────────────┬────────────────┘
              │
              ▼
       🏆 Best Prompt
