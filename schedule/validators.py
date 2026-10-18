import re

from django.core.exceptions import ValidationError


RSVP_URL = (
    r"(?:https?://(?:www\.)?coyotelakesrecreationclub\.org)?"
    r"/activity/respond(?:/\d+)?/?(?:[?#][^\s)]*)?"
)
RSVP_URL_PATTERN = re.compile(RSVP_URL, flags=re.IGNORECASE)
RSVP_MARKDOWN_LINK_PATTERN = re.compile(
    r"\[[^\]\r\n]+\]\(\s*" + RSVP_URL + r"\s*\)",
    flags=re.IGNORECASE,
)


def validate_rsvp_link_format(value):
    """Reject RSVP URLs that are not inside a complete Markdown link."""
    value = value or ""
    text_without_valid_links = RSVP_MARKDOWN_LINK_PATTERN.sub(
        "", value
    )
    if RSVP_URL_PATTERN.search(text_without_valid_links):
        raise ValidationError(
            "This RSVP link is not formatted correctly. Either select an RSVP "
            "occurrence or use: [RSVP Here]"
            "(https://www.coyotelakesrecreationclub.org/activity/respond)"
        )
    return value
