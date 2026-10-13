import datetime
from unittest import mock

import pytz
from django.core.cache import cache
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from pages.custom_context_processor import occurrences_year
from pages.models import Feature
from schedule.models import Calendar, Event, Rule


class FeatureModelTests(SimpleTestCase):
    def test_get_absolute_url_uses_registered_feature_detail_route(self):
        feature = Feature(id=98, title="Test Feature", slug="test-feature")

        self.assertEqual(
            feature.get_absolute_url(),
            reverse("pages:feature_details", args=[98]),
        )


class ActivityOccurrenceTimezoneTests(TestCase):
    def setUp(self):
        cache.delete("ctx:pages:occurrences_year")
        self.arizona = pytz.timezone("America/Phoenix")
        calendar = Calendar.objects.create(name="Club", slug="club")
        rule = Rule.objects.create(
            name="Second Tuesday",
            frequency="MONTHLY",
            params="byweekday:TU;bysetpos:2",
        )
        Event.objects.create(
            calendar=calendar,
            title="Taco Tuesday",
            start=self.arizona.localize(datetime.datetime(2026, 9, 8, 17, 0)),
            end=self.arizona.localize(datetime.datetime(2026, 9, 8, 19, 0)),
            rule=rule,
        )
        every_other_monday = Rule.objects.create(
            name="Every Other Monday",
            frequency="WEEKLY",
            params="byweekday:MO;interval:2",
        )
        Event.objects.create(
            calendar=calendar,
            title="Bunco",
            start=self.arizona.localize(datetime.datetime(2026, 10, 5, 18, 30)),
            end=self.arizona.localize(datetime.datetime(2026, 10, 5, 20, 30)),
            rule=every_other_monday,
        )

    def tearDown(self):
        cache.delete("ctx:pages:occurrences_year")

    def test_activity_recurrences_keep_the_arizona_weekday(self):
        now = self.arizona.localize(datetime.datetime(2026, 10, 1, 12, 0))

        with timezone.override(self.arizona), mock.patch(
            "pages.custom_context_processor.timezone.localtime", return_value=now
        ):
            context = occurrences_year(None)

        taco_dates = [
            timezone.localtime(occurrence.start, self.arizona).date()
            for occurrence in context["activity_year_list"]
            if occurrence.title == "Taco Tuesday"
        ]

        self.assertIn(datetime.date(2026, 10, 13), taco_dates)
        self.assertNotIn(datetime.date(2026, 10, 12), taco_dates)

    def test_every_other_monday_recurrences_stay_on_monday(self):
        now = self.arizona.localize(datetime.datetime(2026, 10, 1, 12, 0))

        with timezone.override(self.arizona), mock.patch(
            "pages.custom_context_processor.timezone.localtime", return_value=now
        ):
            context = occurrences_year(None)

        bunco_dates = [
            timezone.localtime(occurrence.start, self.arizona).date()
            for occurrence in context["activity_year_list"]
            if occurrence.title == "Bunco"
        ]

        self.assertEqual(
            bunco_dates[:2],
            [datetime.date(2026, 10, 5), datetime.date(2026, 10, 19)],
        )
        self.assertTrue(all(date.weekday() == 0 for date in bunco_dates))
