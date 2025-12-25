from __future__ import annotations

"""Background tasks scaffold.

For the demo scaffold we keep this as plain functions.
Later, you can move these into Celery/RQ tasks without changing the service layer.
"""


def parse_resume_task(*, candidate_id: str) -> None:
    raise NotImplementedError


def generate_report_task(*, session_id: str) -> None:
    raise NotImplementedError
