from functools import wraps
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from meeting.models import Meeting
from user.models import Operator, Attendant

User = get_user_model()



def room_check(func):

    wraps(func)
    def wrapper(request, room_name, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        meeting = Meeting.objects.get(path=room_name)
        if user.is_authenticated:
            if user.is_operator:
                operator = Operator.objects.get(operator_user_id = user.id) 
                if meeting.operator == operator:
                    return func(request, room_name, role=1, *args, **kwargs)
                else:
                    raise PermissionDenied
                
            elif user.is_attendant:
                attendant = Attendant.objects.get(attendant_user_id = user.id) 
                if attendant.meeting_set.filter(id=meeting.id).exists():
                    return func(request, room_name, user, role=2, *args, **kwargs)
                else:
                    raise PermissionDenied 
                
        else:
            return redirect("login")
        
    return wrapper