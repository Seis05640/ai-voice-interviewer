"""Extract education information from resume text."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

# Degree patterns
_DEGREE_KEYWORDS: Final = {
    "bachelor", "master", "phd", "doctorate", "doctor", "mba", "associate",
    "b.sc", "m.sc", "b.a", "m.a", "bs", "ms", "ba", "ma", "diploma",
    "certificate", "certification",
}

# Field of study keywords
_FIELD_KEYWORDS: Final = {
    "computer science", "data science", "software engineering", "information technology",
    "mathematics", "statistics", "physics", "chemistry", "biology",
    "business", "economics", "finance", "marketing", "management",
    "engineering", "electrical engineering", "mechanical engineering",
    "psychology", "sociology", "philosophy", "literature",
    "law", "medicine", "nursing", "education",
}

# Institution type indicators
_INSTITUTION_KEYWORDS: Final = {
    "university", "college", "institute", "institute of technology",
    "school of", "polytechnic",
}


@dataclass
class EducationEntry:
    """Represents a single education entry."""
    degree: str
    field: str | None
    institution: str | None
    year: str | None


# Regex patterns for education extraction
_DEGREE_PATTERNS: Final = [
    # "Bachelor of Science in Computer Science"
    r"(?:Bachelor|Master|Doctor|PhD)\s+(?:of\s+)?(?:Science|Arts|Engineering|Business|Fine Arts)\s+(?:in\s+)?[^\n,]+",
    # "B.Sc. Computer Science" or "MSc Data Science"
    r"(?:B\.Sc|M\.Sc|B\.A|M\.A|BSc|MSc|BS|MS|BA|MA|MBA|PhD)\.?\s+(?:in\s+)?[^\n,]+",
    # "Bachelor degree in..."
    r"(?:Bachelor|Master|Doctorate)\s+degree\s+(?:in\s+)?[^\n,]+",
]

_INSTITUTION_PATTERNS: Final = [
    # "[Institution Name] University"
    r"[A-Z][^\n]*?(?:University|College|Institute|Institute of Technology|Polytechnic)",
    # "University of..."
    r"University\s+(?:of|at)\s+[^\n,]+",
    # "School of..."
    r"School\s+of\s+[^\n,]+",
]

_YEAR_PATTERNS: Final = [
    r"\b(19|20)\d{2}\b",  # Years 1900-2099
    r"\b(19|20)\d{2}\s*-\s*(?:19|20)?\d{2}\b",  # Year ranges like 2015-2019
]


def _extract_degree(text: str) -> list[str]:
    """Extract degree information from text."""
    degrees = []
    
    # Try pattern matching first
    for pattern in _DEGREE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        degrees.extend(matches)
    
    # Also look for degree keywords with nearby field
    for keyword in _DEGREE_KEYWORDS:
        # Look for degree keyword followed by field of study
        pattern = rf"\b{keyword}\b[^\n]{{0,50}}"
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Check if it contains field keywords
            for field in _FIELD_KEYWORDS:
                if field.lower() in match.lower():
                    degrees.append(match.strip())
                    break
    
    return list(dict.fromkeys(degrees))  # Remove duplicates


def _extract_institution(text: str) -> list[str]:
    """Extract institution names from text."""
    institutions = []
    
    for pattern in _INSTITUTION_PATTERNS:
        matches = re.findall(pattern, text)
        institutions.extend(matches)
    
    return list(dict.fromkeys(institutions))


def _extract_years(text: str) -> list[str]:
    """Extract graduation years or year ranges."""
    years = []
    
    for pattern in _YEAR_PATTERNS:
        matches = re.findall(pattern, text)
        years.extend(matches)
    
    return list(dict.fromkeys(years))


def extract_education(text: str) -> dict:
    """
    Extract education information from resume text.
    
    Args:
        text: Resume text content
        
    Returns:
        Dictionary with extracted education:
        {
            "degrees": list of degree strings,
            "institutions": list of institution names,
            "years": list of years/graduation years,
            "entries": list of EducationEntry objects,
            "education_level": highest education level detected
        }
    """
    degrees = _extract_degree(text)
    institutions = _extract_institution(text)
    years = _extract_years(text)
    
    # Create structured entries
    entries = []
    if degrees:
        # If we have degree info, try to create entries
        # This is a simplified approach - in production, you'd use more sophisticated NLP
        for i, degree in enumerate(degrees):
            entry = EducationEntry(
                degree=degree,
                field=_guess_field_of_study(degree),
                institution=institutions[i] if i < len(institutions) else None,
                year=years[i] if i < len(years) else None,
            )
            entries.append(entry)
    
    # Determine education level
    education_level = _determine_education_level(degrees)
    
    return {
        "degrees": degrees,
        "institutions": institutions,
        "years": years,
        "entries": [{"degree": e.degree, "field": e.field, 
                    "institution": e.institution, "year": e.year} 
                   for e in entries],
        "education_level": education_level,
    }


def _guess_field_of_study(degree: str) -> str | None:
    """Guess field of study from degree string."""
    degree_lower = degree.lower()
    for field in _FIELD_KEYWORDS:
        if field in degree_lower:
            return field
    return None


def _determine_education_level(degrees: list[str]) -> str:
    """Determine highest education level from degrees list."""
    if not degrees:
        return "unknown"
    
    degree_str = " ".join(degrees).lower()
    
    if any(keyword in degree_str for keyword in ["phd", "doctor", "doctorate"]):
        return "doctorate"
    elif any(keyword in degree_str for keyword in ["master", "m.sc", "m.s", "m.a", "mba"]):
        return "master"
    elif any(keyword in degree_str for keyword in ["bachelor", "b.sc", "b.s", "b.a"]):
        return "bachelor"
    elif any(keyword in degree_str for keyword in ["associate"]):
        return "associate"
    elif any(keyword in degree_str for keyword in ["diploma", "certificate"]):
        return "diploma"
    else:
        return "unknown"
