from django.contrib import admin

from schedule.forms import EventAdminForm
from schedule.models import (
    Calendar,
    CalendarRelation,
    Event,
    EventRelation,
    Occurrence,
    Rule,
    Volunteer,
    Memberrsvp
)


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    fieldsets = ((None, {"fields": [("name", "slug")]}),)


@admin.register(CalendarRelation)
class CalendarRelationAdmin(admin.ModelAdmin):
    list_display = ("calendar", "content_object")
    list_filter = ("inheritable",)
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "calendar",
                    ("content_type", "object_id", "distinction"),
                    "inheritable",
                ]
            },
        ),
    )


@admin.register(EventRelation)
class EventRelationAdmin(admin.ModelAdmin):
    list_display = ("event", "content_object", "distinction")
    fieldsets = (
        (None, {"fields": ["event", ("content_type", "object_id", "distinction")]}),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "exclude", "start", "end")
    list_filter = ("start",)
    ordering = ("-start",)
    date_hierarchy = "start"
    search_fields = ("title", "description")
    fieldsets = (
        (
            None,
            {
                "fields": [
                    ("title",),
                    ("exclude",),
                    ("description",),
                    ("start", "end"),
                    ("creator", "calendar"),
                    ("rule", "end_recurring_period"),
                ]
            },
        ),
    )
    form = EventAdminForm


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ("title", "exclude", "cancelled", "start", "end")
    ordering = ("-start",)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("text", "occurrence", "owner")
    ordering = ("-created_at",)


@admin.register(Memberrsvp)
class MemberrsvpAdmin(admin.ModelAdmin):
    list_display = ("owner", "attending", "occurrence", "guests", "bringing", "mealchoice")
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": [
                    ("owner",),
                    ("attending",),
                    ("occurrence",),
                    ("guests"),
                    ("bringing"),
                    ("mealchoice"),
                ]
            },
        ),
    )


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("frequency",)
    search_fields = ("name", "description")
