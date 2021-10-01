from django.urls.conf import path
from .views import (
    kick_user,
    meeting_create, 
    meeting_delete, 
    meeting_detail, 
    meeting_update,
    )


app_name = "meeting"
urlpatterns = [
    path("create/", meeting_create, name='meeting-create'),
    path("<int:pk>/", meeting_detail, name='meeting-detail'),
    path("delete/<int:pk>/", meeting_delete, name='meeting-delete'),
    path("update/<int:pk>/", meeting_update, name='meeting-update'),
    path("kick/<int:pk>/<int:attendant_id>/", kick_user, name='kick-user'),
]