
from django import forms
from .models import Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["title", "transcript"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter meeting title",
                }
            ),
            "transcript": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 12,
                    "placeholder": "Paste the meeting transcript here...",
                }
            ),
        }

    def clean_transcript(self):
        transcript = self.cleaned_data["transcript"].strip()

        if not transcript:
            raise forms.ValidationError(
                "Please enter a meeting transcript."
            )

        return transcript
