#!/usr/bin/env python3
"""Demo script for interview answer evaluation module."""

from app.nlp import (
    evaluate_answer,
    generate_sample_report,
    generate_sample_reports_comparison,
)


def main():
    """Run the evaluation demo."""
    print("=" * 70)
    print("INTERVIEW ANSWER EVALUATION MODULE DEMO")
    print("=" * 70)
    print()
    
    # Sample 1: Behavioral question with good answer
    print("=" * 70)
    print("SAMPLE 1: Behavioral Question (Conflict Resolution)")
    print("=" * 70)
    print()
    
    question = (
        "Tell me about a time when you had to handle a conflict within your team. "
        "How did you approach it and what was the outcome?"
    )
    
    answer = (
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
    
    result = evaluate_answer(question, answer, "behavioral")
    
    print(f"Question: {question}")
    print(f"\nAnswer: {answer}")
    print("\n" + "-" * 70)
    print("EVALUATION RESULTS:")
    print("-" * 70)
    print(f"Overall Score: {result.overall_score_percent}/100")
    print(f"  Relevance: {result.relevance_score:.2f} (weight: 50%)")
    print(f"  Depth: {result.depth_score:.2f} (weight: 30%)")
    print(f"  Clarity: {result.clarity_score:.2f} (weight: 20%)")
    print(f"\nSummary: {result.explanation}")
    print(f"\nStrengths:")
    for strength in result.strengths:
        print(f"  - {strength}")
    print(f"\nAreas for Improvement:")
    for weakness in result.weaknesses:
        print(f"  - {weakness}")
    print(f"\nSuggestions:")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
    print()
    
    # Sample 2: Technical question with average answer
    print("=" * 70)
    print("SAMPLE 2: Technical Question (Debugging)")
    print("=" * 70)
    print()
    
    question = "What is your approach to debugging complex issues in production?"
    
    answer = (
        "When I see a production issue, I first check the logs to see what went wrong. "
        "Then I look at the code to find the bug. Sometimes it's a simple fix like a "
        "typo or a missing condition. Other times it's more complicated and takes longer. "
        "I try to reproduce it locally if I can. After fixing it, I deploy the fix and "
        "monitor to make sure it's working. I think being systematic is important but "
        "sometimes you just need to jump in and fix it quickly."
    )
    
    result = evaluate_answer(question, answer, "technical")
    
    print(f"Question: {question}")
    print(f"\nAnswer: {answer}")
    print("\n" + "-" * 70)
    print("EVALUATION RESULTS:")
    print("-" * 70)
    print(f"Overall Score: {result.overall_score_percent}/100")
    print(f"  Relevance: {result.relevance_score:.2f} (weight: 50%)")
    print(f"  Depth: {result.depth_score:.2f} (weight: 30%)")
    print(f"  Clarity: {result.clarity_score:.2f} (weight: 20%)")
    print(f"\nSummary: {result.explanation}")
    print()
    
    # Sample 3: Simple question with brief answer
    print("=" * 70)
    print("SAMPLE 3: General Question (Motivation)")
    print("=" * 70)
    print()
    
    question = "Why do you want to work for our company?"
    
    answer = "I think your company is great and I want to learn a lot."
    
    result = evaluate_answer(question, answer, "general")
    
    print(f"Question: {question}")
    print(f"\nAnswer: {answer}")
    print("\n" + "-" * 70)
    print("EVALUATION RESULTS:")
    print("-" * 70)
    print(f"Overall Score: {result.overall_score_percent}/100")
    print(f"  Relevance: {result.relevance_score:.2f} (weight: 50%)")
    print(f"  Depth: {result.depth_score:.2f} (weight: 30%)")
    print(f"  Clarity: {result.clarity_score:.2f} (weight: 20%)")
    print(f"\nSummary: {result.explanation}")
    print()
    
    # Show sample reports
    print("=" * 70)
    print("SAMPLE EVALUATION REPORT")
    print("=" * 70)
    print()
    print(generate_sample_report())
    print()


if __name__ == "__main__":
    main()
