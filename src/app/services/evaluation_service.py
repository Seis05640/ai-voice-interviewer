from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.policies.scoring_policy import answer_quality_score
from app.persistence.repositories.interview_repo import InterviewRepository


class EvaluationService:
    def __init__(self, session: Session) -> None:
        self._interviews = InterviewRepository(session)

    def evaluate_session(self, *, session_id: str) -> float:
        messages = self._interviews.list_messages(session_id)
        candidate_answers = [m.content for m in messages if m.role == "candidate"]

        if not candidate_answers:
            return 0.0

        scores = [answer_quality_score(a) for a in candidate_answers]
        return sum(scores) / len(scores)
