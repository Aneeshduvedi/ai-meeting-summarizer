
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from .forms import MeetingForm
from .models import Meeting, MeetingReport
from .services.meeting_workflow import summarize_meeting


@login_required
def dashboard_view(request):
    search_query = request.GET.get("q", "").strip()
    from_date = request.GET.get("from_date", "").strip()
    to_date = request.GET.get("to_date", "").strip()
    sort_by = request.GET.get("sort", "newest").strip()

    # Available sorting options
    sort_options = {
        "newest": "-created_at",
        "oldest": "created_at",
        "title_asc": "title",
        "title_desc": "-title",
    }

    # Default to newest first if the option is invalid
    if sort_by not in sort_options:
        sort_by = "newest"

    order_field = sort_options[sort_by]

    # Show only the logged-in user's meetings
    meetings = request.user.meetings.all()

    # Dashboard statistics for the logged-in user
    user_meetings = request.user.meetings.all()
    total_meetings = user_meetings.count()

    reports_generated = MeetingReport.objects.filter(
        meeting__user=request.user
    ).count()

    pending_meetings = total_meetings - reports_generated

    # Calculate report generation rate
    report_generation_rate = (
        round((reports_generated / total_meetings) * 100, 1)
        if total_meetings > 0
        else 0
    )

    # Search meetings by title
    if search_query:
        meetings = meetings.filter(title__icontains=search_query)

    # Filter meetings by start date
    if from_date:
        meetings = meetings.filter(
            created_at__date__gte=from_date
        )

    # Filter meetings by end date
    if to_date:
        meetings = meetings.filter(
            created_at__date__lte=to_date
        )

    # Apply sorting
    meetings = meetings.order_by(order_field, "id")

    # Pagination: display 5 meetings per page
    paginator = Paginator(meetings, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "meetings/dashboard.html",
        {
            "meetings": page_obj,
            "page_obj": page_obj,
            "paginator": paginator,
            "search_query": search_query,
            "from_date": from_date,
            "to_date": to_date,
            "sort_by": sort_by,

            # Dashboard summary statistics
            "total_meetings": total_meetings,
            "reports_generated": reports_generated,
            "pending_meetings": pending_meetings,
            "report_generation_rate": report_generation_rate,
        },
    )


@login_required
def create_meeting_view(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)

        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.user = request.user
            meeting.save()

            messages.success(
                request,
                "Meeting transcript saved successfully."
            )
            return redirect("dashboard")
    else:
        form = MeetingForm()

    return render(
        request,
        "meetings/meeting_form.html",
        {"form": form},
    )


@login_required
def edit_meeting_view(request, meeting_id):
    meeting = get_object_or_404(
        Meeting,
        id=meeting_id,
        user=request.user,
    )

    original_transcript = meeting.transcript

    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)

        if form.is_valid():
            updated_meeting = form.save(commit=False)

            transcript_changed = (
                updated_meeting.transcript != original_transcript
            )

            updated_meeting.save()

            if transcript_changed:
                MeetingReport.objects.filter(
                    meeting=updated_meeting
                ).delete()

                messages.success(
                    request,
                    "Meeting updated. The transcript changed, so the old "
                    "report was removed. Generate a new report when ready."
                )
            else:
                messages.success(
                    request,
                    "Meeting details updated successfully."
                )

            return redirect("dashboard")
    else:
        form = MeetingForm(instance=meeting)

    return render(
        request,
        "meetings/meeting_form.html",
        {
            "form": form,
            "editing": True,
            "meeting": meeting,
        },
    )


@login_required
def summarize_meeting_view(request, meeting_id):
    if request.method != "POST":
        return redirect("dashboard")

    meeting = get_object_or_404(
        Meeting,
        id=meeting_id,
        user=request.user,
    )

    if hasattr(meeting, "report"):
        messages.info(
            request,
            "A report already exists for this meeting."
        )
        return redirect(
            "meeting_detail",
            meeting_id=meeting.id,
        )

    try:
        summarize_meeting(meeting)

        messages.success(
            request,
            "Meeting report generated and saved successfully."
        )

        return redirect(
            "meeting_detail",
            meeting_id=meeting.id,
        )

    except (ValueError, RuntimeError) as exc:
        print("MEETING REPORT ERROR:", repr(exc))
        messages.error(request, str(exc))

    except Exception as exc:
        import traceback

        print("UNEXPECTED MEETING REPORT ERROR:", repr(exc))
        traceback.print_exc()

        messages.error(
            request,
            "Unable to generate the report. Check the server terminal."
        )

    return redirect("dashboard")


@login_required
def meeting_detail_view(request, meeting_id):
    meeting = get_object_or_404(
        Meeting,
        id=meeting_id,
        user=request.user,
    )

    report = get_object_or_404(
        MeetingReport,
        meeting=meeting,
    )

    return render(
        request,
        "meetings/meeting_detail.html",
        {
            "meeting": meeting,
            "report": report,
        },
    )


@login_required
def delete_meeting_view(request, meeting_id):
    if request.method != "POST":
        return redirect("dashboard")

    meeting = get_object_or_404(
        Meeting,
        id=meeting_id,
        user=request.user,
    )

    meeting_title = meeting.title
    meeting.delete()

    messages.success(
        request,
        f'Meeting "{meeting_title}" and its associated report '
        "have been deleted successfully.",
    )

    return redirect("dashboard")


@login_required
def download_meeting_report_view(request, meeting_id):
    # Allow access only to the logged-in user's meeting
    meeting = get_object_or_404(
        Meeting,
        id=meeting_id,
        user=request.user,
    )

    # A report must exist before it can be downloaded
    report = get_object_or_404(
        MeetingReport,
        meeting=meeting,
    )

    def safe_text(value):
        return (
            str(value if value is not None else "Not specified")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )

    # Create the PDF in memory
    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    # Meeting title and creation date
    story.append(
        Paragraph(safe_text(meeting.title), styles["Title"])
    )
    story.append(
        Paragraph(
            f"Created: {meeting.created_at.strftime('%d %b %Y, %I:%M %p')}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 16))

    # Original transcript
    story.append(
        Paragraph("Meeting Transcript", styles["Heading2"])
    )
    story.append(
        Paragraph(
            safe_text(meeting.transcript),
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 16))

    # Meeting summary
    story.append(
        Paragraph("Summary", styles["Heading2"])
    )
    story.append(
        Paragraph(
            safe_text(report.summary),
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    # Topics, decisions, and unresolved questions
    sections = [
        ("Topics Discussed", report.topics),
        ("Decisions Made", report.decisions),
        ("Unresolved Questions", report.unresolved_questions),
    ]

    for heading, items in sections:
        story.append(
            Paragraph(heading, styles["Heading2"])
        )

        if items:
            for item in items:
                story.append(
                    Paragraph(
                        f"&bull; {safe_text(item)}",
                        styles["BodyText"],
                    )
                )
                story.append(Spacer(1, 4))
        else:
            story.append(
                Paragraph("None recorded.", styles["BodyText"])
            )

        story.append(Spacer(1, 12))

    # Action items table
    story.append(
        Paragraph("Action Items", styles["Heading2"])
    )

    action_items = report.action_items or []

    if action_items:
        table_data = [
            [
                Paragraph("<b>Task</b>", styles["BodyText"]),
                Paragraph("<b>Owner</b>", styles["BodyText"]),
                Paragraph("<b>Deadline</b>", styles["BodyText"]),
            ]
        ]

        for item in action_items:
            if isinstance(item, dict):
                task = item.get("task", "Not specified")
                owner = item.get("owner", "Not specified")
                deadline = item.get("deadline", "Not specified")
            else:
                task = str(item)
                owner = "Not specified"
                deadline = "Not specified"

            table_data.append([
                Paragraph(safe_text(task), styles["BodyText"]),
                Paragraph(safe_text(owner), styles["BodyText"]),
                Paragraph(safe_text(deadline), styles["BodyText"]),
            ])

        action_table = Table(
            table_data,
            colWidths=[250, 100, 100],
            repeatRows=1,
        )

        action_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1D4ED8"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(action_table)
    else:
        story.append(
            Paragraph(
                "No action items recorded.",
                styles["BodyText"],
            )
        )

    # Generate the PDF
    pdf.build(story)
    buffer.seek(0)

    # Return it as a downloadable file
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="meeting_report_{meeting.id}.pdf"'
    )

    buffer.close()

    return response
