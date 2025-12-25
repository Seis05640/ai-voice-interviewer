"""NLP module for resume processing and screening."""

from app.nlp.skill_extractor import extract_skills
from app.nlp.education_extractor import extract_education
from app.nlp.experience_extractor import extract_experience
from app.nlp.scorer import calculate_match_score
from app.nlp.answer_evaluator import evaluate_answer, evaluate_answer_dict, AnswerEvaluation
from app.nlp.evaluation_report import (
    generate_report,
    generate_sample_report,
    generate_sample_reports_comparison,
    InterviewEvaluationReport,
    BatchEvaluationReport,
)

__all__ = [
    "extract_skills",
    "extract_education",
    "extract_experience",
    "calculate_match_score",
    "evaluate_answer",
    "evaluate_answer_dict",
    "AnswerEvaluation",
    "generate_report",
    "generate_sample_report",
    "generate_sample_reports_comparison",
    "InterviewEvaluationReport",
    "BatchEvaluationReport",
]
