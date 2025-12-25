#!/usr/bin/env python3
"""Sample evaluation reports demonstrating different output formats."""

from app.nlp import evaluate_answer, generate_report, InterviewEvaluationReport, BatchEvaluationReport


def main():
    """Generate sample evaluation reports in different formats."""
    
    # Sample question and answer
    question = "Tell me about a challenging project you've worked on. What made it challenging and how did you overcome those challenges?"
    
    answer = (
        "The most challenging project I worked on was migrating our legacy monolithic application "
        "to microservices architecture. This project was challenging for several reasons:\n\n"
        "First, we had to maintain 100% uptime during the migration, which required careful "
        "orchestration of data synchronization between the old and new systems. Second, the "
        "legacy codebase had minimal documentation and test coverage, making it difficult to "
        "understand all the dependencies.\n\n"
        "To overcome these challenges, I took a phased approach. First, I spent two weeks "
        "analyzing the existing system and creating a comprehensive mapping of all data flows "
        "and dependencies. This documentation became the foundation for our migration plan.\n\n"
        "Second, I proposed a strangler fig pattern where we gradually extracted services from "
        "the monolith, implementing an API gateway to route requests between the old and new "
        "systems. This allowed us to migrate at our own pace without disrupting users.\n\n"
        "Third, I established rigorous testing with end-to-end integration tests that covered "
        "all critical paths. We also implemented canary deployments to catch issues early.\n\n"
        "The result was a successful migration completed in 6 months with zero downtime incidents. "
        "Post-migration, we saw a 40% improvement in deployment frequency and 60% reduction in "
        "bug fix time. The key was thorough planning, incremental progress, and maintaining "
        "clear communication with all stakeholders throughout the process."
    )
    
    # Evaluate the answer
    result = evaluate_answer(question, answer, "behavioral")
    
    print("=" * 70)
    print("INTERVIEW ANSWER EVALUATION - SAMPLE OUTPUT")
    print("=" * 70)
    print()
    
    # Show scores
    print("SCORES:")
    print("-" * 70)
    print(f"Overall Score: {result.overall_score_percent}/100")
    print(f"  Relevance: {result.relevance_score:.2f} (weight: 50%)")
    print(f"  Depth:      {result.depth_score:.2f} (weight: 30%)")
    print(f"  Clarity:    {result.clarity_score:.2f} (weight: 20%)")
    print()
    
    # Show explanation
    print("SUMMARY:")
    print("-" * 70)
    print(result.explanation)
    print()
    
    # Show strengths
    print("STRENGTHS:")
    print("-" * 70)
    for i, strength in enumerate(result.strengths, 1):
        print(f"  {i}. {strength}")
    print()
    
    # Show weaknesses
    print("AREAS FOR IMPROVEMENT:")
    print("-" * 70)
    for i, weakness in enumerate(result.weaknesses, 1):
        print(f"  {i}. {weakness}")
    print()
    
    # Show suggestions
    print("SUGGESTIONS:")
    print("-" * 70)
    for i, suggestion in enumerate(result.suggestions, 1):
        print(f"  {i}. {suggestion}")
    print()
    
    # Generate formatted reports
    print("=" * 70)
    print("TEXT FORMAT REPORT")
    print("=" * 70)
    text_report = generate_report(question, answer, "behavioral", "text")
    print(text_report)
    print()
    
    print("=" * 70)
    print("MARKDOWN FORMAT REPORT")
    print("=" * 70)
    markdown_report = generate_report(question, answer, "behavioral", "markdown")
    print(markdown_report)
    print()
    
    # Show dictionary format
    print("=" * 70)
    print("DICTIONARY FORMAT")
    print("=" * 70)
    report = InterviewEvaluationReport(
        question=question,
        answer=answer,
        question_type="behavioral",
        evaluation=result,
    )
    dict_output = report.format_dict()
    import json
    print(json.dumps(dict_output, indent=2))
    print()
    
    # Show batch evaluation
    print("=" * 70)
    print("BATCH EVALUATION EXAMPLE")
    print("=" * 70)
    
    questions = [
        "Tell me about a time you demonstrated leadership.",
        "How do you handle tight deadlines?",
        "Describe a technical challenge you solved.",
    ]
    
    answers = [
        "I led a team of 5 developers on a critical project. I organized daily stand-ups, "
        "created a clear roadmap, and mentored junior team members. We delivered ahead of schedule.",
        "When faced with tight deadlines, I prioritize tasks ruthlessly. I identify the MVP, "
        "focus on critical path items, and communicate early if scope needs adjustment.",
        "We had a performance issue with our database. I analyzed query patterns, added "
        "appropriate indexes, and implemented caching. This reduced response times by 80%.",
    ]
    
    batch = BatchEvaluationReport(candidate_name="Sample Candidate")
    
    for q, a in zip(questions, answers):
        eval_result = evaluate_answer(q, a, "behavioral")
        single_report = InterviewEvaluationReport(
            question=q,
            answer=a,
            question_type="behavioral",
            evaluation=eval_result,
        )
        batch.add_evaluation(single_report)
    
    avg_scores = batch.calculate_average_scores()
    print("Average Scores:")
    print(f"  Overall: {avg_scores['overall_percent']}/100")
    print(f"  Relevance: {avg_scores['relevance']:.2f}")
    print(f"  Depth: {avg_scores['depth']:.2f}")
    print(f"  Clarity: {avg_scores['clarity']:.2f}")
    print(f"  Total Questions: {len(batch.evaluations)}")
    print()


if __name__ == "__main__":
    main()
