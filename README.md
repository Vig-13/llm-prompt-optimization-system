<div align="center">

# 🧠 LLM Prompt Optimisation & Evaluation System

### Automatically generate, evaluate, compare, and select better prompts.

A modular Python system that uses an LLM to analyze a task, generate multiple prompt candidates, test them against the same evaluation scenarios, evaluate their outputs and prompt effectiveness, track token usage, and select the strongest prompt.

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
8. Selects the strongest prompt

The result is a measurable workflow for comparing prompt-engineering strategies.

---

## 🔄 System Workflow

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
```

---

# ✨ Key Features

## 🔍 1. Automatic Task Analysis

The original user prompt is first analyzed into structured information:

- **Task Type**
- **Task Summary**
- **Expected Output**
- **Evaluation Focus**

Example:

```json
{
  "task_type": "email writing",
  "task_summary": "Write a professional email to a client explaining that a project has been delayed.",
  "expected_output": "A polite, professional email draft including a clear subject line, an explanation for the delay, a revised timeline, and an apology.",
  "evaluation_focus": [
    "tone",
    "clarity",
    "professionalism",
    "empathy",
    "actionability"
  ]
}
```

This structured task representation is then used by the downstream evaluation stages.

---

## 🧪 2. Multi-Strategy Prompt Optimization

The system generates **three different prompt candidates**, each using a distinct optimization strategy.

| Candidate | Optimization Strategy |
|-----------|-----------------------|
| 🎯 Candidate 1 | Clarity-focused |
| 🧩 Candidate 2 | Structure-focused |
| 📋 Candidate 3 | Constraint-focused |

### Candidate 1 — Clarity-focused

Improves clarity and removes ambiguity while preserving the original intent.

### Candidate 2 — Structure-focused

Improves organization, output structure, and explicit instructions.

### Candidate 3 — Constraint-focused

Adds explicit requirements, constraints, and instruction-following guidance.

The system therefore compares different prompt-engineering approaches instead of simply generating three similar rewrites.

---

## 🎭 3. Scenario-Based Evaluation

The system generates exactly **2 neutral evaluation scenarios** from the original task and its task analysis.

The scenarios are generated independently of the optimized prompt candidates.

Every prompt is then evaluated against the **same scenarios**.

```text
                    SAME TEST SCENARIOS
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      Baseline          Candidate 1      Candidate 2
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                       Candidate 3
```

Using identical scenarios provides a more controlled comparison between prompts.

---

## ⚖️ 4. LLM-as-a-Judge Evaluation

The system evaluates two separate dimensions:

### Output Quality

Generated outputs are evaluated using:

- Task Completion
- Requirement Satisfaction
- Scenario Appropriateness
- Expected Output Alignment

### Prompt Effectiveness

The prompts themselves are evaluated using:

- Task Clarity
- Requirement Coverage
- Output Specification
- Constraint Handling
- Ambiguity Reduction

The individual criteria are scored and aggregated into normalized scores.

```text
0.0 ─────────────────────────────── 1.0
Poor                              Excellent
```

> **Note:** The evaluation scores are LLM-generated assessments and should be interpreted as experiment-specific measurements rather than absolute measures of prompt quality.

---

## 📊 5. Quantitative Prompt Comparison

For every prompt, the system calculates:

- Average Output Quality
- Average Prompt Effectiveness
- Average Overall Score
- Minimum Output Quality
- Average Input Tokens
- Average Output Tokens
- Average Total Tokens

This turns prompt optimization from a purely subjective process into a measurable experiment.

---

## 🏆 6. Automatic Best-Prompt Selection

The system automatically selects the strongest prompt using the following priority:

1. **Highest Average Output Quality**
2. **Highest Minimum Output Quality**
   - Measures consistency across evaluation scenarios
3. **Highest Average Prompt Effectiveness**
4. **Lowest Average Token Usage**

The selected prompt is returned along with the reasoning behind the selection.

---

## 🔢 7. Token Usage Analysis

Every prompt execution tracks:

- Input Tokens
- Output Tokens
- Total Tokens

This allows the system to analyze the trade-off between prompt quality and token efficiency.

A longer prompt does not automatically mean a better prompt.

---

# 🖥️ Example Experiment

## Original Prompt

```text
Write an email to a client about a project delay.
```

The system analyzes the task and generates three optimized alternatives.

---

### 🎯 Candidate 1 — Clarity-focused

```text
Write a professional and polite email to a client explaining that their project is delayed.

Include placeholders for:
- Project name
- Reason for the delay
- New expected completion date
- Proposed next steps
```

---

### 🧩 Candidate 2 — Structure-focused

```text
Draft a client project delay email using the following structure:

1. Clear subject line indicating a project update.
2. Friendly opening and direct statement of the delay.
3. Brief, professional explanation of the cause.
4. Revised timeline with the new delivery date.
5. Reassurance and next steps.

Keep the tone empathetic, accountable, and proactive.
```

---

### 📋 Candidate 3 — Constraint-focused

```text
Write an email to a client notifying them of a project delay.

Constraints:

- Maintain a professional and reassuring tone.
- Do not make excuses; state the reason objectively.
- Clearly outline the revised timeline.
- Keep the word count under 150 words.
- Use placeholders where necessary.
```

The baseline and all three candidates are then executed against the same evaluation scenarios.

---

# 📈 Example Evaluation Result

One experiment produced the following results:

| Prompt | Output Quality | Prompt Effectiveness | Overall Score | Avg. Total Tokens |
|--------|---------------:|---------------------:|--------------:|------------------:|
| Baseline | 1.000 | 0.180 | 0.754 | 373.5 |
| Candidate 1 | 1.000 | 0.760 | 0.928 | 390.5 |
| Candidate 2 | 1.000 | 0.950 | 0.985 | 439.0 |
| Candidate 3 | 0.988 | 0.810 | 0.934 | 349.5 |

### 🏆 Selected Prompt

**Candidate 2**

```text
Draft a client project delay email using the following structure:

1. Clear subject line indicating a project update.
2. Friendly opening and direct statement of the delay.
3. Brief, professional explanation of the cause.
4. Revised timeline with the new delivery date.
5. Reassurance and next steps.

Keep the tone empathetic, accountable, and proactive.
```

Candidate 2 achieved the highest overall score, primarily because of its strong prompt-effectiveness score while maintaining excellent output quality across the evaluation scenarios.

> **Important:** These results are from a single experiment. LLM-based evaluation can vary between runs, so the scores should be treated as experimental measurements rather than universal benchmarks.

---

# 🏗️ Architecture

```text
                    ┌───────────────┐
                    │  User Prompt  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Task Analysis │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
     ┌─────────────────┐        ┌────────────────────┐
     │ Prompt          │        │ Evaluation         │
     │ Candidates      │        │ Scenarios          │
     │                 │        │                    │
     │ Candidate 1     │        │ Scenario 1         │
     │ Candidate 2     │        │ Scenario 2         │
     │ Candidate 3     │        │                    │
     └────────┬────────┘        └─────────┬──────────┘
              │                           │
              └─────────────┬─────────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Prompt Execution    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Generated Outputs   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   LLM-as-a-Judge    │
                  │                     │
                  │ Output Quality      │
                  │ Prompt Effectiveness│
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Metric Aggregation  │
                  │                     │
                  │ Quality             │
                  │ Effectiveness       │
                  │ Token Usage         │
                  └──────────┬──────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Best Prompt   │
                    └────────────────┘
```

---

# 📸 Example Execution Output

The complete evaluation pipeline can be executed directly from the command line.

Example output:

```text
======================================================================
PROMPT EVALUATION RESULTS
======================================================================

Baseline
----------------------------------------
Average Output Quality: 1.000
Average Prompt Effectiveness: 0.180
Average Overall Score: 0.754

Candidate 1
----------------------------------------
Average Output Quality: 1.000
Average Prompt Effectiveness: 0.760
Average Overall Score: 0.928

Candidate 2
----------------------------------------
Average Output Quality: 1.000
Average Prompt Effectiveness: 0.950
Average Overall Score: 0.985

Candidate 3
----------------------------------------
Average Output Quality: 0.988
Average Prompt Effectiveness: 0.810
Average Overall Score: 0.934

======================================================================
BEST PROMPT
======================================================================

Candidate 2
```

---

# 🧮 Scoring Methodology

The system calculates the overall score using:

```text
Overall Score =
    70% × Output Quality
  + 30% × Prompt Effectiveness
```

### Why 70/30?

The primary objective is to produce a better result for the user's task.

Therefore:

```text
Task Performance > Prompt Design
```

Prompt effectiveness is still included because a prompt that communicates requirements more clearly and explicitly can provide better performance across future executions.

---

# 📁 Project Structure

```text
llm-prompt-optimization-system/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── generator.py
│   ├── gemini_client.py
│   ├── candidate_generator.py
│   ├── task_analyzer.py
│   ├── scenario_generator.py
│   ├── prompt_executor.py
│   ├── prompt_judge.py
│   ├── evaluator.py
│   └── prompts.py
│
├── experiments/
│   ├── test_candidate_generator.py
│   ├── test_evaluator.py
│   ├── test_gemini.py
│   ├── test_gemini_connection.py
│   ├── test_prompt_executor.py
│   ├── test_prompt_judge.py
│   ├── test_scenario_generator.py
│   └── test_task_analyzer.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Core application and evaluation pipeline |
| 🤖 Google Gemini API | LLM generation and evaluation |
| 🧠 Prompt Engineering | Prompt optimization strategies |
| ⚖️ LLM-as-a-Judge | Automated evaluation |
| 📦 JSON | Structured LLM responses |
| 🧩 Python Modules | Modular application architecture |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Vig-13/llm-prompt-optimization-system.git
cd llm-prompt-optimization-system
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

---

# ▶️ Running the Project

Run the complete evaluation pipeline from the project root:

```bash
python -m experiments.test_evaluator
```

## Individual Components

### Task Analysis

```bash
python -m experiments.test_task_analyzer
```

### Candidate Generation

```bash
python -m experiments.test_candidate_generator
```

### Scenario Generation

```bash
python -m experiments.test_scenario_generator
```

### Prompt Execution

```bash
python -m experiments.test_prompt_executor
```

### Prompt Evaluation

```bash
python -m experiments.test_prompt_judge
```

---

# 🧠 Design Principles

## Controlled Comparison

Every prompt is evaluated against the same evaluation scenarios.

This reduces variation caused by different test inputs.

---

## Separate Prompt and Output Evaluation

The system distinguishes between:

```text
How good was the generated answer?
                +
How effective was the prompt?
```

This prevents prompt quality and output quality from being treated as exactly the same measurement.

---

## Task Performance First

The optimization process prioritizes actual task performance.

A prompt is not considered better simply because it contains more instructions.

---

## Token Awareness

Token usage is tracked alongside quality metrics to understand the efficiency trade-off between prompt complexity and performance.

---

## Modular Architecture

Each stage of the pipeline has a focused responsibility.

```text
Task Analysis
      │
      ▼
Candidate Generation
      │
      ▼
Scenario Generation
      │
      ▼
Prompt Execution
      │
      ▼
LLM Evaluation
      │
      ▼
Metric Aggregation
      │
      ▼
Best Prompt Selection
```

This makes the system easier to test, debug, and extend.

---

# 🔐 Security

API credentials should never be committed to the repository.

Use:

```text
.env
```

for local API configuration.

The repository's `.gitignore` excludes:

```text
.env
__pycache__/
*.pyc
.venv/
venv/
.vscode/
```

---

# ⚠️ Current Scope

This project currently focuses specifically on **LLM prompt optimization and evaluation**.

The current implementation does **not** include:

- ❌ Retrieval-Augmented Generation (RAG)
- ❌ Vector databases
- ❌ Embeddings
- ❌ Agentic workflows
- ❌ Multi-agent systems
- ❌ Persistent experiment databases
- ❌ FastAPI deployment
- ❌ Docker deployment

These technologies are intentionally outside the current implementation scope.

---

# 🔮 Potential Future Improvements

Possible future extensions include:

- 📊 Persistent experiment tracking
- 🌐 Web-based interface
- ⚡ FastAPI backend
- 📚 Experiment history and comparison
- 🧪 Larger evaluation suites
- 👤 Human feedback integration
- 📈 Statistical comparison across repeated runs
- 💰 Cost-aware prompt optimization
- 🤖 Model-to-model evaluation
- ☁️ Production deployment

---

# 🎯 Why This Project?

Prompt engineering is often approached through trial and error.

This project explores a more systematic approach:

```text
                 Prompt Engineering
                         │
                         ▼
                Generate Candidates
                         │
                         ▼
                 Create Scenarios
                         │
                         ▼
                Controlled Execution
                         │
                         ▼
                  Evaluate Outputs
                    /           \
                   ▼             ▼
          Output Quality   Prompt Effectiveness
                   \             /
                    ▼           ▼
                    Metric Aggregation
                         │
                         ▼
                   Token Analysis
                         │
                         ▼
                  Select Best Prompt
```

The goal is to make prompt optimization:

- **Measurable**
- **Repeatable**
- **Comparable**
- **Engineering-driven**

rather than relying entirely on manual judgment.

---

# 📌 Key Takeaway

This project demonstrates practical experience with:

- Generative AI
- LLM API integration
- Prompt engineering
- Prompt optimization
- LLM evaluation
- LLM-as-a-Judge
- Structured model outputs
- Scenario-based testing
- Controlled experimentation
- Quantitative comparison
- Token usage analysis
- Modular Python architecture

---

<div align="center">

### 🧠 Prompt Engineering → Evaluation → Optimization

**Turning prompt experimentation into a measurable engineering workflow.**

</div>
