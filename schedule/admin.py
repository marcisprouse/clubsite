from django.contrib import admin
from django.db.models import Q
from django.utils import timezone

from schedule.forms import EventAdminForm, OccurrenceAdminForm
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


class TimingFilter(admin.SimpleListFilter):
    """Keep old calendar records available without cluttering the default view."""

    title = "timing"
    parameter_name = "timing"

    def lookups(self, request, model_admin):
        return (
            ("current", "Current & upcoming"),
            ("past", "Past"),
            ("all", "All"),
        )

    def choices(self, changelist):
        # Django normally inserts its own "All" option. These explicit choices
        # let Current & upcoming remain the uncluttered default instead.
        selected_value = self.value() or "current"
        for lookup, title in self.lookup_choices:
            yield {
                "selected": selected_value == lookup,
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }


class EventTimingFilter(TimingFilter):
    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "all":
            return queryset
        if self.value() == "past":
            return queryset.filter(
                Q(rule__isnull=True, end__lt=now)
                | Q(
                    rule__isnull=False,
                    end_recurring_period__isnull=False,
                    end_recurring_period__lt=now,
                )
            )
        return queryset.filter(
            Q(rule__isnull=True, end__gte=now)
            | Q(rule__isnull=False, end_recurring_period__isnull=True)
            | Q(rule__isnull=False, end_recurring_period__gte=now)
        )


class OccurrenceTimingFilter(TimingFilter):
    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "all":
            return queryset
        if self.value() == "past":
            return queryset.filter(end__lt=now)
        return queryset.filter(end__gte=now)


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
    list_filter = (EventTimingFilter, "start")
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
    form = OccurrenceAdminForm
    list_display = ("title", "exclude", "cancelled", "start", "end")
    ordering = ("-start",)
    date_hierarchy = 'start'
    list_filter = (OccurrenceTimingFilter, "title")
    search_fields = ('title', 'event__title')


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
