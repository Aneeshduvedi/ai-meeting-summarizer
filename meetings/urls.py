
from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.dashboard_view,
        name="dashboard",
    ),
    path(
        "meetings/new/",
        views.create_meeting_view,
        name="create_meeting",
    ),
    path(
        "meetings/<int:meeting_id>/edit/",
        views.edit_meeting_view,
        name="edit_meeting",
    ),
    path(
        "meetings/<int:meeting_id>/summarize/",
        views.summarize_meeting_view,
        name="summarize_meeting",
    ),
    path(
        "meetings/<int:meeting_id>/report/",
        views.meeting_detail_view,
        name="meeting_detail",
    ),
    path(
        "meetings/<int:meeting_id>/report/download/",
        views.download_meeting_report_view,
        name="download_meeting_report",
    ),
    path(
        "meetings/<int:meeting_id>/delete/",
        views.delete_meeting_view,
        name="delete_meeting",
    ),
]
