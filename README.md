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

🔍 1. Automatic Task Analysis

The original user prompt is analyzed into structured information:

Task type
Task summary
Expected output
Evaluation focus

Example:

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
🧪 2. Multi-Strategy Prompt Optimization

The system generates three different prompt candidates, each using a different optimization strategy.

Candidate	Optimization Strategy
🎯 Candidate 1	Clarity-focused
🧩 Candidate 2	Structure-focused
📋 Candidate 3	Constraint-focused

This allows the system to compare different prompt-engineering approaches instead of generating three nearly identical prompts.

🎭 3. Scenario-Based Evaluation

The system generates exactly two neutral evaluation scenarios from the original task and its task analysis.

The scenarios are created independently of the optimized prompt candidates.

Every prompt is then tested against the same scenarios.

                   SAME TEST SCENARIOS
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
       Baseline       Candidate 1     Candidate 2
          │               │               │
          └───────────────┼───────────────┘
                          │
                          ▼
                     Candidate 3

This provides a more controlled comparison between prompts.

⚖️ 4. LLM-as-a-Judge Evaluation

The system evaluates both the generated outputs and the prompt instructions themselves.

Output Quality

Generated outputs are evaluated using:

Task Completion
Requirement Satisfaction
Scenario Appropriateness
Expected Output Alignment
Prompt Effectiveness

Prompts are evaluated using:

Task Clarity
Requirement Coverage
Output Specification
Constraint Handling
Ambiguity Reduction

Scores are normalized between:

0.0 ─────────────────────── 1.0
Poor                         Excellent
📊 5. Quantitative Prompt Comparison

For every prompt, the system calculates:

Average Output Quality
Average Prompt Effectiveness
Average Overall Score
Minimum Output Quality
Average Input Tokens
Average Output Tokens
Average Total Tokens

This transforms prompt optimization from a purely subjective process into a measurable experiment.

🏆 6. Automatic Best-Prompt Selection

The system automatically selects the strongest prompt using the following priority:

1. Highest Average Output Quality
2. Highest Minimum Output Quality
   → Measures consistency across scenarios
3. Highest Prompt Effectiveness
4. Lowest Token Usage

The selected prompt is returned along with the selection reasoning.

🔢 7. Token Usage Analysis

Every prompt execution tracks:

Input Tokens
Output Tokens
Total Tokens

This makes it possible to analyze the trade-off between prompt quality and token usage.

🖥️ Example
Original Prompt
Write an email to a client about
a project delay.

The system generates multiple optimized alternatives.

🎯 Candidate 1 — Clarity-focused
Write a professional and polite email to a client
explaining that their project is delayed. Include
placeholders for the project name, the reason for
the delay, the new expected completion date, and
proposed next steps.
🧩 Candidate 2 — Structure-focused
Draft a client project delay email using the
following structure:

1. Clear subject line indicating a project update.
2. Friendly opening and direct statement of the delay.
3. Brief, professional explanation of the cause.
4. Revised timeline with the new delivery date.
5. Reassurance and next steps.

Keep the tone empathetic, accountable, and proactive.
📋 Candidate 3 — Constraint-focused
Write an email to a client notifying them of
a project delay.

Constraints:
- Maintain a professional and reassuring tone.
- Do not make excuses.
- Clearly outline the revised timeline.
- Keep the word count under 150 words.
- Use placeholders where necessary.

The four prompts are then executed against the same evaluation scenarios.

📈 Example Evaluation Result

One experiment produced the following results:

Prompt	Output Quality	Prompt Effectiveness	Overall Score	Avg. Total Tokens
Baseline	1.000	0.180	0.754	373.5
Candidate 1	1.000	0.760	0.928	390.5
Candidate 2	1.000	0.950	0.985	439.0
Candidate 3	0.988	0.810	0.934	349.5
🏆 Selected Prompt

Candidate 2

Draft a client project delay email using the following structure:
1. Clear subject line indicating a project update.
2. Friendly opening and direct statement of the delay.
3. Brief, professional explanation of the cause.
4. Revised timeline with the new delivery date.
5. Reassurance and next steps.
Keep the tone empathetic, accountable, and proactive.

The candidate achieved the highest prompt-effectiveness score while maintaining excellent output quality and consistency across the evaluation scenarios.

Note: Evaluation scores are LLM-generated assessments and should be interpreted as experiment-specific rather than absolute measures of prompt quality.

🏗️ Architecture

Pipeline
User Prompt
     │
     ▼
Task Analysis
     │
     ├───────────────┐
     ▼               ▼
Prompt Candidates   Evaluation Scenarios
     │               │
     └───────┬───────┘
             ▼
      Prompt Execution
             │
             ▼
      Generated Outputs
             │
             ▼
        LLM-as-a-Judge
         /          \
        ▼            ▼
Output Quality   Prompt Effectiveness
        \            /
         ▼          ▼
          Aggregation
               │
               ▼
          Best Prompt
📸 Example Execution

The system can be executed directly from the command line and produces structured evaluation results.

Example:

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
🧮 Scoring Methodology

The system calculates the overall score using:

Overall Score =
    70% × Output Quality
  + 30% × Prompt Effectiveness
Why 70/30?

The primary objective is to produce a better result for the user's task.

Therefore:

Task Performance > Prompt Design

Prompt effectiveness is still included because a prompt that consistently communicates requirements better is generally more useful for future executions.

📁 Project Structure
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
├── assets/
│   ├── architecture.png
│   └── evaluation-output.png
│
├── README.md
├── requirements.txt
└── .gitignore
🛠️ Tech Stack
Technology	Purpose
🐍 Python	Core application and evaluation pipeline
🤖 Google Gemini API	LLM generation and evaluation
🧠 Prompt Engineering	Prompt optimization strategies
⚖️ LLM-as-a-Judge	Automated evaluation
📦 JSON	Structured LLM responses
🧩 Python Modules	Modular application architecture
⚙️ Installation
1. Clone the repository
git clone https://github.com/Vig-13/llm-prompt-optimization-system.git

cd llm-prompt-optimization-system
2. Create a virtual environment
Windows
python -m venv venv

venv\Scripts\activate
macOS / Linux
python3 -m venv venv

source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure the Gemini API key

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

The .env file is excluded from Git using .gitignore.

▶️ Running the Project

Run the complete evaluation pipeline from the project root:

python -m experiments.test_evaluator
Individual Components

Task analysis:

python -m experiments.test_task_analyzer

Candidate generation:

python -m experiments.test_candidate_generator

Scenario generation:

python -m experiments.test_scenario_generator

Prompt execution:

python -m experiments.test_prompt_executor

Prompt evaluation:

python -m experiments.test_prompt_judge
🧠 Design Principles
Controlled Comparison

Every prompt is evaluated against the same scenarios.

Separate Prompt and Output Evaluation

The system distinguishes between:

How good was the generated answer?
                +
How effective was the prompt?

This prevents prompt quality and output quality from being treated as exactly the same thing.

Task Performance First

Prompt optimization is primarily focused on improving actual task performance.

Token Awareness

More instructions do not automatically mean a better prompt.

Token usage is tracked to understand the efficiency trade-off.

Modular Architecture

Each stage of the pipeline has a focused responsibility, making the system easier to test, debug, and extend.

🔐 Security

API credentials should never be committed to the repository.

Use:

.env

for local API configuration.

The repository's .gitignore excludes:

.env
__pycache__/
*.pyc
.venv/
venv/
.vscode/
⚠️ Current Scope

This project currently focuses specifically on LLM prompt optimization and evaluation.

The current implementation does not include:

❌ Retrieval-Augmented Generation (RAG)
❌ Vector databases
❌ Embeddings
❌ Agentic workflows
❌ Multi-agent systems
❌ Persistent experiment databases
❌ FastAPI deployment
❌ Docker deployment

These technologies are intentionally outside the current implementation scope.

🔮 Potential Future Improvements

Possible future extensions include:

📊 Persistent experiment tracking
🌐 Web-based interface
⚡ FastAPI backend
📚 Experiment history and comparison
🧪 Larger evaluation suites
👤 Human feedback integration
📈 Statistical comparison across repeated runs
💰 Cost-aware prompt optimization
🤖 Model-to-model evaluation
☁️ Production deployment
🎯 Why This Project?

Prompt engineering is often approached through trial and error.

This project explores a more systematic approach:

Prompt Engineering
       │
       ▼
Generate Candidates
       │
       ▼
Create Test Scenarios
       │
       ▼
Controlled Execution
       │
       ▼
Evaluate Outputs
       │
       ├───────────────┐
       ▼               ▼
Output Quality   Prompt Effectiveness
       │               │
       └───────┬───────┘
               ▼
         Token Analysis
               │
               ▼
        Select Best Prompt

The goal is to make prompt optimization measurable, repeatable, and engineering-driven rather than relying entirely on manual judgment.

📌 Key Takeaway

This project demonstrates practical experience with:

Generative AI
LLM API integration
Prompt engineering
LLM evaluation
LLM-as-a-Judge
Structured model outputs
Scenario-based testing
Quantitative comparison
Token usage analysis
Modular Python architecture
