from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls.base import reverse
from user.decorators import user_id_check
from user.models import Attendant, Operator
from user.forms import SignUpForm, UpdateForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, get_user_model, login

from meeting.models import Meeting

User = get_user_model()

def signUp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]

            user = authenticate(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )

            
            if form.cleaned_data["role"] == 1:
                user.is_operator = True
                operator = Operator.objects.create(operator_user=user)
                operator.save()
            elif form.cleaned_data["role"] == 2:
                user.is_attendant = True
                attendant = Attendant.objects.create(attendant_user=user)
                attendant.save()

            user.save()

            login(request, user)

            return redirect('home-page')

    else:
        form = SignUpForm()

    context = {
        "form" : form
    }

    return render(request, "registration/signup.html", context)


def user_update(request, pk):
    user = User.objects.get(id=pk)
    form = UpdateForm(instance=user)

    if request.method == "POST":

        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]

            
            user.first_name = first_name
            user.last_name = last_name
            user.username = username

            user.save()
            
            return redirect("home-page")

    else:
        
        context = {
            "form" : form,
            "user" : user,
        }
    return render(request, "user/user-update.html", context)


class PasswordChange(PasswordChangeView):
    model = User
    context_object_name = "form"
    success_url = reverse_lazy('user:password-change-done')

    # def get_success_url(self):
    #     return reverse('')


class password_change_done(PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"



@user_id_check
def user_delete(request, pk, *args, **kwargs):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect("home-page")
    


@user_id_check
def dashboard(request, pk, *args, **kwargs):

    role = kwargs["role"]
    if role == 1:
        operator = Operator.objects.get(operator_user_id=pk)
        meetings = Meeting.objects.filter(operator = operator)

        context = {
            "meetings" : meetings,
            "role" : role,
        }
        return render(request, "user/dashboard.html", context)
        
    elif role == 2:
        attendant = Attendant.objects.get(attendant_user_id=pk)
        meetings  = Meeting.objects.filter(attendants = attendant)

        context = {
            "meetings" : meetings,
            "role" : role,
        }
        
        return render(request, "user/dashboard.html", context)
