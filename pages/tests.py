import datetime
import importlib
from unittest import mock

import pytz
from django.apps import apps as django_apps
from django.core.cache import cache
from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from pages.custom_context_processor import occurrences_year
from pages.models import Feature
from schedule.models import Calendar, Event, Occurrence, Rule


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


class FeatureRsvpOccurrenceTests(TestCase):
    def setUp(self):
        self.arizona = pytz.timezone("America/Phoenix")
        calendar = Calendar.objects.create(name="Club", slug="club")
        start = self.arizona.localize(datetime.datetime(2026, 11, 10, 17, 0))
        end = self.arizona.localize(datetime.datetime(2026, 11, 10, 19, 0))
        event = Event.objects.create(
            calendar=calendar,
            title="Taco Tuesday",
            start=start,
            end=end,
        )
        self.occurrence = Occurrence.objects.create(
            event=event,
            title="Taco Tuesday",
            start=start,
            end=end,
            original_start=start,
            original_end=end,
            rsvp=True,
        )

    def make_feature(self, **overrides):
        values = {
            "title": "Taco Tuesday",
            "slug": "taco-tuesday",
            "feature_day_time": self.occurrence.start,
            "feature_location": "",
            "is_landscape": False,
        }
        values.update(overrides)
        return Feature.objects.create(**values)

    def test_generic_rsvp_link_resolves_to_selected_occurrence(self):
        original_description = (
            "Please [RSVP Here]"
            "(https://www.coyotelakesrecreationclub.org/activity/respond)."
        )
        feature = self.make_feature(
            description=original_description,
            rsvp_occurrence=self.occurrence,
        )

        self.assertIn(
            "/activity/respond/{})".format(self.occurrence.pk),
            feature.resolved_description,
        )
        self.assertEqual(feature.description, original_description)
        self.assertTrue(feature.description_has_rsvp_link)

    def test_feature_without_typed_link_gets_direct_rsvp_button(self):
        feature = self.make_feature(
            description="Event details are on the flyer.",
            rsvp_occurrence=self.occurrence,
        )

        rendered = render_to_string(
            "pages/feature_detail.html",
            {"feature": feature},
        )

        self.assertIn('href="/activity/respond/{}"'.format(self.occurrence.pk), rendered)
        self.assertIn("RSVP Here", rendered)

    def test_data_migration_backfills_only_confident_matches(self):
        direct_feature = self.make_feature(
            slug="direct-taco",
            description="[RSVP](/activity/respond/{})".format(self.occurrence.pk),
        )
        title_and_date_feature = self.make_feature(
            title="Taco Dinner Flyer",
            slug="matched-taco",
            description="[RSVP](/activity/respond)",
        )
        unmatched_feature = self.make_feature(
            title="Different Event",
            slug="different-event",
            description="[RSVP](/activity/respond)",
        )
        migration = importlib.import_module(
            "pages.migrations.0020_feature_rsvp_occurrence"
        )

        migration.backfill_feature_rsvp_occurrences(django_apps, None)

        direct_feature.refresh_from_db()
        title_and_date_feature.refresh_from_db()
        unmatched_feature.refresh_from_db()
        self.assertEqual(direct_feature.rsvp_occurrence, self.occurrence)
        self.assertEqual(title_and_date_feature.rsvp_occurrence, self.occurrence)
        self.assertIsNone(unmatched_feature.rsvp_occurrence)
