#!/usr/bin/env python3
"""
Simple Resume Screening Example
Shows input and output for the NLP module.
"""

import sys
sys.path.insert(0, '/home/engine/project/src')

from app.nlp.scorer import calculate_match_score

# INPUT: Job Description
JOB_DESCRIPTION = """
Python Developer - 3+ years experience

Requirements:
• Python, Django, or FastAPI
• Experience with AWS or Docker
• Knowledge of PostgreSQL
• Bachelor's degree in Computer Science or related field
"""

# INPUT: Resume
RESUME_TEXT = """
John Doe
Python Developer

WORK EXPERIENCE
Python Developer | TechCompany | 2021 - Present
• Developed REST APIs using FastAPI and Django
• Deployed applications to AWS EC2 using Docker
• Designed PostgreSQL database schemas
• Built automated CI/CD pipelines

Junior Developer | StartupXYZ | 2020 - 2021
• Python backend development
• MongoDB database management

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2020

SKILLS
Python, Django, FastAPI, AWS, Docker, PostgreSQL, MongoDB, Git
"""

# Run the screening
result = calculate_match_score(JOB_DESCRIPTION, RESUME_TEXT)

# OUTPUT
print("=" * 70)
print("RESUME SCREENING RESULT")
print("=" * 70)

print("\n📊 OVERALL SCORE")
print(f"   {result['overall_score_percent']}% (0-100)")

print("\n📈 COMPONENT SCORES")
for component, score in result['component_scores'].items():
    bar = '█' * int(score * 30)
    print(f"   {component:20s} {score:.0%}  {bar}")

print("\n📋 EXPLANATION")
print(f"   {result['explanation']}")

print("\n🎯 RESUME DATA")
print(f"   Technical Skills: {result['resume_data']['skills']['technical']}")
print(f"   Education Level:  {result['resume_data']['education']['education_level']}")
print(f"   Experience Years: {result['resume_data']['experience']['total_years_estimated']}")

print("\n📝 JOB REQUIREMENTS")
print(f"   Required Skills:  {result['job_requirements']['skills']}")
print(f"   Required Level:   {result['job_requirements']['experience']}")
print(f"   Required Edu:     {result['job_requirements']['education']['level']}")

print("\n" + "=" * 70)
