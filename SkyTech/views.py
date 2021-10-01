from meeting.models import Meeting
from django.shortcuts import render

def home_page(request):

    meetings = Meeting.objects.all()

    context = {
        "meetings" : meetings,
    }
    return render(request, "home-page.html", context)