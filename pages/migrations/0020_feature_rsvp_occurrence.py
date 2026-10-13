import re
import unicodedata

import pytz
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


DIRECT_RSVP_PATTERN = re.compile(r"/activity/respond/(\d+)(?=[/?#)\s]|$)", re.IGNORECASE)


def _normalize_title(value):
    value = unicodedata.normalize("NFKD", value or "")
    return "".join(character.lower() for character in value if character.isalnum())


def _title_words(value):
    ignored_words = {"activity", "event", "featured", "flyer", "the"}
    return {
        word.lower()
        for word in re.findall(r"[A-Za-z0-9]+", value or "")
        if len(word) >= 4 and word.lower() not in ignored_words
    }


def _local_date(value, club_timezone):
    if timezone.is_naive(value):
        value = club_timezone.localize(value)
    return timezone.localtime(value, club_timezone).date()


def backfill_feature_rsvp_occurrences(apps, schema_editor):
    Feature = apps.get_model("pages", "Feature")
    Occurrence = apps.get_model("schedule", "Occurrence")
    club_timezone = pytz.timezone("America/Phoenix")

    rsvp_occurrences = list(
        Occurrence.objects.filter(rsvp=True).select_related("event")
    )
    occurrences_by_id = {occurrence.pk: occurrence for occurrence in rsvp_occurrences}

    features = Feature.objects.filter(
        description__icontains="/activity/respond",
        rsvp_occurrence__isnull=True,
    )

    for feature in features.iterator():
        direct_match = DIRECT_RSVP_PATTERN.search(feature.description or "")
        if direct_match:
            occurrence = occurrences_by_id.get(int(direct_match.group(1)))
            if occurrence:
                feature.rsvp_occurrence_id = occurrence.pk
                feature.save(update_fields=["rsvp_occurrence"])
                continue

        feature_title = _normalize_title(feature.title)
        feature_date = _local_date(feature.feature_day_time, club_timezone)
        same_date_occurrences = []

        for occurrence in rsvp_occurrences:
            if _local_date(occurrence.start, club_timezone) != feature_date:
                continue
            same_date_occurrences.append(occurrence)

        exact_matches = []
        for occurrence in same_date_occurrences:
            occurrence_titles = {
                _normalize_title(occurrence.title),
                _normalize_title(occurrence.event.title),
            }
            if feature_title and feature_title in occurrence_titles:
                exact_matches.append(occurrence)

        if len(exact_matches) == 1:
            feature.rsvp_occurrence_id = exact_matches[0].pk
            feature.save(update_fields=["rsvp_occurrence"])
            continue

        feature_words = _title_words(feature.title)
        word_matches = []
        for occurrence in same_date_occurrences:
            occurrence_words = _title_words(occurrence.title) | _title_words(
                occurrence.event.title
            )
            if feature_words & occurrence_words:
                word_matches.append(occurrence)

        if len(word_matches) == 1:
            feature.rsvp_occurrence_id = word_matches[0].pk
            feature.save(update_fields=["rsvp_occurrence"])


def clear_feature_rsvp_occurrences(apps, schema_editor):
    Feature = apps.get_model("pages", "Feature")
    Feature.objects.update(rsvp_occurrence=None)


class Migration(migrations.Migration):

    dependencies = [
        ("schedule", "0036_alter_memberrsvp_mealchoice"),
        ("pages", "0019_feature_is_landscape"),
    ]

    operations = [
        migrations.AddField(
            model_name="feature",
            name="rsvp_occurrence",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional: select the saved occurrence for this featured event. The site will create the correct direct RSVP link automatically.",
                limit_choices_to={"rsvp": True},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="features",
                to="schedule.occurrence",
            ),
        ),
        migrations.AlterField(
            model_name="feature",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Add information that is not already on the flyer. To make a link, use [text](full website address) with no space between the brackets and parentheses. Select an RSVP occurrence below instead of manually entering a general RSVP link.",
                null=True,
            ),
        ),
        migrations.RunPython(
            backfill_feature_rsvp_occurrences,
            clear_feature_rsvp_occurrences,
        ),
    ]
