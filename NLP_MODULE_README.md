# Resume Screening NLP Module

A complete Python module for automated resume screening using pure Python and regex-based NLP.

## What's Included

### Core Module (`src/app/nlp/`)

1. **`skill_extractor.py`** - Extract technical and soft skills from resumes
2. **`education_extractor.py`** - Extract degrees, institutions, and education levels
3. **`experience_extractor.py`** - Extract job titles, companies, years of experience
4. **`scorer.py`** - Calculate match scores between resumes and job descriptions

### Examples

1. **`examples/resume_screening_example.py`** - Full demonstration with 2 sample resumes
2. **`test_nlp.py`** - Quick test script

## Quick Start

### Minimal Example

```python
from app.nlp.scorer import calculate_match_score

result = calculate_match_score(job_description, resume_text)
print(f"Match Score: {result['overall_score_percent']}%")
print(f"Explanation: {result['explanation']}")
```

### Running the Examples

```bash
PYTHONPATH=/home/engine/project/src python examples/resume_screening_example.py
```

## Example Input and Output

### Input

**Job Description:**
```
Senior Python Developer
5+ years Python, Django, AWS, Docker
Bachelor's degree in Computer Science
```

**Resume:**
```
John Smith - Senior Python Developer
Experience: Python, Django, AWS, Docker, 4 years
Education: BS Computer Science
Skills: Python, Django, PostgreSQL, FastAPI
```

### Output

```python
{
    "overall_score": 88,
    "overall_score_percent": 88,
    "component_scores": {
        "skills_match": 0.83,
        "experience_match": 0.80,
        "education_match": 1.0,
        "keyword_overlap": 0.31
    },
    "explanation": "Overall Match Score: 88%. Matched skills: python, django, aws, docker. Has 4 years experience (required: 5+). Meets education requirement (bachelor degree).",
    ...
}
```

## Features

- ✅ No external dependencies (uses Python stdlib only)
- ✅ No paid APIs (100% free)
- ✅ Extracts skills, education, and experience
- ✅ Calculates weighted match scores
- ✅ Provides human-readable explanations
- ✅ Easy to extend and customize

## File Structure

```
src/app/nlp/
├── __init__.py              # Main exports
├── skill_extractor.py       # Skill extraction (80+ tech skills)
├── education_extractor.py   # Education extraction
├── experience_extractor.py  # Work experience extraction
└── scorer.py               # Match score calculation

examples/
├── resume_screening_example.py  # Full demonstration
└── README.md

docs/
└── RESUME_SCREENING_NLP.md      # Complete documentation
```

## API Summary

| Function | Description |
|----------|-------------|
| `calculate_match_score(jd, resume)` | Calculate overall match (0-100%) |
| `extract_skills(text)` | Get technical and soft skills |
| `extract_education(text)` | Get degrees, institutions, level |
| `extract_experience(text)` | Get titles, companies, years |

## Scoring Weights

- **Skills Match**: 50% - Required skills found in resume
- **Experience Match**: 30% - Years and seniority level
- **Education Match**: 15% - Degree level and field
- **Keyword Overlap**: 5% - General language similarity

## Key Features

### Skill Database (80+ entries)
- Languages: Python, Java, JavaScript, C++, Go, etc.
- Frameworks: Django, Flask, FastAPI, React, Spring, etc.
- Cloud: AWS, Azure, GCP, Docker, Kubernetes
- Data: Pandas, NumPy, TensorFlow, PyTorch
- Soft skills: Leadership, communication, teamwork, etc.

### Education Levels
- Unknown → Diploma → Associate → Bachelor → Master → Doctorate

### Experience Analysis
- Job title extraction
- Company name detection
- Duration/year parsing
- Achievement extraction

## Complete Documentation

See `docs/RESUME_SCREENING_NLP.md` for:
- Full API reference
- Detailed examples
- Extension guide
- Customization instructions

## Running the Demo

```bash
PYTHONPATH=/home/engine/project/src python examples/resume_screening_example.py
```

Output shows:
- Skill extraction results
- Education extraction results  
- Experience extraction results
- Comparison of 2 candidates (strong vs weak match)
- Detailed explanations

## License

Part of the ai-interview-system project.
