import datetime

import pytz
from django.test import TestCase

from schedule.models import Calendar, Event, Occurrence
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
