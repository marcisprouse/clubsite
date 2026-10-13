import datetime
from datetime import timedelta

import pytz
from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.utils import timezone

from schedule.admin import (
    EventAdmin,
    EventTimingFilter,
    OccurrenceAdmin,
    OccurrenceTimingFilter,
)
from schedule.models import Calendar, Event, Occurrence, Rule
from schedule.periods import Day, Month


class PeriodOccurrenceSortingTests(TestCase):
    def setUp(self):
        self.calendar = Calendar.objects.create(name="Club", slug="club")
        self.tzinfo = pytz.timezone("America/Phoenix")

    def make_event(self, title, start, end):
        return Event.objects.create(
            calendar=self.calendar,
            title=title,
            start=self.tzinfo.localize(start),
            end=self.tzinfo.localize(end),
        )

    def test_month_day_occurrences_sort_by_start_time(self):
        self.make_event(
            "Early long event",
            datetime.datetime(2026, 4, 7, 8, 0),
            datetime.datetime(2026, 4, 7, 11, 0),
        )
        self.make_event(
            "Later short event",
            datetime.datetime(2026, 4, 7, 8, 45),
            datetime.datetime(2026, 4, 7, 9, 15),
        )

        month = Month(
            self.calendar.events.all(),
            datetime.datetime(2026, 4, 1),
            tzinfo=self.tzinfo,
        )
        day = month.get_day(7)

        self.assertEqual(
            [partial["occurrence"].title for partial in day.get_occurrence_partials()],
            ["Early long event", "Later short event"],
        )

    def test_pooled_occurrences_sort_by_start_time(self):
        early_event = self.make_event(
            "Early pooled event",
            datetime.datetime(2026, 4, 7, 8, 0),
            datetime.datetime(2026, 4, 7, 11, 0),
        )
        later_event = self.make_event(
            "Later pooled event",
            datetime.datetime(2026, 4, 7, 8, 45),
            datetime.datetime(2026, 4, 7, 9, 15),
        )
        early_occurrence = Occurrence(
            event=early_event,
            title=early_event.title,
            start=early_event.start,
            end=early_event.end,
            original_start=early_event.start,
            original_end=early_event.end,
        )
        later_occurrence = Occurrence(
            event=later_event,
            title=later_event.title,
            start=later_event.start,
            end=later_event.end,
            original_start=later_event.start,
            original_end=later_event.end,
        )

        day = Day(
            [],
            datetime.datetime(2026, 4, 7),
            occurrence_pool=[later_occurrence, early_occurrence],
            tzinfo=self.tzinfo,
        )

        self.assertEqual(
            [occurrence.title for occurrence in day.get_occurrences()],
            ["Early pooled event", "Later pooled event"],
        )


class AdminTimingFilterTests(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.calendar = Calendar.objects.create(name="Club", slug="club")
        self.rule = Rule.objects.create(
            name="Monthly", description="Monthly", frequency="MONTHLY"
        )
        self.request = RequestFactory().get("/admin/")

    def event(self, title, start, end, **kwargs):
        return Event.objects.create(
            title=title,
            start=start,
            end=end,
            calendar=self.calendar,
            **kwargs,
        )

    def filter_events(self, timing=None):
        params = {} if timing is None else {"timing": timing}
        timing_filter = EventTimingFilter(
            self.request, params, Event, EventAdmin(Event, admin.site)
        )
        return timing_filter.queryset(self.request, Event.objects.all())

    def filter_occurrences(self, timing=None):
        params = {} if timing is None else {"timing": timing}
        timing_filter = OccurrenceTimingFilter(
            self.request,
            params,
            Occurrence,
            OccurrenceAdmin(Occurrence, admin.site),
        )
        return timing_filter.queryset(self.request, Occurrence.objects.all())

    def test_event_default_shows_upcoming_and_active_recurring_events(self):
        past = self.event(
            "Past",
            self.now - timedelta(days=2),
            self.now - timedelta(days=1),
        )
        upcoming = self.event(
            "Upcoming",
            self.now + timedelta(days=1),
            self.now + timedelta(days=2),
        )
        active_recurring = self.event(
            "Active recurring",
            self.now - timedelta(days=60),
            self.now - timedelta(days=60) + timedelta(hours=1),
            rule=self.rule,
            end_recurring_period=self.now + timedelta(days=60),
        )
        ended_recurring = self.event(
            "Ended recurring",
            self.now - timedelta(days=120),
            self.now - timedelta(days=120) + timedelta(hours=1),
            rule=self.rule,
            end_recurring_period=self.now - timedelta(days=30),
        )

        results = set(self.filter_events())

        self.assertEqual(results, {upcoming, active_recurring})
        self.assertNotIn(past, results)
        self.assertNotIn(ended_recurring, results)

    def test_event_past_and_all_choices_keep_history_available(self):
        past = self.event(
            "Past",
            self.now - timedelta(days=2),
            self.now - timedelta(days=1),
        )
        upcoming = self.event(
            "Upcoming",
            self.now + timedelta(days=1),
            self.now + timedelta(days=2),
        )

        self.assertEqual(set(self.filter_events("past")), {past})
        self.assertEqual(set(self.filter_events("all")), {past, upcoming})

    def test_occurrence_default_hides_past_but_filters_can_reveal_it(self):
        event = self.event(
            "Event",
            self.now - timedelta(days=2),
            self.now + timedelta(days=2),
        )
        past = Occurrence.objects.create(
            event=event,
            title="Past",
            start=self.now - timedelta(days=2),
            end=self.now - timedelta(days=1),
            original_start=self.now - timedelta(days=2),
            original_end=self.now - timedelta(days=1),
        )
        upcoming = Occurrence.objects.create(
            event=event,
            title="Upcoming",
            start=self.now + timedelta(days=1),
            end=self.now + timedelta(days=2),
            original_start=self.now + timedelta(days=1),
            original_end=self.now + timedelta(days=2),
        )

        self.assertEqual(set(self.filter_occurrences()), {upcoming})
        self.assertEqual(set(self.filter_occurrences("past")), {past})
        self.assertEqual(set(self.filter_occurrences("all")), {past, upcoming})
