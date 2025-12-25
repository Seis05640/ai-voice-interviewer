# Examples

This directory contains example scripts demonstrating the usage of the ai-interview-system modules.

## Running the Examples

Make sure the package is installed or set PYTHONPATH to the src directory:

```bash
# Option 1: Using PYTHONPATH
PYTHONPATH=/home/engine/project/src python examples/resume_screening_example.py

# Option 2: Install the package (in a virtual environment)
python3 -m venv venv
source venv/bin/activate
pip install -e .
python examples/resume_screening_example.py
```

## Available Examples

### `resume_screening_example.py`

Demonstrates the resume screening NLP module:

- **Extracting skills** from resume text (technical and soft skills)
- **Extracting education** (degrees, institutions, level)
- **Extracting experience** (titles, companies, years, achievements)
- **Calculating match scores** between resumes and job descriptions
- **Generating explanations** for match scores

Run it to see a complete demonstration with sample resumes (one strong match, one weak match).

Output includes:
- Extracted information (skills, education, experience)
- Component scores (skills, experience, education, keywords)
- Overall match score (0-100%)
- Human-readable explanation of the match
