from datetime import datetime
from typing import Dict, Any


def verify_milestone(
    contract_milestone: Dict[str, Any],
    actual_progress_percent: float,
    quality_verified: bool
) -> Dict[str, Any]:
    """
    Verifier Agent (FINAL AUTHORITY)

    Compares contract milestone requirements with
    verified ground reality and returns a payment decision.
    """

    expected_percent = contract_milestone["percentage"]
    deadline = contract_milestone["deadline"]

    today = datetime.now().date()
    milestone_deadline = datetime.fromisoformat(deadline).date()

    # Deterministic checks
    progress_ok = actual_progress_percent >= expected_percent
    deadline_ok = today <= milestone_deadline
    quality_ok = quality_verified

    milestone_verified = progress_ok and deadline_ok and quality_ok

    return {
        "expected_progress": expected_percent,
        "actual_progress": actual_progress_percent,
        "progress_match": progress_ok,
        "deadline": deadline,
        "deadline_ok": deadline_ok,
        "quality_verified": quality_ok,
        "milestone_verified": milestone_verified,
        "decision": (
            "APPROVE_FOR_PAYMENT"
            if milestone_verified
            else "HOLD_AND_REVIEW"
        )
    }
