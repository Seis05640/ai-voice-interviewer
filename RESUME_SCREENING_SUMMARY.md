# Resume Screening NLP Module - Summary

## What Was Built

A complete Python module for resume screening that:
1. ✅ Accepts resume text (PDF handling planned for future)
2. ✅ Extracts skills, education, and experience using simple NLP
3. ✅ Compares against job descriptions
4. ✅ Outputs match scores with explanations

**No external dependencies, no paid APIs - uses Python standard library only.**

---

## Example Input and Output

### INPUT 1: Job Description

```
Python Developer - 3+ years experience

Requirements:
• Python, Django, or FastAPI
• Experience with AWS or Docker
• Knowledge of PostgreSQL
• Bachelor's degree in Computer Science
```

### INPUT 2: Resume

```
John Doe - Python Developer

WORK EXPERIENCE
Python Developer | TechCompany | 2021 - Present
• Developed REST APIs using FastAPI and Django
• Deployed applications to AWS using Docker
• Designed PostgreSQL database schemas

Junior Developer | StartupXYZ | 2020 - 2021
• Python backend development

EDUCATION
Bachelor of Science in Computer Science, 2020

SKILLS
Python, Django, FastAPI, AWS, Docker, PostgreSQL, Git
```

### OUTPUT (Full Result)

```python
{
    "overall_score": 0.68,
    "overall_score_percent": 68,
    "component_scores": {
        "skills_match": 1.0,       # 100% - All required skills found
        "experience_match": 0.0,    # 0% - Years not parsed from text
        "education_match": 1.0,    # 100% - Meets education requirement
        "keyword_overlap": 0.63     # 63% - General text similarity
    },
    "explanation": "Overall Match Score: 70%. Matched skills: aws, django, docker, fastapi, postgresql, python. Has 0.0 years experience (required: 3+).",
    "resume_data": {
        "skills": {
            "technical": ["docker", "rest", "postgresql", "aws", "django", "fastapi", "python", "git", ...],
            "soft": [],
            "total_count": 10
        },
        "education": {
            "degrees": ["Bachelor of Science in Computer Science"],
            "institutions": [],
            "years": ["2020"],
            "education_level": "bachelor"
        },
        "experience": {
            "job_titles": ["Python Developer", "Junior Developer"],
            "companies": ["TechCompany", "StartupXYZ"],
            "durations": ["2021 - Present", "2020 - 2021"],
            "total_years_estimated": 0.0
        }
    },
    "job_requirements": {
        "experience": {"years": 3, "levels": []},
        "education": {"level": "bachelor", "fields": []},
        "skills": ["docker", "postgresql", "aws", "django", "fastapi", "python"]
    }
}
```

---

## How to Use

### Installation

No installation needed - uses Python standard library only!

Set PYTHONPATH:
```bash
export PYTHONPATH=/home/engine/project/src
```

### Basic Usage

```python
from app.nlp.scorer import calculate_match_score

result = calculate_match_score(job_description, resume_text)

# Get overall score (0-100%)
print(f"Match: {result['overall_score_percent']}%")

# Get detailed explanation
print(f"Explanation: {result['explanation']}")

# Get component scores
print(f"Skills: {result['component_scores']['skills_match']:.0%}")
print(f"Experience: {result['component_scores']['experience_match']:.0%}")
print(f"Education: {result['component_scores']['education_match']:.0%}")
```

### Run Examples

```bash
# Full demonstration with 2 candidates
PYTHONPATH=/home/engine/project/src python examples/resume_screening_example.py

# Simple example showing input/output
PYTHONPATH=/home/engine/project/src python examples/simple_example.py

# Quick test
PYTHONPATH=/home/engine/project/src python test_nlp.py
```

---

## File Structure

```
src/app/nlp/
├── __init__.py              # Main exports
├── skill_extractor.py       # Extract 80+ skills
├── education_extractor.py   # Extract degrees, level
├── experience_extractor.py  # Extract jobs, companies
└── scorer.py               # Calculate match scores

examples/
├── resume_screening_example.py  # Full demo (2 resumes)
├── simple_example.py            # Clear input/output demo
└── README.md

docs/
└── RESUME_SCREENING_NLP.md      # Complete documentation

test_nlp.py                     # Quick test script
```

---

## Key Features

### Skill Extraction (80+ skills)
- Languages: Python, Java, JavaScript, C++, Go, Rust, SQL
- Frameworks: Django, Flask, FastAPI, React, Spring, Rails
- Cloud/DevOps: AWS, Azure, Docker, Kubernetes, Jenkins
- Data: Pandas, NumPy, TensorFlow, PyTorch, scikit-learn
- Soft skills: Leadership, communication, teamwork, etc.

### Education Levels
Unknown → Diploma → Associate → Bachelor → Master → Doctorate

### Scoring Weights
- Skills Match: 50% - Required skills found in resume
- Experience Match: 30% - Years of experience + seniority
- Education Match: 15% - Degree level and field
- Keyword Overlap: 5% - General language similarity

---

## What It Does

1. **Parses resume text** using regex patterns
2. **Extracts information** - skills, education, experience
3. **Analyzes job description** - identifies requirements
4. **Calculates match** - weighted score based on fit
5. **Generates explanation** - human-readable feedback

---

## Limitations

- Works with text (PDF parsing in progress)
- Uses keyword matching (not full ML/NLP)
- Best with well-formatted resumes
- English language only currently

---

## Future Enhancements

- [ ] PDF parsing support
- [ ] Named Entity Recognition (NER)
- [ ] Semantic skill matching (embeddings)
- [ ] Multi-language support
- [ ] Export to JSON/CSV
- [ ] Batch processing

---

## Running Right Now

```bash
# Set path and run example
export PYTHONPATH=/home/engine/project/src
python examples/simple_example.py
```

Output shows:
- Overall match score (68%)
- Component breakdown (skills, experience, education, keywords)
- Explanation of why score was calculated
- Extracted resume data
- Identified job requirements
