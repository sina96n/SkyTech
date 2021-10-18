from functools import wraps

from django.core.exceptions import PermissionDenied
from meeting.models import Meeting
from user.models import Attendant, Operator
from django.shortcuts import HttpResponseRedirect


def operator_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_operator:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")
    return wrap

def attandent_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_operator:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")
    return wrap

def role_check(func):
    @wraps(func)
    def wrap(request, pk, *args, **kwargs):
        user = request.user
        meeting = Meeting.objects.get(id=pk)
        if user.is_authenticated and user.is_operator:
            operator = Operator.objects.get(operator_user_id = user.id) 
            if meeting.operator == operator:
                return func(request, pk, role=1)
            else:
                raise PermissionDenied
        elif user.is_authenticated and user.is_attendant:
            attendant = Attendant.objects.get(attendant_user_id = user.id) 
            if attendant.meeting_set.filter(id=meeting.id).exists():
                return func(request, pk, role=2)
            else:
                return func(request, pk, role=3)
    return wrap


def operator_check(func):
    @wraps(func)
    def wrap(request, pk, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_operator:
            operator = Operator.objects.get(operator_user_id = user.id) 
            meeting = Meeting.objects.get(id=pk)
            if meeting.operator == operator:
                return func(request, pk, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    return wrap