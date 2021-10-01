from django.urls.conf import path, include
from .views import (
    PasswordChange, 
    dashboard, 
    signUp, 
    user_update,
    user_delete,
    password_change_done,
)

from django.contrib.auth import views as auth_views


app_name = "user"
urlpatterns = [
    #path("", include("django.contrib.auth.urls")),
    path("signup/", signUp, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("modify/<int:pk>/", user_update, name="user-update"),
    path("delete/<int:pk>/", user_delete, name="user-delete"),
    path("password_change/", PasswordChange.as_view(), name="password-change"),
    path("password_change_done/", password_change_done.as_view(), name="password-change-done"),
    path("dashboard/<int:pk>/", dashboard, name="dashboard"),
]