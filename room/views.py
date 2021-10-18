from typing_extensions import ParamSpec
from django.shortcuts import render

from .decorators import room_check
from meeting.models import Meeting

from django.contrib.auth import get_user_model

User = get_user_model()


@room_check
def room(request, room_name, *args, **kwargs):

    role = kwargs["role"]
    user = User.objects.get(id=request.user.id)
    meeting = Meeting.objects.get(path=room_name)
    # if role == 1:
    #     pass
    # elif role == 2:
    #     pass

    context = {
        "room_name": room_name,
        "user" : user,
        "meeting" : meeting,
        "role" : role,
    }
    return render(request, "room/room.html", context)