"""Calculate match scores between resume and job description."""

from __future__ import annotations

import re
from collections import Counter
from typing import Final

from app.nlp.education_extractor import extract_education
from app.nlp.experience_extractor import extract_experience
from app.nlp.skill_extractor import extract_skills

# Weights for different scoring components
_WEIGHTS: Final = {
    "skills_match": 0.50,      # 50% weight on skill matching
    "experience_match": 0.30,  # 30% weight on experience level
    "education_match": 0.15,  # 15% weight on education level
    "keyword_overlap": 0.05,  # 5% weight on general keyword overlap
}


# Education level hierarchy (higher number = higher level)
_EDUCATION_LEVELS: Final = {
    "unknown": 0,
    "diploma": 1,
    "associate": 2,
    "bachelor": 3,
    "master": 4,
    "doctorate": 5,
}


def _tokenize(text: str) -> list[str]:
    """Simple tokenization."""
    return [t.lower() for t in re.findall(r"[a-zA-Z0-9]+", text)]


def _extract_required_experience(job_description: str) -> dict:
    """Extract required experience years and level from job description."""
    result = {"years": 0, "levels": []}
    
    # Look for experience requirements
    year_patterns = [
        r"(\d+)\+?\s*years?\s*(?:of\s+)?experience",
        r"(\d+)\s*-\s*(\d+)\s*years?\s*(?:of\s+)?experience",
    ]
    
    for pattern in year_patterns:
        matches = re.findall(pattern, job_description, re.IGNORECASE)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    # For ranges like "3-5 years", use the upper bound
                    result["years"] = max(result["years"], int(match[-1]))
                else:
                    result["years"] = max(result["years"], int(match))
    
    # Look for level keywords
    level_keywords = ["junior", "mid", "senior", "lead", "principal", "architect"]
    for level in level_keywords:
        if re.search(rf"\b{level}\b", job_description, re.IGNORECASE):
            result["levels"].append(level.lower())
    
    return result


def _extract_required_education(job_description: str) -> dict:
    """Extract education requirements from job description."""
    result = {"level": None, "fields": []}
    
    # Look for education level requirements
    level_patterns = [
        r"(?:phd|doctorate|doctor)\s*(?:degree)?",
        r"(?:master['']s?|m\.sc|m\.a|msc|ma)\s*(?:degree)?",
        r"(?:bachelor['']s?|b\.sc|b\.a|bsc|ba)\s*(?:degree)?",
        r"(?:associate['']s?)\s*(?:degree)?",
    ]
    
    for level, pattern in [
        ("doctorate", level_patterns[0]),
        ("master", level_patterns[1]),
        ("bachelor", level_patterns[2]),
        ("associate", level_patterns[3]),
    ]:
        if re.search(pattern, job_description, re.IGNORECASE):
            result["level"] = level
            break
    
    # Look for field of study requirements
    field_keywords = [
        "computer science", "data science", "software engineering",
        "information technology", "mathematics", "statistics",
        "business", "economics", "engineering",
    ]
    
    for field in field_keywords:
        if re.search(rf"{field}", job_description, re.IGNORECASE):
            result["fields"].append(field.lower())
    
    return result


def _score_skills_match(jd_skills: list[str], resume_skills: list[str]) -> float:
    """
    Calculate skill match score.
    
    Returns a score between 0.0 and 1.0.
    """
    if not jd_skills:
        return 0.0
    
    jd_set = set(skill.lower() for skill in jd_skills)
    resume_set = set(skill.lower() for skill in resume_skills)
    
    # Calculate precision, recall, and F1
    intersection = jd_set & resume_set
    
    if not jd_set:
        return 0.0
    
    recall = len(intersection) / len(jd_set)
    
    # If resume has no skills at all, score is very low
    if not resume_set:
        return 0.0
    
    # Weight towards recall (how many required skills the candidate has)
    return recall


def _score_experience_match(jd_requirements: dict, resume_experience: dict) -> float:
    """
    Calculate experience match score.
    
    Returns a score between 0.0 and 1.0.
    """
    required_years = jd_requirements["years"]
    required_levels = jd_requirements["levels"]
    resume_years = resume_experience.get("total_years_estimated", 0)
    
    score = 0.0
    
    # Check years of experience
    if required_years > 0:
        if resume_years >= required_years:
            score += 1.0
        elif resume_years >= required_years * 0.75:
            score += 0.75
        elif resume_years >= required_years * 0.5:
            score += 0.5
        elif resume_years > 0:
            score += 0.25
    else:
        # No specific requirement, give partial credit for having experience
        score += 0.5 if resume_years > 0 else 0.0
    
    # Check level match (simplified)
    if required_levels:
        # Extract levels from resume job titles
        resume_titles = " ".join(resume_experience.get("job_titles", [])).lower()
        
        for req_level in required_levels:
            if req_level in resume_titles:
                score += 0.2
                break
    
    return min(score, 1.0)


def _score_education_match(jd_requirements: dict, resume_education: dict) -> float:
    """
    Calculate education match score.
    
    Returns a score between 0.0 and 1.0.
    """
    required_level = jd_requirements["level"]
    required_fields = jd_requirements["fields"]
    resume_level = resume_education.get("education_level", "unknown")
    
    score = 0.0
    
    # Check education level
    if required_level:
        required_level_num = _EDUCATION_LEVELS.get(required_level, 0)
        resume_level_num = _EDUCATION_LEVELS.get(resume_level, 0)
        
        if resume_level_num >= required_level_num:
            score += 1.0
        elif resume_level_num >= required_level_num - 1:
            score += 0.5
    else:
        # No specific requirement, give partial credit for having any degree
        if resume_level in ["bachelor", "master", "doctorate"]:
            score += 0.5
        elif resume_level in ["associate", "diploma"]:
            score += 0.3
    
    # Check field of study
    if required_fields:
        resume_fields = " ".join(resume_education.get("degrees", [])).lower()
        for req_field in required_fields:
            if req_field in resume_fields:
                score += 0.3
                break
    
    return min(score, 1.0)


def _score_keyword_overlap(jd_text: str, resume_text: str) -> float:
    """
    Calculate general keyword overlap.
    
    Returns a score between 0.0 and 1.0.
    """
    jd_tokens = Counter(_tokenize(jd_text))
    resume_tokens = Counter(_tokenize(resume_text))
    
    # Filter out very common words (basic stoplist)
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "as", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "can", "this", "that", "these", "those",
        "i", "you", "he", "she", "it", "we", "they", "my", "your", "our", "their",
        "work", "working", "team", "role", "position", "job", "candidate",
    }
    
    # Remove stop words from consideration
    jd_tokens = Counter({k: v for k, v in jd_tokens.items() if k not in stop_words and len(k) > 2})
    
    if not jd_tokens:
        return 0.0
    
    # Calculate overlap based on weighted importance
    overlap_sum = 0
    total_sum = 0
    
    for token, jd_count in jd_tokens.items():
        total_sum += jd_count
        if token in resume_tokens:
            overlap_sum += min(jd_count, resume_tokens[token])
    
    if total_sum == 0:
        return 0.0
    
    return overlap_sum / total_sum


def _generate_explanation(
    skills_match: float,
    experience_match: float,
    education_match: float,
    jd_skills: list[str],
    resume_skills: list[str],
    jd_requirements: dict,
    resume_data: dict,
) -> str:
    """Generate a human-readable explanation of the score."""
    parts = []
    
    # Skills explanation
    jd_set = set(skill.lower() for skill in jd_skills)
    resume_set = set(skill.lower() for skill in resume_skills)
    matched_skills = jd_set & resume_set
    missed_skills = jd_set - resume_set
    
    if matched_skills:
        parts.append(f"Matched skills: {', '.join(sorted(matched_skills))}")
    if missed_skills:
        parts.append(f"Missing required skills: {', '.join(sorted(missed_skills))}")
    
    # Experience explanation
    req_years = jd_requirements["years"]
    resume_years = resume_data["experience"].get("total_years_estimated", 0)
    if req_years > 0:
        if resume_years >= req_years:
            parts.append(f"Meets experience requirement ({req_years}+ years)")
        else:
            parts.append(f"Has {resume_years} years experience (required: {req_years}+)")
    
    # Education explanation
    req_edu_level = jd_requirements.get("level")
    resume_edu_level = resume_data["education"].get("education_level")
    if req_edu_level:
        if resume_edu_level == req_edu_level:
            parts.append(f"Meets education requirement ({req_edu_level} degree)")
        elif resume_edu_level in ["master", "doctorate"] and req_edu_level == "bachelor":
            parts.append(f"Exceeds education requirement ({resume_edu_level} degree)")
        elif resume_edu_level:
            parts.append(f"Has {resume_edu_level} degree (required: {req_edu_level})")
        else:
            parts.append(f"Education level unclear (required: {req_edu_level})")
    
    # Summary score
    overall = (skills_match * 0.5 + experience_match * 0.3 + 
               education_match * 0.15 + 0.05)  # Simplified
    overall_score = int(overall * 100)
    parts.insert(0, f"Overall Match Score: {overall_score}%")
    
    return ". ".join(parts)


def calculate_match_score(job_description: str, resume_text: str) -> dict:
    """
    Calculate a comprehensive match score between a resume and job description.
    
    Args:
        job_description: The job description text
        resume_text: The resume text
        
    Returns:
        Dictionary with:
        {
            "overall_score": float (0.0 to 1.0),
            "overall_score_percent": int (0 to 100),
            "component_scores": {
                "skills_match": float,
                "experience_match": float,
                "education_match": float,
                "keyword_overlap": float,
            },
            "explanation": str,
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
    """
    # Extract data from both sources
    resume_skills = extract_skills(resume_text)
    resume_education = extract_education(resume_text)
    resume_experience = extract_experience(resume_text)
    
    # Extract requirements from job description
    jd_requirements = {
        "experience": _extract_required_experience(job_description),
        "education": _extract_required_education(job_description),
        "skills": extract_skills(job_description)["technical"],
    }
    
    # Calculate component scores
    skills_match = _score_skills_match(
        jd_requirements["skills"],
        resume_skills["technical"],
    )
    
    experience_match = _score_experience_match(
        jd_requirements["experience"],
        resume_experience,
    )
    
    education_match = _score_education_match(
        jd_requirements["education"],
        resume_education,
    )
    
    keyword_overlap = _score_keyword_overlap(job_description, resume_text)
    
    # Calculate weighted overall score
    overall_score = (
        skills_match * _WEIGHTS["skills_match"]
        + experience_match * _WEIGHTS["experience_match"]
        + education_match * _WEIGHTS["education_match"]
        + keyword_overlap * _WEIGHTS["keyword_overlap"]
    )
    
    # Generate explanation
    explanation = _generate_explanation(
        skills_match=skills_match,
        experience_match=experience_match,
        education_match=education_match,
        jd_skills=jd_requirements["skills"],
        resume_skills=resume_skills["technical"],
        jd_requirements=jd_requirements["experience"],
        resume_data={
            "experience": resume_experience,
            "education": resume_education,
        },
    )
    
    return {
        "overall_score": round(overall_score, 3),
        "overall_score_percent": int(overall_score * 100),
        "component_scores": {
            "skills_match": round(skills_match, 3),
            "experience_match": round(experience_match, 3),
            "education_match": round(education_match, 3),
            "keyword_overlap": round(keyword_overlap, 3),
        },
        "explanation": explanation,
        "resume_data": {
            "skills": resume_skills,
            "education": resume_education,
            "experience": resume_experience,
        },
        "job_requirements": jd_requirements,
    }
