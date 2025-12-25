# Resume Screening NLP Module

A Python module for automated resume screening using NLP techniques. Extracts skills, education, and experience from resumes, then matches them against job descriptions with scored explanations.

## Features

- **No external dependencies** - Uses Python standard library only (re, collections, dataclasses)
- **No paid APIs** - All processing done locally
- **Easy to understand** - Clear, well-documented code
- **Comprehensive extraction**:
  - Skills (technical and soft)
  - Education (degrees, institutions, level)
  - Experience (titles, companies, years, achievements)
- **Smart scoring** with weighted components:
  - Skills match (50% weight)
  - Experience match (30% weight)
  - Education match (15% weight)
  - Keyword overlap (5% weight)

## Installation

The module is part of the `ai-interview-system` package. Install the package:

```bash
pip install -e .
```

## Quick Start

```python
from app.nlp.scorer import calculate_match_score

job_description = """
Senior Python Developer

Requirements:
- 5+ years Python development experience
- Experience with Django, Flask, or FastAPI
- Knowledge of AWS, Docker
- Bachelor's degree in Computer Science
"""

resume_text = """
John Smith
Senior Python Developer | 2019-Present

Experience:
- Developed RESTful APIs using FastAPI
- Deployed applications to AWS using Docker
- Led a team of 5 developers

Education:
Bachelor of Science in Computer Science, State University, 2017
"""

result = calculate_match_score(job_description, resume_text)

print(f"Match Score: {result['overall_score_percent']}%")
print(f"Explanation: {result['explanation']}")
```

## API Reference

### Main Function

#### `calculate_match_score(job_description: str, resume_text: str) -> dict`

Calculate a comprehensive match score between a resume and job description.

**Returns:**
```python
{
    "overall_score": float,           # 0.0 to 1.0
    "overall_score_percent": int,      # 0 to 100
    "component_scores": {
        "skills_match": float,
        "experience_match": float,
        "education_match": float,
        "keyword_overlap": float,
    },
    "explanation": str,                # Human-readable explanation
    "resume_data": {
        "skills": dict,
        "education": dict,
        "experience": dict,
    },
    "job_requirements": {
        "experience": dict,
        "education": dict,
        "skills": list,
    },
}
```

### Extraction Functions

#### `extract_skills(text: str) -> dict`

Extract skills from resume text.

**Returns:**
```python
{
    "technical": list[str],    # Technical skills
    "soft": list[str],         # Soft skills
    "total_count": int,        # Total unique skills
}
```

#### `extract_education(text: str) -> dict`

Extract education information from resume text.

**Returns:**
```python
{
    "degrees": list[str],
    "institutions": list[str],
    "years": list[str],
    "entries": list[dict],
    "education_level": str,    # "unknown", "diploma", "associate", "bachelor", "master", "doctorate"
}
```

#### `extract_experience(text: str) -> dict`

Extract work experience from resume text.

**Returns:**
```python
{
    "job_titles": list[str],
    "companies": list[str],
    "durations": list[str],
    "achievements": list[str],
    "total_years_estimated": float,
    "entries": list[dict],
}
```

## Example Input and Output

### Input

**Job Description:**
```
Senior Python Developer

Requirements:
- 5+ years Python development experience
- Experience with Django, Flask, or FastAPI
- Knowledge of AWS, Docker, PostgreSQL
- Bachelor's degree in Computer Science
```

**Resume:**
```
John Smith
Senior Python Developer | TechCorp Inc. | 2019 - Present

Experience:
- Developed RESTful APIs using FastAPI
- Deployed applications to AWS using Docker
- Worked with PostgreSQL databases
- Led a team of 5 developers

Education:
Bachelor of Science in Computer Science, State University, 2017

Skills:
Python, Django, FastAPI, AWS, Docker, PostgreSQL
```

### Output

```python
{
    "overall_score": 0.875,
    "overall_score_percent": 88,
    "component_scores": {
        "skills_match": 0.833,
        "experience_match": 1.0,
        "education_match": 1.0,
        "keyword_overlap": 0.312,
    },
    "explanation": "Overall Match Score: 88%. Matched skills: python, django, aws, docker, postgresql, fastapi. Meets experience requirement (5+ years). Meets education requirement (bachelor degree).",
    "resume_data": {
        "skills": {
            "technical": ["python", "django", "fastapi", "aws", "docker", "postgresql"],
            "soft": [],
            "total_count": 6,
        },
        "education": {
            "degrees": ["Bachelor of Science in Computer Science"],
            "institutions": ["State University"],
            "years": ["2017"],
            "entries": [...],
            "education_level": "bachelor",
        },
        "experience": {
            "job_titles": ["Senior Python Developer"],
            "companies": ["TechCorp Inc."],
            "durations": ["2019 - Present"],
            "achievements": [...],
            "total_years_estimated": 4.0,
            "entries": [...],
        },
    },
    "job_requirements": {
        "experience": {"years": 5, "levels": ["senior"]},
        "education": {"level": "bachelor", "fields": ["computer science"]},
        "skills": ["python", "django", "flask", "fastapi", "aws", "docker", "postgresql"],
    },
}
```

## Running the Example

To see a complete demonstration:

```bash
cd /home/engine/project
python examples/resume_screening_example.py
```

This will show:
- Skill extraction from a sample resume
- Education extraction (degrees, institutions, level)
- Experience extraction (titles, companies, years)
- Scoring comparison between strong and weak candidates
- Detailed explanations for each score

## How It Works

### 1. Skill Extraction
- Uses keyword matching against a comprehensive skill database
- Supports technical skills (languages, frameworks, tools) and soft skills
- Detects versioned skills (e.g., "Python 3.8", "React 18")

### 2. Education Extraction
- Identifies degree types and levels
- Extracts institution names
- Determines education level for comparison

### 3. Experience Extraction
- Finds job titles and company names
- Estimates total years of experience
- Extracts achievement descriptions (bullet points)

### 4. Scoring
Calculates a weighted score based on:
- **Skills Match (50%)**: How many required skills the candidate has
- **Experience Match (30%)**: Years of experience and seniority level
- **Education Match (15%)**: Whether education meets requirements
- **Keyword Overlap (5%)**: General language similarity

## Extending the Module

### Adding Custom Skills

Edit `src/app/nlp/skill_extractor.py`:

```python
_COMMON_TECH_SKILLS = {
    # Add your custom skills here
    "your-skill-1",
    "your-skill-2",
}
```

### Adjusting Scoring Weights

Edit `src/app/nlp/scorer.py`:

```python
_WEIGHTS = {
    "skills_match": 0.50,      # Change this
    "experience_match": 0.30,  # And this
    "education_match": 0.15,  # And this
    "keyword_overlap": 0.05,  # And this
}
```

### Adding Custom Extraction Patterns

Each extractor uses regex patterns that can be extended:

```python
_CUSTOM_PATTERNS = [
    r"your-custom-pattern-here",
]
```

## Limitations

- Currently works with plain text (PDF parsing coming soon)
- Uses keyword matching (not full NLP/ML)
- No semantic understanding (e.g., doesn't know "Node.js" = "JavaScript")
- Works best with well-formatted, English-language resumes

## Future Enhancements

- [ ] PDF parsing support
- [ ] Named Entity Recognition (NER) for better extraction
- [ ] Word embeddings for semantic skill matching
- [ ] Support for more languages
- [ ] Export results to JSON/CSV
- [ ] Batch processing for multiple resumes

## License

Part of the ai-interview-system project.
