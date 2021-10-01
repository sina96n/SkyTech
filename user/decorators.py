from functools import wraps
from django.shortcuts import HttpResponseRedirect, redirect
from django.core.exceptions import PermissionDenied



def user_id_check(func):
    @wraps(func)
    def wrap(request, pk, *args, **kwargs):
        user = request.user 
        if user.is_authenticated:
            if user.id == pk:
                if user.is_operator:
                    return func(request, pk, role=1)
                elif user.is_attendant:
                    return func(request, pk, role=2)
            else:
                return PermissionDenied
        else:
            return redirect("login")
    return wrap