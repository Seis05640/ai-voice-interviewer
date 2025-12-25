"""Extract skills from resume text using NLP techniques."""

from __future__ import annotations

import re
from collections import Counter
from typing import Final

# Common technical skills - can be expanded
_COMMON_TECH_SKILLS: Final = {
    # Programming languages
    "python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "swift",
    "kotlin", "php", "scala", "typescript", "r", "sql", "html", "css",
    # Frameworks & libraries
    "django", "flask", "fastapi", "spring", "react", "angular", "vue", "nodejs",
    "express", "rails", "numpy", "pandas", "tensorflow", "pytorch", "keras",
    "scikit-learn", "django", "laravel", "asp.net", "jquery", "bootstrap",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "ci/cd",
    "terraform", "ansible", "linux", "bash", "shell", "nginx", "apache",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "oracle", "elasticsearch",
    "cassandra", "dynamodb", "neo4j", "firebase",
    # Data science & ML
    "machine learning", "deep learning", "nlp", "data science", "data analysis",
    "statistics", "matplotlib", "seaborn", "tableau", "power bi", "spark", "hadoop",
    "jupyter", "rmarkdown", "sas", "spss",
    # Other technical skills
    "api", "rest", "graphql", "microservices", "agile", "scrum", "kanban",
    "tdd", "bdd", "unit testing", "integration testing", "gitflow", "design patterns",
}

# Soft skills
_SOFT_SKILLS: Final = {
    "leadership", "communication", "teamwork", "problem solving", "critical thinking",
    "adaptability", "time management", "collaboration", "analytical", "creativity",
    "project management", "public speaking", "negotiation", "decision making",
    "strategic thinking", "mentoring", "coaching", "interpersonal", "organizational",
}

# Skill patterns to detect
_SKILL_PATTERNS: Final = [
    # Programming with versions (e.g., Python 3.8, Java 11)
    r"python\s*\d+(\.\d+)*",
    r"java\s*\d+(\.\d+)*",
    r"node(?:js)?\s*\d+(\.\d+)*",
    # Framework versions (e.g., React 18, Django 4)
    r"react\s*\d+(\.\d+)*",
    r"angular\s*\d+(\.\d+)*",
    r"django\s*\d+(\.\d+)*",
    # Certifications
    r"aws\s*certified",
    r"azure\s*certified",
    r"gcp\s*certified",
    r"pmp",
    r"prince2",
    r"scrum\s*master",
    r"agile\s*certified",
]


def _find_skills_by_pattern(text: str, patterns: list[str]) -> set[str]:
    """Find skills using regex patterns."""
    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # For simple patterns, the match is the skill itself
            found.update(m.lower() for m in matches)
    return found


def _extract_keyword_skills(text: str, skill_dict: set[str]) -> list[str]:
    """Extract skills from text using keyword matching."""
    text_lower = text.lower()
    found = []
    
    for skill in skill_dict:
        # Match whole words only
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    
    return found


def extract_skills(text: str) -> dict:
    """
    Extract skills from resume text.
    
    Args:
        text: Resume text content
        
    Returns:
        Dictionary with extracted skills:
        {
            "technical": list of technical skills,
            "soft": list of soft skills,
            "total_count": total number of unique skills found
        }
    """
    # Extract using keyword matching
    tech_skills = _extract_keyword_skills(text, _COMMON_TECH_SKILLS)
    soft_skills = _extract_keyword_skills(text, _SOFT_SKILLS)
    
    # Find skills using patterns
    pattern_skills = _find_skills_by_pattern(text, _SKILL_PATTERNS)
    
    # Merge pattern skills into tech skills (avoiding duplicates)
    tech_skills.extend(s for s in pattern_skills if s not in tech_skills)
    
    # Remove duplicates while preserving order
    tech_skills = list(dict.fromkeys(tech_skills))
    soft_skills = list(dict.fromkeys(soft_skills))
    
    return {
        "technical": tech_skills,
        "soft": soft_skills,
        "total_count": len(tech_skills) + len(soft_skills),
    }
