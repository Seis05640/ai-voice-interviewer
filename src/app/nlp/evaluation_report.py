"""Generate formatted evaluation reports for interview answers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from app.nlp.answer_evaluator import AnswerEvaluation, evaluate_answer


@dataclass
class InterviewEvaluationReport:
    """Complete evaluation report for an interview question and answer."""
    question: str
    answer: str
    question_type: str
    evaluation: AnswerEvaluation
    
    def format_text(self) -> str:
        """Format the evaluation report as plain text."""
        lines = [
            "=" * 70,
            "INTERVIEW ANSWER EVALUATION REPORT",
            "=" * 70,
            "",
            "QUESTION:",
            "-" * 70,
            self.question,
            "",
            "ANSWER:",
            "-" * 70,
            self.answer,
            "",
            "EVALUATION SCORES:",
            "-" * 70,
            f"Overall Score: {self.evaluation.overall_score_percent}/100",
            "",
            f"  Relevance:  {self.evaluation.relevance_score:.2f} (weight: 50%)",
            f"  Depth:      {self.evaluation.depth_score:.2f} (weight: 30%)",
            f"  Clarity:    {self.evaluation.clarity_score:.2f} (weight: 20%)",
            "",
            "EVALUATION SUMMARY:",
            "-" * 70,
            self.evaluation.explanation,
            "",
            "STRENGTHS:",
            "-" * 70,
        ]
        
        for i, strength in enumerate(self.evaluation.strengths, 1):
            lines.append(f"  {i}. {strength}")
        
        lines.extend([
            "",
            "AREAS FOR IMPROVEMENT:",
            "-" * 70,
        ])
        
        for i, weakness in enumerate(self.evaluation.weaknesses, 1):
            lines.append(f"  {i}. {weakness}")
        
        lines.extend([
            "",
            "SUGGESTIONS:",
            "-" * 70,
        ])
        
        for i, suggestion in enumerate(self.evaluation.suggestions, 1):
            lines.append(f"  {i}. {suggestion}")
        
        lines.extend([
            "",
            "=" * 70,
            "END OF REPORT",
            "=" * 70,
        ])
        
        return "\n".join(lines)
    
    def format_markdown(self) -> str:
        """Format the evaluation report as Markdown."""
        lines = [
            "# Interview Answer Evaluation Report",
            "",
            "## Question",
            self.question,
            "",
            "## Answer",
            self.answer,
            "",
            "## Evaluation Scores",
            "",
            f"**Overall Score:** {self.evaluation.overall_score_percent}/100",
            "",
            "| Criteria | Score | Weight |",
            "|----------|-------|--------|",
            f"| Relevance | {self.evaluation.relevance_score:.2f} | 50% |",
            f"| Depth | {self.evaluation.depth_score:.2f} | 30% |",
            f"| Clarity | {self.evaluation.clarity_score:.2f} | 20% |",
            "",
            "## Evaluation Summary",
            "",
            self.evaluation.explanation,
            "",
            "## Strengths",
            "",
        ]
        
        for strength in self.evaluation.strengths:
            lines.append(f"- {strength}")
        
        lines.extend([
            "",
            "## Areas for Improvement",
            "",
        ])
        
        for weakness in self.evaluation.weaknesses:
            lines.append(f"- {weakness}")
        
        lines.extend([
            "",
            "## Suggestions",
            "",
        ])
        
        for suggestion in self.evaluation.suggestions:
            lines.append(f"- {suggestion}")
        
        return "\n".join(lines)
    
    def format_dict(self) -> dict:
        """Format the evaluation report as a dictionary."""
        return {
            "question": self.question,
            "answer": self.answer,
            "question_type": self.question_type,
            "scores": {
                "overall": self.evaluation.overall_score,
                "overall_percent": self.evaluation.overall_score_percent,
                "relevance": self.evaluation.relevance_score,
                "depth": self.evaluation.depth_score,
                "clarity": self.evaluation.clarity_score,
            },
            "summary": self.evaluation.explanation,
            "strengths": self.evaluation.strengths,
            "weaknesses": self.evaluation.weaknesses,
            "suggestions": self.evaluation.suggestions,
        }


@dataclass
class BatchEvaluationReport:
    """Evaluation report for multiple interview answers."""
    candidate_name: str | None = None
    evaluations: list[InterviewEvaluationReport] = None
    
    def __post_init__(self):
        if self.evaluations is None:
            self.evaluations = []
    
    def add_evaluation(self, report: InterviewEvaluationReport):
        """Add an evaluation to the batch report."""
        self.evaluations.append(report)
    
    def calculate_average_scores(self) -> dict:
        """Calculate average scores across all evaluations."""
        if not self.evaluations:
            return {
                "overall": 0.0,
                "overall_percent": 0,
                "relevance": 0.0,
                "depth": 0.0,
                "clarity": 0.0,
            }
        
        count = len(self.evaluations)
        return {
            "overall": round(sum(e.evaluation.overall_score for e in self.evaluations) / count, 3),
            "overall_percent": round(sum(e.evaluation.overall_score_percent for e in self.evaluations) / count),
            "relevance": round(sum(e.evaluation.relevance_score for e in self.evaluations) / count, 3),
            "depth": round(sum(e.evaluation.depth_score for e in self.evaluations) / count, 3),
            "clarity": round(sum(e.evaluation.clarity_score for e in self.evaluations) / count, 3),
        }
    
    def format_text(self) -> str:
        """Format the batch evaluation report as plain text."""
        avg_scores = self.calculate_average_scores()
        
        lines = [
            "=" * 70,
            "BATCH INTERVIEW EVALUATION REPORT",
            "=" * 70,
        ]
        
        if self.candidate_name:
            lines.extend([
                f"Candidate: {self.candidate_name}",
                "",
            ])
        
        lines.extend([
            "AVERAGE SCORES:",
            "-" * 70,
            f"Overall Score: {avg_scores['overall_percent']}/100",
            f"  Relevance:  {avg_scores['relevance']:.2f}",
            f"  Depth:      {avg_scores['depth']:.2f}",
            f"  Clarity:    {avg_scores['clarity']:.2f}",
            "",
            f"Total Questions Evaluated: {len(self.evaluations)}",
            "",
            "=" * 70,
            "",
        ])
        
        for i, report in enumerate(self.evaluations, 1):
            lines.extend([
                f"--- Question {i} ---",
                "",
            ])
            lines.append(report.format_text())
            lines.append("")
        
        return "\n".join(lines)
    
    def format_markdown(self) -> str:
        """Format the batch evaluation report as Markdown."""
        avg_scores = self.calculate_average_scores()
        
        lines = [
            "# Batch Interview Evaluation Report",
            "",
        ]
        
        if self.candidate_name:
            lines.append(f"**Candidate:** {self.candidate_name}")
            lines.append("")
        
        lines.extend([
            "## Average Scores",
            "",
            f"**Overall:** {avg_scores['overall_percent']}/100",
            "",
            "| Criteria | Average Score |",
            "|----------|---------------|",
            f"| Relevance | {avg_scores['relevance']:.2f} |",
            f"| Depth | {avg_scores['depth']:.2f} |",
            f"| Clarity | {avg_scores['clarity']:.2f} |",
            "",
            f"**Total Questions Evaluated:** {len(self.evaluations)}",
            "",
            "---",
            "",
        ])
        
        for i, report in enumerate(self.evaluations, 1):
            lines.extend([
                f"## Question {i}",
                "",
            ])
            lines.append(report.format_markdown())
            lines.append("")
        
        return "\n".join(lines)


def generate_report(
    question: str,
    answer: str,
    question_type: str = "general",
    format: str = "text",
) -> str:
    """
    Generate a formatted evaluation report for a single question-answer pair.
    
    Args:
        question: The interview question
        answer: The candidate's answer
        question_type: Type of question
        format: Output format ('text', 'markdown', or 'dict')
        
    Returns:
        Formatted evaluation report
    """
    evaluation = evaluate_answer(question, answer, question_type)
    report = InterviewEvaluationReport(
        question=question,
        answer=answer,
        question_type=question_type,
        evaluation=evaluation,
    )
    
    if format == "text":
        return report.format_text()
    elif format == "markdown":
        return report.format_markdown()
    elif format == "dict":
        return str(report.format_dict())
    else:
        raise ValueError(f"Unknown format: {format}")


# Sample evaluation report generation function
def generate_sample_report() -> str:
    """
    Generate a sample evaluation report with example Q&A.
    
    Returns:
        Sample evaluation report in text format
    """
    sample_question = (
        "Tell me about a time when you had to handle a conflict within your team. "
        "How did you approach it and what was the outcome?"
    )
    
    sample_answer = (
        "In my previous role as a team lead, I had two developers who strongly disagreed "
        "on the technical approach for a new feature. One wanted to use a microservices "
        "architecture, while the other preferred a monolithic approach. The conflict was "
        "affecting team morale and delaying progress.\n\n"
        "First, I scheduled separate meetings with each developer to understand their "
        "perspectives fully. I learned that both had valid concerns about timeline, "
        "maintainability, and team expertise. Then I arranged a joint meeting where each "
        "person had to present the other's viewpoint before advocating for their own.\n\n"
        "This exercise helped them see each other's reasoning. We then discussed the "
        "trade-offs openly and decided on a hybrid approach that addressed the main "
        "concerns. The project was delivered on time, and the team actually became more "
        "collaborative afterward. The key was ensuring everyone felt heard and focusing "
        "on the shared goal rather than personal preferences."
    )
    
    report = generate_report(sample_question, sample_answer, "behavioral", "text")
    
    # Add header to indicate this is a sample
    lines = [
        "",
        "#" * 70,
        "# SAMPLE EVALUATION REPORT",
        "#" * 70,
        "",
        "The following is an example of an interview answer evaluation report.",
        "",
    ]
    
    return "\n".join(lines) + report


# Sample evaluation report with different answer quality
def generate_sample_reports_comparison() -> str:
    """
    Generate sample reports comparing different answer qualities.
    
    Returns:
        Multiple sample evaluation reports for comparison
    """
    question = "What is your approach to debugging complex issues in production?"
    
    # Excellent answer
    excellent_answer = (
        "My approach to debugging production issues follows a structured process. "
        "First, I gather as much information as possible from monitoring tools, logs, "
        "and error tracking systems like Sentry. I look for patterns, timestamps, and "
        "affected user segments to understand the scope.\n\n"
        "Second, I assess the severity and business impact. If it's critical, I initiate "
        "our incident response protocol and coordinate with stakeholders. For less severe "
        "issues, I create a timeline and communicate expectations.\n\n"
        "Third, I work to reproduce the issue in a staging environment, using the same "
        "data and configuration if possible. I use techniques like binary search on code "
        "commits, adding strategic logging, and analyzing database queries.\n\n"
        "Fourth, once identified, I implement a fix with thorough testing. However, I also "
        "look for the root cause and suggest improvements to prevent similar issues. "
        "Finally, I document the incident and conduct a post-mortem to share learnings "
        "with the team. In my last role, this approach helped reduce our MTTR from 4 "
        "hours to under 90 minutes over 6 months."
    )
    
    # Average answer
    average_answer = (
        "When I see a production issue, I first check the logs to see what went wrong. "
        "Then I look at the code to find the bug. Sometimes it's a simple fix like a "
        "typo or a missing condition. Other times it's more complicated and takes longer. "
        "I try to reproduce it locally if I can. After fixing it, I deploy the fix and "
        "monitor to make sure it's working. I think being systematic is important but "
        "sometimes you just need to jump in and fix it quickly."
    )
    
    # Poor answer
    poor_answer = (
        "I just look at the error and try to fix it. Sometimes I Google the error message "
        "to see if others had the same problem. It really depends on what kind of issue it is. "
        "If it's urgent, I just try to get it fixed as fast as possible. I don't really "
        "have a specific process, I just kind of figure it out as I go."
    )
    
    lines = [
        "#" * 70,
        "# SAMPLE EVALUATION REPORTS COMPARISON",
        "#" * 70,
        "",
        "Question: " + question,
        "",
        "=" * 70,
        "",
        "EXCELLENT ANSWER EXAMPLE:",
        "=" * 70,
        "",
    ]
    
    lines.append(generate_report(question, excellent_answer, "technical", "text"))
    
    lines.extend([
        "",
        "=" * 70,
        "",
        "AVERAGE ANSWER EXAMPLE:",
        "=" * 70,
        "",
    ])
    
    lines.append(generate_report(question, average_answer, "technical", "text"))
    
    lines.extend([
        "",
        "=" * 70,
        "",
        "POOR ANSWER EXAMPLE:",
        "=" * 70,
        "",
    ])
    
    lines.append(generate_report(question, poor_answer, "technical", "text"))
    
    return "\n".join(lines)
