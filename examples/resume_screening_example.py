"""
Example usage of the resume screening NLP module.

This script demonstrates how to use the NLP module to:
1. Extract skills, education, and experience from resumes
2. Compare against job descriptions
3. Calculate match scores with explanations
"""

from app.nlp import extract_skills, extract_education, extract_experience
from app.nlp.scorer import calculate_match_score


# Example 1: Strong match
JOB_DESCRIPTION_1 = """
Senior Python Developer

We are looking for a Senior Python Developer with 5+ years of experience to join our growing team.

Requirements:
- 5+ years of Python development experience
- Strong experience with Django, Flask, or FastAPI
- Experience with AWS cloud services
- Knowledge of PostgreSQL and MongoDB
- Experience with Docker and Kubernetes
- Bachelor's degree in Computer Science or related field
- Experience with machine learning or data science is a plus

Responsibilities:
- Design and implement scalable backend services
- Lead technical initiatives and mentor junior developers
- Collaborate with cross-functional teams
- Write clean, maintainable code
"""

RESUME_1 = """
John Smith
Senior Python Developer
Email: john.smith@email.com
Phone: (555) 123-4567

Experience
----------
Senior Python Developer | TechCorp Inc. | 2019 - Present
- Developed RESTful APIs using FastAPI and Django
- Led a team of 5 developers on a microservices migration project
- Implemented CI/CD pipelines using Jenkins and Docker
- Deployed applications to AWS EC2 and ECS
- Optimized database queries reducing response time by 40%

Python Developer | DataSolutions LLC | 2017 - 2019
- Built data processing pipelines using Python and Pandas
- Developed web applications using Flask
- Worked with PostgreSQL and MongoDB databases
- Implemented unit tests using pytest

Education
---------
Bachelor of Science in Computer Science
State University, 2017

Skills
-------
- Languages: Python, JavaScript, SQL, HTML, CSS
- Frameworks: Django, Flask, FastAPI, React
- Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Git
- Databases: PostgreSQL, MongoDB, Redis
- Data Science: Pandas, NumPy, scikit-learn
"""


# Example 2: Weak match
RESUME_2 = """
Jane Doe
Marketing Manager
Email: jane.doe@email.com

Experience
----------
Marketing Manager | RetailCo | 2020 - Present
- Developed marketing campaigns for retail products
- Managed social media presence
- Analyzed customer data and created reports

Sales Associate | ShopMart | 2018 - 2020
- Assisted customers with purchases
- Maintained inventory records

Education
---------
Bachelor of Arts in Marketing
City College, 2018

Skills
-------
- Marketing strategy
- Social media management
- Microsoft Office
- Customer service
"""


def demonstrate_extraction():
    """Demonstrate the extraction functions."""
    print("=" * 80)
    print("DEMONSTRATING EXTRACTION FUNCTIONS")
    print("=" * 80)
    
    # Extract from Resume 1
    print("\n--- EXTRACTING FROM RESUME 1 (John Smith) ---\n")
    
    skills = extract_skills(RESUME_1)
    print(f"Technical Skills ({skills['total_count']} total):")
    print(f"  {skills['technical']}")
    print(f"\nSoft Skills:")
    print(f"  {skills['soft']}")
    
    education = extract_education(RESUME_1)
    print(f"\nEducation:")
    print(f"  Degrees: {education['degrees']}")
    print(f"  Institutions: {education['institutions']}")
    print(f"  Level: {education['education_level']}")
    
    experience = extract_experience(RESUME_1)
    print(f"\nExperience:")
    print(f"  Job Titles: {experience['job_titles']}")
    print(f"  Companies: {experience['companies']}")
    print(f"  Estimated Years: {experience['total_years_estimated']}")
    print(f"  Achievements (first 3): {experience['achievements'][:3]}")


def demonstrate_scoring():
    """Demonstrate the scoring function."""
    print("\n\n" + "=" * 80)
    print("DEMONSTRATING SCORING FUNCTION")
    print("=" * 80)
    
    # Score Resume 1 (Strong Match)
    print("\n--- SCORING RESUME 1 (John Smith) vs Job Description ---\n")
    
    result_1 = calculate_match_score(JOB_DESCRIPTION_1, RESUME_1)
    
    print(f"Overall Score: {result_1['overall_score_percent']}%")
    print(f"\nComponent Scores:")
    for component, score in result_1['component_scores'].items():
        print(f"  {component}: {score:.2%}")
    
    print(f"\nExplanation:")
    print(f"  {result_1['explanation']}")
    
    # Score Resume 2 (Weak Match)
    print("\n\n--- SCORING RESUME 2 (Jane Doe) vs Job Description ---\n")
    
    result_2 = calculate_match_score(JOB_DESCRIPTION_1, RESUME_2)
    
    print(f"Overall Score: {result_2['overall_score_percent']}%")
    print(f"\nComponent Scores:")
    for component, score in result_2['component_scores'].items():
        print(f"  {component}: {score:.2%}")
    
    print(f"\nExplanation:")
    print(f"  {result_2['explanation']}")


def demonstrate_simple_usage():
    """Demonstrate simple, minimal usage."""
    print("\n\n" + "=" * 80)
    print("SIMPLE USAGE EXAMPLE")
    print("=" * 80)
    
    print("\n# Simple usage:")
    print("from app.nlp.scorer import calculate_match_score")
    print("")
    print("result = calculate_match_score(job_description, resume_text)")
    print("print(f'Match Score: {result[\"overall_score_percent\"]}%')")
    print("print(f'Explanation: {result[\"explanation\"]}')")
    print("")
    
    # Actually run it
    result = calculate_match_score(JOB_DESCRIPTION_1, RESUME_1)
    print(f"\nResult:")
    print(f"  Match Score: {result['overall_score_percent']}%")
    print(f"  Explanation: {result['explanation']}")


def main():
    """Run all demonstrations."""
    demonstrate_extraction()
    demonstrate_scoring()
    demonstrate_simple_usage()
    
    print("\n\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nThe resume screening module provides:")
    print("1. Extract skills (technical and soft)")
    print("2. Extract education (degrees, institutions, level)")
    print("3. Extract experience (titles, companies, years, achievements)")
    print("4. Calculate match scores with detailed explanations")
    print("\nAll using only Python standard libraries and regex!")
    print("=" * 80)


if __name__ == "__main__":
    main()
