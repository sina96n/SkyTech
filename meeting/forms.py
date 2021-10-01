from django import forms
from django.db.models import fields
from .models import Meeting

class MeetingForm(forms.ModelForm):

    class Meta:
        model = Meeting
        fields = (
            "title",
            # "date",
            "description",
            "thumbnail",
        )