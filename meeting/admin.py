from meeting.models import Meeting
from django.contrib import admin
from django.contrib.admin.filters import ListFilter


class meetingAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Meeting Info", {
                "fields" : (
                    ("title", "operator",  "description", "thumbnail", "is_open")
                )
            }
        ),

        (
            "Attendants", {
                "fields" : (
                    ("attendants",)
                )
            }
        ),
        (
            "Path", {
                "fields" : (
                    ("path",)
                )
            }
        ),
    )

    list_display = (
        "title",
        "operator",
        # "date",
        "is_open",
        "attendants_count",
    )

    list_filter = (
        "is_open",
    )

    search_fields = (
        "title",
        "operator",
    )

    def attendants_count(self, obj):
        return obj.attendants.all().count()


admin.site.register(Meeting, meetingAdmin)