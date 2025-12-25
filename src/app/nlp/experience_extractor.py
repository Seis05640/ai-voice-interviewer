"""Extract work experience information from resume text."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

# Common action verbs found in experience sections
_ACTION_VERBS: Final = {
    "developed", "designed", "implemented", "managed", "led", "created", "built",
    "deployed", "maintained", "improved", "optimized", "tested", "analyzed",
    "coordinated", "collaborated", "supervised", "trained", "mentored",
    "architected", "engineered", "programmed", "configured", "documented",
    "monitored", "automated", "streamlined", "launched", "delivered",
}

# Job title keywords
_TITLE_KEYWORDS: Final = {
    "engineer", "developer", "manager", "analyst", "director", "lead",
    "senior", "junior", "principal", "architect", "consultant", "specialist",
    "coordinator", "administrator", "officer", "assistant", "head", "chief",
}

# Company/organization indicators
_COMPANY_PATTERNS: Final = [
    r"[A-Z][A-Za-z\s]+(?:Inc|LLC|Corp|Ltd|Technologies|Solutions|Systems|Labs)",
    r"[A-Z][A-Za-z\s]+(?:Company|Group|Partners)",
]


@dataclass
class ExperienceEntry:
    """Represents a single work experience entry."""
    title: str | None
    company: str | None
    duration: str | None
    description: list[str]


# Regex patterns for experience extraction
_TITLE_PATTERNS: Final = [
    # Job titles like "Senior Software Engineer"
    r"(?:Senior|Junior|Principal|Lead|Staff)?\s*(?:Software|Full.?Stack|Backend|Frontend|Data|ML|DevOps|Cloud)?\s*(?:Engineer|Developer|Manager|Architect|Analyst|Consultant)",
    # Managerial roles
    r"(?:Engineering|Technical|Product|Project)\s+Manager",
    # Director/VP roles
    r"(?:Director|VP)\s+(?:of\s+)?(?:Engineering|Technology|Product|Operations)",
    # Other common titles
    r"(?:Data|ML|AI)\s+Scientist",
]

_DURATION_PATTERNS: Final = [
    # "January 2020 - Present" or "Jan 2020 - Present"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*-\s*(?:Present|Current|\d{4})",
    # "2020 - 2023" or "2020-Present"
    r"\d{4}\s*-\s*(?:Present|Current|\d{4})",
    # "3 years" or "2.5 years"
    r"\d+(?:\.\d+)?\s+years?",
    # "6 months"
    r"\d+\s+months?",
]

_BULLET_POINT_PATTERNS: Final = [
    r"•\s*[^\n]+",
    r"-\s*[^\n]+",
    r"·\s*[^\n]+",
    r"✓\s*[^\n]+",
]


def _extract_job_titles(text: str) -> list[str]:
    """Extract job titles from text."""
    titles = []
    
    for pattern in _TITLE_PATTERNS:
        matches = re.findall(pattern, text)
        titles.extend(matches)
    
    # Also look for lines that look like job titles
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        # Check if line contains title keywords and looks like a title
        if any(keyword.lower() in line.lower() for keyword in _TITLE_KEYWORDS):
            # Exclude lines that are too long (likely descriptions)
            if len(line.split()) <= 5:
                titles.append(line)
    
    return list(dict.fromkeys(titles))


def _extract_companies(text: str) -> list[str]:
    """Extract company names from text."""
    companies = []
    
    for pattern in _COMPANY_PATTERNS:
        matches = re.findall(pattern, text)
        companies.extend(matches)
    
    return list(dict.fromkeys(companies))


def _extract_durations(text: str) -> list[str]:
    """Extract work durations (dates, ranges, or time periods)."""
    durations = []
    
    for pattern in _DURATION_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        durations.extend(matches)
    
    return list(dict.fromkeys(durations))


def _extract_bullets(text: str) -> list[str]:
    """Extract bullet points (achievement descriptions)."""
    bullets = []
    
    for pattern in _BULLET_POINT_PATTERNS:
        matches = re.findall(pattern, text)
        # Clean up bullet points
        cleaned = [re.sub(r"^[•\-·✓]\s*", "", m).strip() for m in matches]
        bullets.extend(cleaned)
    
    return bullets


def _extract_total_experience_months(text: str) -> int:
    """Estimate total work experience in months."""
    months = 0
    
    # Look for explicit time period mentions
    year_matches = re.findall(r"(\d+)\s+years?", text, re.IGNORECASE)
    for match in year_matches:
        months += int(match) * 12
    
    month_matches = re.findall(r"(\d+)\s+months?", text, re.IGNORECASE)
    for match in month_matches:
        months += int(match)
    
    return months


def extract_experience(text: str) -> dict:
    """
    Extract work experience information from resume text.
    
    Args:
        text: Resume text content
        
    Returns:
        Dictionary with extracted experience:
        {
            "job_titles": list of job titles,
            "companies": list of company names,
            "durations": list of duration strings,
            "achievements": list of bullet points/descriptions,
            "total_years_estimated": estimated total years of experience,
            "entries": list of structured ExperienceEntry objects
        }
    """
    job_titles = _extract_job_titles(text)
    companies = _extract_companies(text)
    durations = _extract_durations(text)
    achievements = _extract_bullets(text)
    
    # Create structured entries
    entries = []
    max_len = max(len(job_titles), len(companies), len(durations))
    
    for i in range(max_len):
        entry = ExperienceEntry(
            title=job_titles[i] if i < len(job_titles) else None,
            company=companies[i] if i < len(companies) else None,
            duration=durations[i] if i < len(durations) else None,
            # Distribute achievements across entries (simplified)
            description=[],
        )
        entries.append({"title": entry.title, "company": entry.company,
                       "duration": entry.duration, "description": entry.description})
    
    # Calculate total experience
    total_months = _extract_total_experience_months(text)
    total_years = round(total_months / 12, 1)
    
    return {
        "job_titles": job_titles,
        "companies": companies,
        "durations": durations,
        "achievements": achievements,
        "total_years_estimated": total_years,
        "entries": entries,
    }
