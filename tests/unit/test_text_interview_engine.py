from app.interview_engine import TextInterviewEngine


def test_text_interview_engine_flow():
    engine = TextInterviewEngine()

    jd = "Python FastAPI AWS"
    resume = """
    WORK EXPERIENCE
    Backend Engineer | ExampleCo | 2022 - Present
    - Built REST APIs using FastAPI and SQLAlchemy

    SKILLS
    Python, FastAPI
    """

    state = engine.start(job_description=jd, resume_text=resume, max_questions=4)

    assert state.status == "active"
    assert state.max_questions == 4
    assert state.turns[1].question.startswith("On your resume you mention")

    answers = ["a1", "a2", "a3", "a4"]
    for a in answers:
        q = engine.next_question(state)
        assert q is not None
        engine.answer(state, answer=a)

    assert state.status == "completed"
    assert engine.next_question(state) is None
    assert [t.answer for t in state.turns] == answers
