
from __future__ import absolute_import
from __future__ import print_function
import datetime
from django.conf import settings
from django import template
from django.urls import reverse
from django.utils.dateformat import format
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from schedule.models import Calendar
from schedule.periods import weekday_names, weekday_abbrs
from six.moves import range

from django.utils import timezone

from django.utils.html import escape

#markdown
import markdown



from schedule.settings import (
    CHECK_CALENDAR_PERM_FUNC,
    CHECK_EVENT_PERM_FUNC,
    SCHEDULER_PREVNEXT_LIMIT_SECONDS,
)

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.inclusion_tag("schedule/_month_table.html", takes_context=True)
def month_table(context, calendar, month, size="regular", shift=None):
    if shift:
        if shift == -1:
            month = month.prev()
        if shift == 1:
            month = next(month)
    if size == "small":
        context["day_names"] = weekday_abbrs
    else:
        context["day_names"] = weekday_names
    context["calendar"] = calendar
    context["month"] = month
    context["size"] = size
    return context

@register.inclusion_tag("schedule/_month_table_tri.html", takes_context=True)
def month_table_tri(context, calendar, month, size="regular", shift=None):
    if shift:
        if shift == -1:
            month = month.prev()
        if shift == 1:
            month = next(month)
    if size == "small":
        context["day_names"] = weekday_abbrs
    else:
        context["day_names"] = weekday_names
    context["calendar"] = calendar
    context["month"] = month
    context["size"] = size
    return context

@register.inclusion_tag("schedule/_month_table_year.html", takes_context=True)
def month_table_year(context, calendar, month, size="regular", shift=None):
    if shift:
        if shift == -1:
            month = month.prev()
        if shift == 1:
            month = next(month)
    if size == "small":
        context["day_names"] = weekday_abbrs
    else:
        context["day_names"] = weekday_names
    context["calendar"] = calendar
    context["month"] = month
    context["size"] = size
    return context


@register.inclusion_tag("schedule/_day_cell.html", takes_context=True)
def day_cell(context, calendar, day, month, size="regular"):
    context.update({"calendar": calendar, "day": day, "month": month, "size": size})
    return context


@register.inclusion_tag("schedule/_daily_table.html", takes_context=True)
def daily_table(context, day, start=8, end=23, increment=30):
    """
    Display a nice table with occurrences and action buttons.
    Arguments:
    start - hour at which the day starts
    end - hour at which the day ends
    increment - size of a time slot (in minutes)
    """
    user = context["request"].user
    addable = CHECK_EVENT_PERM_FUNC(None, user)
    if "calendar" in context:
        addable = addable and CHECK_CALENDAR_PERM_FUNC(context["calendar"], user)
    context["addable"] = addable
    day_part = day.get_time_slot(
        day.start + datetime.timedelta(hours=start),
        day.start + datetime.timedelta(hours=end),
    )
    # get slots to display on the left
    slots = _cook_slots(day_part, increment)
    context["slots"] = slots
    return context


@register.inclusion_tag("schedule/_event_title.html", takes_context=True)
def title(context, occurrence):
    context.update({"occurrence": occurrence})
    return context


@register.inclusion_tag("schedule/_event_options.html", takes_context=True)
def options(context, occurrence):
    context.update(
        {"occurrence": occurrence, "MEDIA_URL": getattr(settings, "MEDIA_URL")}
    )
    context["view_occurrence"] = occurrence.get_absolute_url()
    user = context["request"].user
    if CHECK_EVENT_PERM_FUNC(occurrence.event, user) and CHECK_CALENDAR_PERM_FUNC(
        occurrence.event.calendar, user
    ):
        context["edit_occurrence"] = occurrence.get_edit_url()
        context["cancel_occurrence"] = occurrence.get_cancel_url()
        context["delete_event"] = reverse("delete_event", args=(occurrence.event.id,))
        context["edit_event"] = reverse(
            "edit_event", args=(occurrence.event.calendar.slug, occurrence.event.id)
        )
    else:
        context["edit_event"] = context["delete_event"] = ""
    return context


@register.inclusion_tag("schedule/_create_event_options.html", takes_context=True)
def create_event_url(context, calendar, slot):
    context.update({"calendar": calendar, "MEDIA_URL": getattr(settings, "MEDIA_URL")})
    lookup_context = {"calendar_slug": calendar.slug}
    context["create_event_url"] = "{}{}".format(
        reverse("calendar_create_event", kwargs=lookup_context),
        querystring_for_date(slot),
    )
    return context


class CalendarNode(template.Node):
    def __init__(self, content_object, distinction, context_var, create=False):
        self.content_object = template.Variable(content_object)
        self.distinction = distinction
        self.context_var = context_var

    def render(self, context):
        Calendar.objects.get_calendar_for_object(
            self.content_object.resolve(context), self.distinction
        )
        context[self.context_var] = Calendar.objects.get_calendar_for_object(
            self.content_object.resolve(context), self.distinction
        )
        return ""


@register.tag
def get_calendar(parser, token):
    contents = token.split_contents()
    if len(contents) == 4:
        _, content_object, _, context_var = contents
        distinction = None
    elif len(contents) == 5:
        _, content_object, distinction, _, context_var = token.split_contents()
    else:
        raise template.TemplateSyntaxError(
            "%r tag follows form %r <content_object> as <context_var>"
            % (token.contents.split()[0], token.contents.split()[0])
        )
    return CalendarNode(content_object, distinction, context_var)


class CreateCalendarNode(template.Node):
    def __init__(self, content_object, distinction, context_var, name):
        self.content_object = template.Variable(content_object)
        self.distinction = distinction
        self.context_var = context_var
        self.name = name

    def render(self, context):
        context[self.context_var] = Calendar.objects.get_or_create_calendar_for_object(
            self.content_object.resolve(context), self.distinction, name=self.name
        )
        return ""


@register.tag
def get_or_create_calendar(parser, token):
    contents = token.split_contents()
    if len(contents) > 2:
        obj = contents[1]
        if "by" in contents:
            by_index = contents.index("by")
            distinction = contents[by_index + 1]
        else:
            distinction = None
        if "named" in contents:
            named_index = contents.index("named")
            name = contents[named_index + 1]
            if name[0] == name[-1]:
                name = name[1:-1]
        else:
            name = None
        if "as" in contents:
            as_index = contents.index("as")
            context_var = contents[as_index + 1]
        else:
            raise template.TemplateSyntaxError(
                "%r tag requires an a context variable: %r <content_object> [named <calendar name>] [by <distinction>] as <context_var>"
                % (token.split_contents()[0], token.split_contents()[0])
            )
    else:
        raise template.TemplateSyntaxError(
            "%r tag follows form %r <content_object> [named <calendar name>] [by <distinction>] as <context_var>"
            % (token.split_contents()[0], token.split_contents()[0])
        )
    return CreateCalendarNode(obj, distinction, context_var, name)


@register.simple_tag
@register.filter(needs_autoescape=True)
def querystring_for_date(date, num=6, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    query_string = '?'
    qs_parts = ['year=%d', 'month=%d', 'day=%d', 'hour=%d', 'minute=%d', 'second=%d']
    qs_vars = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    query_string += esc('&'.join(qs_parts[:num]) % qs_vars[:num])
    return mark_safe(query_string)


''' previous and next url for month '''

@register.simple_tag
def prev_url(target, calendar, period):
    now = timezone.now()
    delta = now - period.prev().start
    slug = calendar.slug
    target = 'month_calendar'
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-left"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.prev().start),
        )
    )


@register.simple_tag
def next_url(target, calendar, period):
    now = timezone.now()
    slug = calendar.slug
    target = 'month_calendar'
    delta = period.next().start - now
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-right"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.next().start),
        )
    )


@register.inclusion_tag("schedule/_prevnext.html")
def prevnext(target, calendar, period, fmt=None):
    if fmt is None:
        fmt = settings.DATE_FORMAT
    context = {
        "calendar": calendar,
        "period": period,
        "period_name": format(period.start, fmt),
        "target": target,
    }
    return context


''' end previous and next url for month '''


''' previous and next url for year '''

@register.simple_tag
def prev_url_year(target, calendar, period):
    now = timezone.now()
    delta = now - period.prev().start
    slug = calendar.slug
    target = 'year_calendar'
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-left"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.prev().start),
        )
    )


@register.simple_tag
def next_url_year(target, calendar, period):
    now = timezone.now()
    slug = calendar.slug
    target = 'year_calendar'
    delta = period.next().start - now
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-right"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.next().start),
        )
    )


@register.inclusion_tag("schedule/_prevnext_year.html")
def prevnext_year(target, calendar, period, fmt=None):
    if fmt is None:
        fmt = settings.DATE_FORMAT
    context = {
        "calendar": calendar,
        "period": period,
        "period_name": format(period.start, fmt),
        "target": target,
    }
    return context


''' end previous and next url for year '''


''' previous and next url for day '''

@register.simple_tag
def prev_url_day(target, calendar, period):
    now = timezone.now()
    delta = now - period.prev().start
    slug = calendar.slug
    target = 'day_calendar'
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-left"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.prev().start),
        )
    )


@register.simple_tag
def next_url_day(target, calendar, period):
    now = timezone.now()
    slug = calendar.slug
    target = 'day_calendar'
    delta = period.next().start - now
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-right"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.next().start),
        )
    )


@register.inclusion_tag("schedule/_prevnext_day.html")
def prevnext_day(target, calendar, period, fmt=None):
    if fmt is None:
        fmt = settings.DATE_FORMAT
    context = {
        "calendar": calendar,
        "period": period,
        "period_name": format(period.start, fmt),
        "target": target,
    }
    return context


''' end previous and next url for day '''


''' previous and next url for week '''

@register.simple_tag
def prev_url_week(target, calendar, period):
    now = timezone.now()
    delta = now - period.prev().start
    slug = calendar.slug
    target = 'week_calendar'
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-left"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.prev().start),
        )
    )


@register.simple_tag
def next_url_week(target, calendar, period):
    now = timezone.now()
    slug = calendar.slug
    target = 'week_calendar'
    delta = period.next().start - now
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-right"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.next().start),
        )
    )


@register.inclusion_tag("schedule/_prevnext_week.html")
def prevnext_week(target, calendar, period, fmt=None):
    if fmt is None:
        fmt = settings.DATE_FORMAT
    context = {
        "calendar": calendar,
        "period": period,
        "period_name": format(period.start, fmt),
        "target": target,
    }
    return context


''' end previous and next url for week '''


''' previous and next url for tri '''

@register.simple_tag
def prev_url_tri(target, calendar, period):
    now = timezone.now()
    delta = now - period.prev().start
    slug = calendar.slug
    target = 'tri_month_calendar'
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-left"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.prev().start),
        )
    )


@register.simple_tag
def next_url_tri(target, calendar, period):
    now = timezone.now()
    slug = calendar.slug
    target = 'tri_month_calendar'
    delta = period.next().start - now
    if delta.total_seconds() > SCHEDULER_PREVNEXT_LIMIT_SECONDS:
        return ""

    return mark_safe(
        '<a href="%s%s"><i class="fa fa-arrow-circle-right"></i></a>'
        % (
            reverse(target, kwargs={"calendar_slug": slug}),
            querystring_for_date(period.next().start),
        )
    )


@register.inclusion_tag("schedule/_prevnext_tri.html")
def prevnext_tri(target, calendar, period, fmt=None):
    if fmt is None:
        fmt = settings.DATE_FORMAT
    context = {
        "calendar": calendar,
        "period": period,
        "period_name": format(period.start, fmt),
        "target": target,
    }
    return context


''' end previous and next url for tri '''





@register.inclusion_tag("schedule/_detail.html")
def detail(occurrence):
    context = {"occurrence": occurrence}
    return context


def _cook_occurrences(period, occs, width, height):
    """ Prepare occurrences to be displayed.
        Calculate dimensions and position (in px) for each occurrence.
        The algorithm tries to fit overlapping occurrences so that they require a minimum
        number of "columns".
        Arguments:
        period - time period for the whole series
        occs - occurrences to be displayed
        increment - slot size in minutes
        width - width of the occurrences column (px)
        height - height of the table (px)
    """
    last = {}
    # find out which occurrences overlap
    for o in occs[:]:
        o.data = period.classify_occurrence(o)
        if not o.data:
            occs.remove(o)
            continue
        o.level = -1
        o.max = 0
        if not last:
            last[0] = o
            o.level = 0
        else:
            for k in sorted(last.keys()):
                if last[k].end <= o.start:
                    o.level = k
                    last[k] = o
                    break
            if o.level == -1:
                k = k + 1
                last[k] = o
                o.level = k
    # calculate position and dimensions
    for o in occs:
        # number of overlapping occurrences
        o.max = len([n for n in occs if not(n.end <= o.start or n.start >= o.end)])
    for o in occs:
        o.cls = o.data['class']
        o.real_start = max(o.start, period.start)
        o.real_end = min(o.end, period.end)
        # number of "columns" is a minimum number of overlaps for each overlapping group
        o.max = min([n.max for n in occs if not(n.end <= o.start or n.start >= o.end)] or [1])
        w = int(width / (o.max))
        o.width = w - 2
        o.left = w * o.level
        o.top = int(height * (float((o.real_start - period.start).seconds) / (period.end - period.start).seconds))
        o.height = int(height * (float((o.real_end - o.real_start).seconds) / (period.end - period.start).seconds))
        o.height = min(o.height, height - o.top) # trim what extends beyond the area
    return occs



def _cook_slots(period, increment):
    """
    Prepare slots to be displayed on the left hand side
    calculate dimensions (in px) for each slot.
    Arguments:
    period - time period for the whole series
    increment - slot size in minutes
    """
    tdiff = datetime.timedelta(minutes=increment)
    num = int((period.end - period.start).total_seconds()) // int(tdiff.total_seconds())
    s = period.start
    slots = []
    for i in range(num):
        sl = period.get_time_slot(s, s + tdiff)
        slots.append(sl)
        s = s + tdiff
    return slots


@register.simple_tag
def hash_occurrence(occ):
    return "{}_{}".format(occ.start.strftime("%Y%m%d%H%M%S"), occ.event.id)
