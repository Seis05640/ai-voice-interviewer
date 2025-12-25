"""Evaluate interview answers based on relevance, clarity, and depth."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Final


# Weights for different evaluation criteria
_WEIGHTS: Final = {
    "relevance": 0.50,  # 50% weight on how well the answer addresses the question
    "depth": 0.30,      # 30% weight on level of detail and comprehensiveness
    "clarity": 0.20,    # 20% weight on clarity and understandability
}


@dataclass
class AnswerEvaluation:
    """Structured result of an answer evaluation."""
    relevance_score: float
    clarity_score: float
    depth_score: float
    overall_score: float
    overall_score_percent: int
    explanation: str
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def _tokenize(text: str) -> list[str]:
    """Simple tokenization of text into words."""
    return [t.lower() for t in re.findall(r"[a-zA-Z0-9]+", text)]


def _extract_key_phrases(text: str, min_length: int = 3) -> list[str]:
    """Extract key phrases from text (n-grams)."""
    tokens = _tokenize(text)
    if len(tokens) < min_length:
        return [tokens[0]] if tokens else []
    
    # Return bigrams and trigrams
    phrases = []
    for n in [2, 3]:
        for i in range(len(tokens) - n + 1):
            phrase = " ".join(tokens[i:i + n])
            phrases.append(phrase)
    
    return phrases


def _calculate_relevance(question: str, answer: str) -> float:
    """
    Calculate how relevant the answer is to the question.
    
    Factors considered:
    - Keyword overlap between question and answer
    - Answer length relative to question (too short may be irrelevant)
    - Presence of question-related terms in answer
    """
    if not answer or not question:
        return 0.0
    
    # Extract key terms from question
    question_tokens = set(_tokenize(question))
    
    # Remove common stop words
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "can", "could", "should", "may", "might", "must", "what",
        "how", "why", "when", "where", "who", "which", "tell",
        "me", "about", "your", "you", "to", "for", "of", "in",
    }
    
    question_keywords = {t for t in question_tokens if t not in stop_words and len(t) > 2}
    answer_tokens = set(_tokenize(answer))
    
    # Calculate keyword overlap
    if not question_keywords:
        keyword_overlap = 0.5  # Default when no clear keywords
    else:
        matched_keywords = question_keywords & answer_tokens
        keyword_overlap = len(matched_keywords) / len(question_keywords)
    
    # Check if answer directly addresses the question
    relevance_boosters = [
        "first", "second", "third", "finally", "in my experience",
        "specifically", "for example", "to illustrate", "basically",
        "essentially", "primarily", "mainly", "therefore", "consequently",
        "as a result", "because", "since", "due to",
    ]
    
    answer_lower = answer.lower()
    booster_count = sum(1 for booster in relevance_boosters if booster in answer_lower)
    booster_score = min(booster_count * 0.05, 0.15)
    
    # Penalize very short answers (likely incomplete)
    answer_words = len(_tokenize(answer))
    question_words = len(_tokenize(question))
    
    length_score = 0.0
    if answer_words >= question_words * 2:
        length_score = 1.0
    elif answer_words >= question_words:
        length_score = 0.8
    elif answer_words >= question_words * 0.5:
        length_score = 0.6
    elif answer_words > 0:
        length_score = 0.3
    
    # Combine factors
    relevance = (
        keyword_overlap * 0.5 +
        length_score * 0.35 +
        booster_score * 0.15
    )
    
    return min(relevance, 1.0)


def _calculate_clarity(answer: str) -> float:
    """
    Calculate how clear and understandable the answer is.
    
    Factors considered:
    - Sentence structure (avoid very long sentences)
    - Use of examples and illustrations
    - Logical flow indicators
    - Ambiguous language markers
    """
    if not answer:
        return 0.0
    
    clarity_score = 0.5  # Start with baseline
    
    # Check sentence length
    sentences = re.split(r"[.!?]+", answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if sentences:
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_sentence_length <= 15:
            clarity_score += 0.15  # Good, concise sentences
        elif avg_sentence_length <= 25:
            clarity_score += 0.05  # Acceptable
        elif avg_sentence_length > 40:
            clarity_score -= 0.15  # Too long, hard to follow
    
    # Check for examples and illustrations
    example_indicators = [
        "for example", "for instance", "such as", "like", "specifically",
        "to illustrate", "consider this", "imagine", "let's say", "e.g.",
    ]
    
    has_examples = any(ind in answer.lower() for ind in example_indicators)
    if has_examples:
        clarity_score += 0.15
    
    # Check for logical flow indicators
    flow_indicators = [
        "first", "second", "third", "next", "then", "finally", "lastly",
        "additionally", "furthermore", "moreover", "also", "besides",
        "however", "on the other hand", "conversely", "alternatively",
        "therefore", "thus", "consequently", "as a result", "because",
        "so", "in conclusion", "in summary", "overall",
    ]
    
    flow_count = sum(1 for ind in flow_indicators if ind in answer.lower())
    clarity_score += min(flow_count * 0.03, 0.15)
    
    # Penalize ambiguous language
    ambiguous_markers = [
        "kind of", "sort of", "maybe", "perhaps", "i think", "i guess",
        "probably", "possibly", "might be", "could be", "not sure",
        "uh", "um", "hmm", "like", "you know",
    ]
    
    ambiguous_count = sum(1 for marker in ambiguous_markers if marker in answer.lower())
    clarity_score -= min(ambiguous_count * 0.05, 0.20)
    
    # Check for structured format (bullets or numbered lists)
    has_structure = bool(re.search(r"^\s*[-*•]\s+", answer, re.MULTILINE)) or \
                   bool(re.search(r"^\s*\d+[.)]\s+", answer, re.MULTILINE))
    if has_structure:
        clarity_score += 0.10
    
    return min(max(clarity_score, 0.0), 1.0)


def _calculate_depth(answer: str, question_type: str = "general") -> float:
    """
    Calculate the depth and comprehensiveness of the answer.
    
    Factors considered:
    - Use of technical terminology (appropriate for the context)
    - Multiple perspectives or approaches mentioned
    - Specific details and concrete examples
    - Acknowledgement of trade-offs or complexities
    - Answer length (reasonable length indicates depth)
    """
    if not answer:
        return 0.0
    
    depth_score = 0.3  # Start with baseline
    
    # Check for technical/subject-specific terms
    answer_tokens = _tokenize(answer)
    unique_tokens = set(answer_tokens)
    
    # Vocabulary richness (unique tokens / total tokens)
    if answer_tokens:
        vocabulary_richness = len(unique_tokens) / len(answer_tokens)
        depth_score += min(vocabulary_richness * 0.2, 0.15)
    
    # Check for specific details (numbers, percentages, metrics)
    has_numbers = bool(re.search(r"\d+%|\d+\.\d+|\d+ years|\d+ months", answer))
    if has_numbers:
        depth_score += 0.15
    
    # Check for concrete examples or case studies
    concrete_indicators = [
        "in my previous role", "at my last company", "i worked on",
        "we implemented", "the project involved", "for instance",
        "specifically", "one time when", "a situation where",
    ]
    
    concrete_count = sum(1 for ind in concrete_indicators if ind in answer.lower())
    depth_score += min(concrete_count * 0.08, 0.20)
    
    # Check for nuance and trade-off recognition
    nuance_indicators = [
        "however", "although", "while", "on the other hand", "conversely",
        "trade-off", "balance", "depends on", "consider", "alternative",
        "pros and cons", "advantage", "disadvantage", "challenge",
        "limitation", "it's important to note", "keep in mind",
    ]
    
    nuance_count = sum(1 for ind in nuance_indicators if ind in answer.lower())
    depth_score += min(nuance_count * 0.05, 0.15)
    
    # Check for multiple approaches or methods mentioned
    approach_indicators = [
        "first approach", "second method", "alternative way", "another option",
        "one way", "another way", "also", "additionally", "furthermore",
        "in addition", "besides", "moreover",
    ]
    
    approach_count = sum(1 for ind in approach_indicators if ind in answer.lower())
    depth_score += min(approach_count * 0.06, 0.18)
    
    # Check answer length (within reasonable bounds)
    word_count = len(answer_tokens)
    if word_count >= 150:
        depth_score += 0.10  # Good length for depth
    elif word_count >= 100:
        depth_score += 0.08
    elif word_count >= 50:
        depth_score += 0.05
    elif word_count < 20:
        depth_score -= 0.20  # Too short for meaningful depth
    
    return min(max(depth_score, 0.0), 1.0)


def _generate_evaluation_explanation(
    relevance: float,
    clarity: float,
    depth: float,
    question: str,
    answer: str,
) -> str:
    """Generate a human-readable explanation of the evaluation."""
    parts = []
    
    # Relevance explanation
    if relevance >= 0.8:
        parts.append("The answer directly addresses the question with strong alignment.")
    elif relevance >= 0.6:
        parts.append("The answer addresses most aspects of the question.")
    elif relevance >= 0.4:
        parts.append("The answer partially addresses the question but may miss some key points.")
    else:
        parts.append("The answer does not adequately address the question asked.")
    
    # Clarity explanation
    if clarity >= 0.8:
        parts.append("Communication is clear and well-structured.")
    elif clarity >= 0.6:
        parts.append("Communication is generally clear with minor improvements possible.")
    elif clarity >= 0.4:
        parts.append("Communication could be improved with better structure and examples.")
    else:
        parts.append("Communication needs significant improvement to be more understandable.")
    
    # Depth explanation
    if depth >= 0.8:
        parts.append("Demonstrates strong subject knowledge with good detail and nuance.")
    elif depth >= 0.6:
        parts.append("Shows good understanding with reasonable detail provided.")
    elif depth >= 0.4:
        parts.append("Shows basic understanding but lacks depth and specific examples.")
    else:
        parts.append("Answer lacks sufficient detail and depth to demonstrate expertise.")
    
    return ". ".join(parts)


def _identify_strengths(
    relevance: float,
    clarity: float,
    depth: float,
    answer: str,
) -> list[str]:
    """Identify strengths in the answer."""
    strengths = []
    
    if relevance >= 0.8:
        strengths.append("Directly addresses the question")
    
    if clarity >= 0.7:
        strengths.append("Clear and well-structured communication")
    
    if depth >= 0.7:
        strengths.append("Demonstrates strong subject knowledge")
    
    # Check for specific strengths
    if "example" in answer.lower() or "for instance" in answer.lower():
        strengths.append("Uses concrete examples to illustrate points")
    
    if re.search(r"first.*second.*third", answer.lower()):
        strengths.append("Well-organized with clear structure")
    
    if any(word in answer.lower() for word in ["however", "although", "trade-off"]):
        strengths.append("Shows awareness of nuance and complexity")
    
    if re.search(r"\d+%|\d+\.\d+", answer):
        strengths.append("Uses specific metrics and data points")
    
    return strengths if strengths else ["Answered the question"]


def _identify_weaknesses(
    relevance: float,
    clarity: float,
    depth: float,
    answer: str,
) -> list[str]:
    """Identify weaknesses in the answer."""
    weaknesses = []
    
    if relevance < 0.5:
        weaknesses.append("Does not fully address the question")
    
    if clarity < 0.5:
        weaknesses.append("Could improve clarity and structure")
    
    if depth < 0.5:
        weaknesses.append("Lacks depth and specific examples")
    
    # Check for specific weaknesses
    if len(_tokenize(answer)) < 30:
        weaknesses.append("Answer is too brief")
    
    if "kind of" in answer.lower() or "sort of" in answer.lower():
        weaknesses.append("Uses tentative language")
    
    if not any(ind in answer.lower() for ind in ["example", "for instance", "such as"]):
        weaknesses.append("Could benefit from more concrete examples")
    
    if not any(ind in answer.lower() for ind in ["however", "although", "on the other hand"]):
        weaknesses.append("Could discuss trade-offs or alternative approaches")
    
    return weaknesses if weaknesses else ["Minor areas for improvement exist"]


def _generate_suggestions(
    relevance: float,
    clarity: float,
    depth: float,
    question: str,
    answer: str,
) -> list[str]:
    """Generate actionable suggestions for improvement."""
    suggestions = []
    
    if relevance < 0.6:
        suggestions.append("Focus more directly on the core question asked")
    
    if clarity < 0.6:
        suggestions.append("Use a more structured format with clear points")
        suggestions.append("Include examples to make your answer more concrete")
    
    if depth < 0.6:
        suggestions.append("Provide more specific details and examples from your experience")
        suggestions.append("Discuss multiple approaches or considerations")
    
    if len(_tokenize(answer)) < 50:
        suggestions.append("Expand on your answer with more detail")
    
    if "example" not in answer.lower():
        suggestions.append("Add specific examples to illustrate your points")
    
    if not any(ind in answer.lower() for ind in ["however", "although", "trade-off"]):
        suggestions.append("Consider discussing trade-offs or alternative perspectives")
    
    return suggestions if suggestions else ["Continue with this approach"]


def evaluate_answer(
    question: str,
    answer: str,
    question_type: str = "general",
) -> AnswerEvaluation:
    """
    Evaluate an interview answer based on relevance, clarity, and depth.
    
    Args:
        question: The interview question asked
        answer: The candidate's response
        question_type: Type of question (general, technical, behavioral, situational)
        
    Returns:
        AnswerEvaluation object with scores and detailed feedback
    """
    # Calculate individual scores
    relevance = _calculate_relevance(question, answer)
    clarity = _calculate_clarity(answer)
    depth = _calculate_depth(answer, question_type)
    
    # Calculate weighted overall score
    overall = (
        relevance * _WEIGHTS["relevance"]
        + depth * _WEIGHTS["depth"]
        + clarity * _WEIGHTS["clarity"]
    )
    
    # Generate explanation and feedback
    explanation = _generate_evaluation_explanation(relevance, clarity, depth, question, answer)
    strengths = _identify_strengths(relevance, clarity, depth, answer)
    weaknesses = _identify_weaknesses(relevance, clarity, depth, answer)
    suggestions = _generate_suggestions(relevance, clarity, depth, question, answer)
    
    return AnswerEvaluation(
        relevance_score=round(relevance, 3),
        clarity_score=round(clarity, 3),
        depth_score=round(depth, 3),
        overall_score=round(overall, 3),
        overall_score_percent=int(overall * 100),
        explanation=explanation,
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions,
    )


def evaluate_answer_dict(
    question: str,
    answer: str,
    question_type: str = "general",
) -> dict:
    """
    Evaluate an interview answer and return results as a dictionary.
    
    Args:
        question: The interview question asked
        answer: The candidate's response
        question_type: Type of question (general, technical, behavioral, situational)
        
    Returns:
        Dictionary with evaluation results:
        {
            "relevance_score": float,
            "clarity_score": float,
            "depth_score": float,
            "overall_score": float,
            "overall_score_percent": int,
            "explanation": str,
            "strengths": list[str],
            "weaknesses": list[str],
            "suggestions": list[str],
        }
    """
    evaluation = evaluate_answer(question, answer, question_type)
    
    return {
        "relevance_score": evaluation.relevance_score,
        "clarity_score": evaluation.clarity_score,
        "depth_score": evaluation.depth_score,
        "overall_score": evaluation.overall_score,
        "overall_score_percent": evaluation.overall_score_percent,
        "explanation": evaluation.explanation,
        "strengths": evaluation.strengths,
        "weaknesses": evaluation.weaknesses,
        "suggestions": evaluation.suggestions,
    }
