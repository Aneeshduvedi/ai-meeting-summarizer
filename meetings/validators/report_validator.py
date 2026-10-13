
def validate_report(report: dict) -> dict:
    """Validate the structure of a generated meeting report."""

    if not isinstance(report, dict):
        raise ValueError("Report must be a dictionary.")

    required_fields = [
        "summary",
        "topics",
        "decisions",
        "action_items",
        "unresolved_questions",
    ]

    for field in required_fields:
        if field not in report:
            raise ValueError(f"Missing report field: {field}")

    if not isinstance(report["summary"], str):
        raise ValueError("Summary must be text.")

    for field in (
        "topics",
        "decisions",
        "action_items",
        "unresolved_questions",
    ):
        if not isinstance(report[field], list):
            raise ValueError(f"{field} must be a list.")

    for item in report["action_items"]:
        if not isinstance(item, dict):
            raise ValueError("Each action item must be an object.")

        if not isinstance(item.get("task"), str):
            raise ValueError("Each action item needs a task.")

        if not isinstance(item.get("owner"), str):
            raise ValueError("Each action item needs an owner field.")

        if not isinstance(item.get("deadline"), str):
            raise ValueError("Each action item needs a deadline field.")

    return report
