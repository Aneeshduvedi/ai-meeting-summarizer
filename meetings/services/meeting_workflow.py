
from django.db import transaction

from meetings.agents.meeting_analysis import analyze_meeting
from meetings.agents.action_item import extract_action_items
from meetings.agents.report_generation import generate_report
from meetings.validators.report_validator import validate_report
from meetings.models import MeetingReport


def summarize_meeting(meeting):
    transcript = meeting.transcript.strip()

    if not transcript:
        raise ValueError("Meeting transcript cannot be empty.")

    # Run the two AI analysis components.
    analysis = analyze_meeting(transcript)
    action_data = extract_action_items(transcript)

    # Combine and validate the report.
    report_data = generate_report(analysis, action_data)
    validate_report(report_data)

    # Save the report, creating or updating the existing record.
    with transaction.atomic():
        report, _ = MeetingReport.objects.update_or_create(
            meeting=meeting,
            defaults={
                "summary": report_data["summary"],
                "topics": report_data["topics"],
                "decisions": report_data["decisions"],
                "action_items": report_data["action_items"],
                "unresolved_questions": report_data[
                    "unresolved_questions"
                ],
            },
        )

    return report
