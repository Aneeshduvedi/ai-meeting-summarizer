
def generate_report(
    analysis: dict,
    action_data: dict,
) -> dict:
    """Combine agent outputs into one structured meeting report."""

    return {
        "summary": analysis.get("summary", ""),
        "topics": analysis.get("topics", []),
        "decisions": action_data.get("decisions", []),
        "action_items": action_data.get("action_items", []),
        "unresolved_questions": action_data.get(
            "unresolved_questions", []
        ),
    }
