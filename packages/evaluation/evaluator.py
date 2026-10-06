from typing import Dict, Any, Optional

class EvaluatorAgent:
    def __init__(self):
        pass

    def evaluate_output(self, goal: str, result_output: str, required_keywords: Optional[list] = None) -> Dict[str, Any]:
        if not result_output or len(result_output.strip()) == 0:
            return {
                "score": 0.0,
                "passed": False,
                "feedback": "Evaluation failed: Output result is empty or null."
            }

        score = 0.95
        feedback = "Result satisfactorily fulfills the target goal with clean structure."
        
        if required_keywords:
            missing = [kw for kw in required_keywords if kw.lower() not in result_output.lower()]
            if missing:
                score -= len(missing) * 0.15
                score = max(score, 0.0)
                feedback = f"Output satisfies goal partially, but missing keywords: {missing}"

        return {
            "score": round(score, 2),
            "passed": score >= 0.7,
            "feedback": feedback
        }

evaluator_agent = EvaluatorAgent()
