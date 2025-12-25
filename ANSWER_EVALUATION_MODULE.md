# Interview Answer Evaluation Module

## Overview

The interview answer evaluation module (`src/app/nlp/answer_evaluator.py` and `src/app/nlp/evaluation_report.py`) provides comprehensive evaluation of interview responses based on three key criteria:

1. **Relevance** (50% weight) - How well the answer addresses the question
2. **Depth** (30% weight) - Level of detail and comprehensiveness
3. **Clarity** (20% weight) - Clarity and understandability of the answer

## Features

### Pure Python Implementation
- No external dependencies
- Uses only Python standard library (`re`, `collections`, `dataclasses`)
- Easy to integrate and deploy

### Comprehensive Scoring
- **Relevance Score**: Measures keyword overlap, answer length appropriateness, and direct addressing of the question
- **Depth Score**: Evaluates vocabulary richness, concrete examples, nuance awareness, and technical details
- **Clarity Score**: Assesses sentence structure, logical flow, organization, and ambiguous language

### Multiple Output Formats
- Text reports for human reading
- Markdown reports for documentation
- Dictionary/JSON format for API integration
- Batch evaluation reports for multiple questions

## Usage

### Basic Evaluation

```python
from app.nlp import evaluate_answer

question = "Tell me about a time when you had to handle a conflict within your team."
answer = "In my previous role as a team lead, I had two developers who strongly disagreed..."

result = evaluate_answer(question, answer, question_type="behavioral")

print(f"Overall Score: {result.overall_score_percent}/100")
print(f"Relevance: {result.relevance_score:.2f}")
print(f"Depth: {result.depth_score:.2f}")
print(f"Clarity: {result.clarity_score:.2f}")
print(f"\nSummary: {result.explanation}")
print("\nStrengths:")
for strength in result.strengths:
    print(f"  - {strength}")
```

### Dictionary Format (for APIs)

```python
from app.nlp import evaluate_answer_dict

result = evaluate_answer_dict(question, answer, "behavioral")
# Returns a dictionary with all evaluation data
```

### Generating Reports

```python
from app.nlp import generate_report

# Text format
text_report = generate_report(question, answer, format="text")
print(text_report)

# Markdown format
markdown_report = generate_report(question, answer, format="markdown")

# Dictionary format
dict_report = generate_report(question, answer, format="dict")
```

### Batch Evaluation

```python
from app.nlp import InterviewEvaluationReport, BatchEvaluationReport, evaluate_answer

batch_report = BatchEvaluationReport(candidate_name="John Doe")

# Add multiple evaluations
for q, a in interview_data:
    eval_result = evaluate_answer(q, a)
    single_report = InterviewEvaluationReport(
        question=q,
        answer=a,
        question_type="general",
        evaluation=eval_result,
    )
    batch_report.add_evaluation(single_report)

# Get formatted output
print(batch_report.format_text())
# or
print(batch_report.format_markdown())

# Get average scores
avg_scores = batch_report.calculate_average_scores()
```

### Sample Reports

```python
from app.nlp import generate_sample_report, generate_sample_reports_comparison

# Generate a single sample report
print(generate_sample_report())

# Generate comparison of different answer qualities
print(generate_sample_reports_comparison())
```

## Scoring Details

### Relevance (50% weight)

The relevance score is calculated based on:
- **Keyword overlap**: How many key terms from the question appear in the answer
- **Answer length**: Appropriate length relative to the question (too short = incomplete)
- **Direct addressing**: Use of relevance boosters like "first", "specifically", "to illustrate"

**Scoring ranges:**
- 0.8-1.0: Directly addresses the question
- 0.6-0.8: Addresses most aspects of the question
- 0.4-0.6: Partially addresses the question
- 0.0-0.4: Does not adequately address the question

### Depth (30% weight)

The depth score is calculated based on:
- **Vocabulary richness**: Unique words relative to total words
- **Concrete examples**: Use of phrases like "in my previous role", "we implemented"
- **Nuance awareness**: Recognition of trade-offs and complexities
- **Multiple approaches**: Discussion of alternative methods or perspectives
- **Specific details**: Numbers, percentages, metrics, timeframes

**Scoring ranges:**
- 0.7-1.0: Demonstrates strong subject knowledge with detail and nuance
- 0.5-0.7: Shows good understanding with reasonable detail
- 0.3-0.5: Shows basic understanding but lacks depth
- 0.0-0.3: Insufficient detail to demonstrate expertise

### Clarity (20% weight)

The clarity score is calculated based on:
- **Sentence structure**: Avoids overly long sentences
- **Logical flow**: Uses flow indicators like "first", "however", "therefore"
- **Organization**: Use of bullet points or numbered lists
- **Concrete examples**: Uses examples to illustrate points
- **Ambiguous language**: Penalizes tentative language ("kind of", "maybe")

**Scoring ranges:**
- 0.8-1.0: Clear and well-structured communication
- 0.6-0.8: Generally clear with minor improvements possible
- 0.4-0.6: Could be improved with better structure and examples
- 0.0-0.4: Needs significant improvement to be understandable

## Output Format

The evaluation result includes:

```python
AnswerEvaluation(
    relevance_score=0.67,      # 0.0 to 1.0
    clarity_score=0.74,        # 0.0 to 1.0
    depth_score=0.72,          # 0.0 to 1.0
    overall_score=0.69,        # 0.0 to 1.0
    overall_score_percent=69,  # 0 to 100
    explanation="...",         # Human-readable summary
    strengths=[...],           # List of identified strengths
    weaknesses=[...],          # List of areas to improve
    suggestions=[...]          # Actionable improvement suggestions
)
```

## Demo Scripts

Two demo scripts are included in the `examples/` directory:

1. **answer_evaluation_demo.py** - Demonstrates basic usage with three sample questions of different types
2. **answer_comparison_demo.py** - Shows comparison of excellent, average, and poor answers to the same question

Run the demos with:
```bash
PYTHONPATH=/home/engine/project/src python examples/answer_evaluation_demo.py
PYTHONPATH=/home/engine/project/src python examples/answer_comparison_demo.py
```

## Integration with FastAPI

Example endpoint integration:

```python
from fastapi import APIRouter
from app.nlp import evaluate_answer_dict
from pydantic import BaseModel

router = APIRouter()

class EvaluationRequest(BaseModel):
    question: str
    answer: str
    question_type: str = "general"

@router.post("/evaluate-answer")
async def evaluate_interview_answer(request: EvaluationRequest):
    result = evaluate_answer_dict(request.question, request.answer, request.question_type)
    return result
```

## Design Philosophy

The module follows the same design principles as the existing NLP module:

1. **Zero external dependencies** - Uses only Python standard library
2. **Deterministic results** - No random elements or paid APIs
3. **Layered architecture** - Separate evaluation logic from report formatting
4. **Dataclass structures** - Clean, type-safe data structures
5. **Multiple output formats** - Flexible integration options

## Question Types

The module supports different question types:

- `general` - General questions (default)
- `technical` - Technical/programming questions
- `behavioral` - Behavioral interview questions
- `situational` - Situational/hypothetical questions

Question type can be used to adjust scoring weights if needed in future enhancements.

## Limitations

1. **Keyword-based matching**: The module uses pattern matching and keyword analysis, not semantic understanding
2. **Context-independent**: Each answer is evaluated in isolation without considering previous questions or responses
3. **Subject knowledge**: Cannot verify factual accuracy of technical claims
4. **Language support**: Designed for English; other languages may need adaptation

## Future Enhancements

Possible improvements for future versions:

1. **Configurable weights**: Allow customization of scoring weights per job role or level
2. **Pattern libraries**: Pre-built patterns for specific domains (e.g., healthcare, finance)
3. **Answer length calibration**: Adjust optimal length expectations by question type
4. **Sentiment analysis**: Include tone and confidence indicators
5. **Comparison mode**: Evaluate candidate answers against ideal answer templates

## API Reference

### Functions

- `evaluate_answer(question, answer, question_type="general")` - Returns `AnswerEvaluation` dataclass
- `evaluate_answer_dict(question, answer, question_type="general")` - Returns dictionary
- `generate_report(question, answer, question_type="general", format="text")` - Returns formatted report
- `generate_sample_report()` - Returns sample evaluation report
- `generate_sample_reports_comparison()` - Returns comparison of different answer qualities

### Classes

- `AnswerEvaluation` - Dataclass containing all evaluation results
- `InterviewEvaluationReport` - Single Q&A evaluation report with formatting
- `BatchEvaluationReport` - Multi-question batch evaluation with averages

## License

This module is part of the ai-voice-interviewer project.
