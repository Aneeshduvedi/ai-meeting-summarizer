
from django.conf import settings
from django.db import models


class Meeting(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="meetings",
    )
    title = models.CharField(max_length=200, default="Untitled Meeting")
    transcript = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class MeetingReport(models.Model):
    meeting = models.OneToOneField(
        Meeting,
        on_delete=models.CASCADE,
        related_name="report",
    )
    summary = models.TextField(blank=True, default="")
    topics = models.JSONField(default=list, blank=True)
    decisions = models.JSONField(default=list, blank=True)
    action_items = models.JSONField(default=list, blank=True)
    unresolved_questions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report for {self.meeting.title}"
