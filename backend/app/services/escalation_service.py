"""
Escalation service for support-risk detection.

This module applies simple deterministic rules to detect whether a user
message should be flagged for human review.
"""


def check_escalation(message: str) -> dict:
    """Return escalation status and reason for a user message."""
    lowered = message.lower()

    escalation_rules = [
        {
            "keywords": ["fraud", "scam", "stolen card", "unauthorized charge"],
            "reason": "This issue appears to involve a fraud-related complaint and should be reviewed by a human support agent.",
        },
        {
            "keywords": ["lawyer", "legal", "sue", "lawsuit"],
            "reason": "This issue appears to involve legal risk and should be reviewed by a human support agent.",
        },
        {
            "keywords": ["chargeback", "billing dispute", "bank dispute"],
            "reason": "This issue appears to involve a billing dispute and should be reviewed by a human support agent.",
        },
        {
            "keywords": ["manager", "human agent", "real person", "speak to someone"],
            "reason": "The customer explicitly requested human assistance, so the case should be escalated.",
        },
        {
            "keywords": ["lost package", "package lost", "missing package"],
            "reason": "This issue may involve a lost shipment and should be reviewed by a human support agent.",
        },
    ]

    for rule in escalation_rules:
        for keyword in rule["keywords"]:
            if keyword in lowered:
                return {
                    "needed": True,
                    "reason": rule["reason"],
                }

    return {
        "needed": False,
        "reason": None,
    }