"""
Output Reviewer
===============
Lab 8: Self-reflection on outputs to enable improvement.
"""

from dataclasses import dataclass
from typing import Optional
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ReviewResult:
    """Result of an output review."""
    quality_score: float  # 0-1
    issues: list[str]
    suggestions: list[str]
    should_retry: bool


class OutputReviewer:
    """
    Reviews AI outputs for quality and suggests improvements.

    Enables self-correction by:
    1. Evaluating output quality
    2. Identifying issues
    3. Suggesting improvements
    4. Recommending retry when needed
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._review_history: list[ReviewResult] = []

    def review(self, output: str, original_query: str, context: str = "") -> ReviewResult:
        """Review an output for quality."""
        prompt = f"""Review this AI assistant output for quality.

Original Query: {original_query}
Output: {output}

Rate the output quality from 0 to 1 and identify any issues.
Return a JSON object with:
- "quality_score": 0-1 float
- "issues": list of problems found
- "suggestions": list of improvements
- "should_retry": true if output is poor quality

Only return the JSON."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )

            # Parse response
            import json
            text = response.choices[0].message.content
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                data = json.loads(text[start:end])
                result = ReviewResult(
                    quality_score=float(data.get("quality_score", 0.5)),
                    issues=data.get("issues", []),
                    suggestions=data.get("suggestions", []),
                    should_retry=data.get("should_retry", False)
                )
                self._review_history.append(result)
                return result
        except:
            pass

        return ReviewResult(quality_score=0.5, issues=[], suggestions=[], should_retry=False)

    def get_average_quality(self) -> float:
        """Get average quality score from history."""
        if not self._review_history:
            return 0.0
        return sum(r.quality_score for r in self._review_history) / len(self._review_history)

    def get_common_issues(self) -> list[str]:
        """Get most common issues from history."""
        all_issues = []
        for r in self._review_history:
            all_issues.extend(r.issues)
        return list(set(all_issues))[:5]
