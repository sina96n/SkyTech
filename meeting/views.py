from django.db.models.enums import Choices
from meeting.models import Meeting
from meeting.forms import MeetingForm
from django.shortcuts import redirect, render
from .decorators import (
    operator_check, 
    role_check, 
    operator_required
)

from user.models import Attendant, Operator

import string
import random
from pathlib import Path


lumbers = string.ascii_letters + string.digits

@operator_required
def meeting_create(request):

    if request.method == "POST":
        form = MeetingForm(request.POST, request.FILES)
        if form.is_valid():

            title = form.cleaned_data["title"]
            # date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            thumbnail = form.cleaned_data["thumbnail"]

            operator = Operator.objects.get(operator_user= request.user)

            path = "".join(random.choice(lumbers) for _ in range(50))

            meeting = Meeting.objects.create(
                title=title,
                operator=operator,
                description=description,
                thumbnail=thumbnail,
                path=path,
            )

            meeting.save()

            return redirect("home-page")

    else: 
        form = MeetingForm()

        context = {
            "form" : form,
        }

        return render(request, "meeting/meeting_create.html", context)


@role_check
def meeting_detail(request, pk, *args, **kwargs):
    
    role = kwargs["role"]
    meeting = Meeting.objects.get(id=pk)
    url = f"http://127.0.0.1:8000/meeting/{meeting.path}"
    if role == 1:
        attendants = meeting.attendants.all()
        
        context = {
            "meeting" : meeting,
            "attendants" : attendants,
            "url" : url,
            "role" : role,
        }
        return render(request, "meeting/meeting-detail.html", context)
    elif role == 2:
        context = {
            "meeting" : meeting,
            "url" : url,
            "role" : role,
        }
        return render(request, "meeting/meeting-detail.html", context)


@operator_check
def meeting_update(request, pk):
    meeting = Meeting.objects.get(id=pk)
    form = MeetingForm(instance=meeting)
    if request.method == "POST":
        form = MeetingForm(request.POST, request.FILES)

        if form.is_valid():
            title       = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            
            thumbnail   = form.cleaned_data["thumbnail"]
            if thumbnail == None:
                pass
            else:
                path = Path(meeting.thumbnail.path)
                if path.exists():
                    path.unlink()
                else:
                    pass
                    
                meeting.thumbnail = thumbnail

            meeting.title = title
            meeting.description = description
            
            meeting.save()
            
            return redirect("home-page")
        else:
            return redirect("home-page")
    else:
        context = {
            "form" : form,
            "meeting" : meeting,
        }
        
        return render(request, "meeting/meeting-update.html", context)



@operator_check
def meeting_delete(request, pk):
    if request.method == "POST":
        meeting = Meeting.objects.get(id=pk)
        path = Path(meeting.thumbnail.path)
        if path.exists():
            path.unlink()
        else:
            pass
        meeting.delete()
        return redirect("user:dashboard")
    else:
        return render(request, "meeting/meeting-delete.html")


@operator_check
def kick_user(request, pk, attendant_id, *args, **kwargs):
    meeting = Meeting.objects.get(id=pk)
    attendant = Attendant.objects.get(id=attendant_id)

    meeting.attendants.remove(attendant)
    return redirect("meeting:meeting-detail", pk)