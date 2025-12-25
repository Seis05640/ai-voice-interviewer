from app.domain.policies.shortlisting import token_overlap_score


def test_token_overlap_score_basic():
    jd = "Python FastAPI SQL"
    resume = "I have Python and SQL experience"
    score = token_overlap_score(jd, resume)
    assert 0.0 < score <= 1.0
