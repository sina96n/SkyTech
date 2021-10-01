from user.models import Attendant, Operator
from django.contrib import admin

from django.contrib.auth import get_user_model

User = get_user_model()

class userAdmin(admin.ModelAdmin):
    fieldsets=(
        ("User Info", {
            "fields" : (
                "first_name", "last_name", "email", "username", "password"
            )
        }),

        ("Permissions", {
            "fields" : (
                "is_active", "is_staff", "is_superuser", "is_operator", "is_attendant", "groups", "user_permissions"
            )
        }),

        ("Important date(s)", {
            "fields" : (
                "last_login", "date_joined"
            )
        }),
    )

    add_fieldsets = (
        ("User Info", {
            "fields" : (
                "first_name", "last_name", "username", "password"
            )
        }),
    )

    list_display = (
        "last_name",
        "first_name",
        "username",
        "email",
        "last_login",
    )

    search_fields = (
        "username",
        "last_name",
        "first-name",
    )

    list_filter = (
        "is_attendant",
        "is_operator",
        "date_joined",)

    ordering = (
        "last_name",
        "first_name",
    )


# class operatorAdmin(admin.ModelAdmin):

#     list_display = (
#         "operator_user.last_name",
#         "operator_user.first_name",
#         "operator_user.username",
#         "operator_user.email",
#         "operator_user.last_login",
#     )

#     search_fields = (
#         "operator_user.username",
#         "operator_user.last_name",
#         "operator_user.first-name",
#     )

#     list_filter = (
#         "operator_user.date_joined",
#     )

#     ordering = (
#         "operator_user.last_name",
#         "operator_user.first_name",
#     )




admin.site.register(User, userAdmin)
admin.site.register(Operator)
admin.site.register(Attendant)


