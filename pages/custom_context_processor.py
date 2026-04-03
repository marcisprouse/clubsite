from schedule.models import Event
from pages.models import Feature, Alert, ActivityBulletinBoard
from certificates.models import Certificate
from for_sale.models import Sale
from schedule.periods import Period
from accounts.models import MyProfile
import datetime
from django.utils import timezone
from django import forms
from django.conf import settings
from django.core.cache import cache


def _cached_context(key, timeout, builder):
    data = cache.get(key)
    if data is None:
        data = builder()
        cache.set(key, data, timeout)
    return data



def my_map(request):
    context = {
        'api_key': settings.GOOGLE_API_KEY
    }
    return context


def events_renderer(request):
    return _cached_context(
        "ctx:pages:events_renderer",
        60,
        lambda: (lambda events: {"all_events": events, "all_events_list": events})(list(Event.objects.all())),
    )



def members_renderer(request):
    def _build():
        all_members = list(MyProfile.objects.select_related("user").order_by("user__last_name"))
        all_active_members_list = [m for m in all_members if m.is_active_member]
        all_members_logged_in = [m for m in all_members if m.user and m.user.last_login]
        all_renter_members = [m for m in all_members if m.is_a_renter_member]
        return {
            "all_members": all_members,
            "all_members_list": all_members,
            "all_active_members_list": all_active_members_list,
            "all_members_logged_in": all_members_logged_in,
            "all_renter_members": all_renter_members,
        }

    return _cached_context("ctx:pages:members_renderer", 120, _build)



''' This is for the birthday list '''
def birthdays_renderer(request):
    return _cached_context(
        "ctx:pages:birthdays_renderer",
        300,
        lambda: (lambda birthdays: {"all_birthdays": birthdays, "all_birthdays_list": birthdays})(
            list(MyProfile.objects.filter(birth_month__isnull=False).order_by("birth_day"))
        ),
    )


'''This is for the new for sale table in the for_sale app '''
def for_sale_renderer(request):
    def _build():
        all_list = list(Sale.objects.all().order_by("date_resigned"))
        all_sold_list = [s for s in all_list if s.purchase_date]
        all_for_sale_list = [s for s in all_list if s.sold_to in ("", None)]
        return {
            "all_for_sale_list": all_for_sale_list,
            "all_list": all_list,
            "all_sold_list": all_sold_list,
        }

    return _cached_context("ctx:pages:for_sale_renderer", 120, _build)




''' This is mostly used for the sale table. That's why it is ordered by for sale as of date. '''
def certificates_renderer(request):
    def _build():
        all_certificates_list = list(Certificate.objects.all().order_by("is_for_sale_as_of_date"))
        all_certificates_for_sale = [c for c in all_certificates_list if c.is_for_sale]
        all_certificates_for_sale_not_club = [c for c in all_certificates_for_sale if not c.is_club_held]
        return {
            "all_certificates": all_certificates_list,
            "all_certificates_list": all_certificates_list,
            "all_certificates_for_sale": all_certificates_for_sale,
            "all_certificates_for_sale_not_club": all_certificates_for_sale_not_club,
        }

    return _cached_context("ctx:pages:certificates_renderer", 120, _build)


''' This is mostly used for the Member Homes area. '''
def certificates_not_sale_renderer(request):
    def _build():
        certificates_list = list(Certificate.objects.all().order_by("certificate_number"))
        certificates_not_for_sale = [c for c in certificates_list if not c.is_for_sale]
        certificates_not_for_sale_not_club = [c for c in certificates_not_for_sale if not c.is_club_held]
        return {
            "certificates": certificates_list,
            "certificates_list": certificates_list,
            "certificates_not_for_sale": certificates_not_for_sale,
            "certificates_not_for_sale_not_club": certificates_not_for_sale_not_club,
            "members_in_household": [],
        }

    return _cached_context("ctx:pages:certificates_not_sale_renderer", 120, _build)



def occurrences_this_week_index(request):
    def _build():
        my_events = Event.objects.all()
        today = datetime.datetime.now()
        this_week = Period(my_events, today, today + datetime.timedelta(days=7))
        return {"occ_for_event_in_week_list": this_week.get_occurrences()}

    return _cached_context("ctx:pages:occurrences_this_week_index", 60, _build)

def occurrences_this_week(request):
    cached = cache.get("ctx:pages:occurrences_this_week")
    if cached is not None:
        return cached
    ''' This function retrieves all events and occurrences for the current week '''
    my_events = Event.objects.all()
    today = datetime.datetime.now()
    this_week = Period(my_events, today, today+datetime.timedelta(days=7))
    activity_week_list = this_week.get_occurrences()



    ''' There are 'occurrences' without ids, they are events only and usually repeat.
    Only occurrences that are entered in the occurrence table have ids, so
    I am isolating those occurrences WITH ids from within the events so that I can have a
    detail view for those occurrences.'''

    act_with_id_list=[]

    for act_with_id in activity_week_list:
        if act_with_id.id != None:
            act_with_id_list.append(act_with_id)

    ''' This will filter the activities that need volunteers.'''
    vol_act_week_list = []

    for vol in act_with_id_list:
        if vol.need_volunteers == True:
            vol_act_week_list.append(vol)

    ''' This will filter the activities that need members to bring something.'''
    item_act_week_list = []

    for item in act_with_id_list:
        if item.bring == True:
            item_act_week_list.append(item)

    ''' This will filter the activities that need rsvp.'''
    yes_act_week_list = []

    for yes in act_with_id_list:
        if yes.rsvp == True:
            yes_act_week_list.append(yes)


    retval = {
              'activity_week_list':activity_week_list,
              'act_with_id_list':act_with_id_list,
              'vol_act_week_list':vol_act_week_list,
              'item_act_week_list':item_act_week_list,
              'yes_act_week_list':yes_act_week_list
              }

    cache.set("ctx:pages:occurrences_this_week", retval, 60)
    return retval



def occurrences_next_thirty(request):
    cached = cache.get("ctx:pages:occurrences_next_thirty")
    if cached is not None:
        return cached
    ''' This function retrieves all events and occurrences for the next thirty days. '''
    my_events = Event.objects.all()
    today = datetime.datetime.now()
    next_thirty = Period(my_events,today, today+datetime.timedelta(days=31))
    activity_thirty_list = next_thirty.get_occurrences()


    ''' There are 'occurrences' without ids, they are events only and usually repeat.
    Only occurrences that are entered in the occurrence table have ids, so
    I am isolating those occurrences WITH ids from within the events so that I can have a
    detail view for those occurrences.'''

    act_with_id_thirty_list=[]

    for act_with_id_thirty in activity_thirty_list:
        if act_with_id_thirty.id != None:
            act_with_id_thirty_list.append(act_with_id_thirty)

    ''' This will filter the activities that need volunteers.'''

    vol_act_thirty_list = []

    for vol in act_with_id_thirty_list:
        if vol.need_volunteers == True:
            vol_act_thirty_list.append(vol)


    ''' This will filter the activities that need members to bring something.'''
    item_act_thirty_list = []

    for item in act_with_id_thirty_list:
        if item.bring == True:
            item_act_thirty_list.append(item)

    ''' This will filter the activities that need rsvp.'''
    yes_act_thirty_list = []

    for yes in act_with_id_thirty_list:
        if yes.rsvp == True:
            yes_act_thirty_list.append(yes)


    retval = {
              'activity_thirty_list':activity_thirty_list,
              'act_with_id_thirty_list':act_with_id_thirty_list,
              'vol_act_thirty_list':vol_act_thirty_list,
              'item_act_thirty_list':item_act_thirty_list,
              'yes_act_thirty_list':yes_act_thirty_list
              }

    cache.set("ctx:pages:occurrences_next_thirty", retval, 60)
    return retval



def occurrences_next_sixty(request):
    cached = cache.get("ctx:pages:occurrences_next_sixty")
    if cached is not None:
        return cached
    ''' This function retrieves all events and occurrences for the next sixty days. '''
    my_events = Event.objects.all()
    today = datetime.datetime.now()
    next_sixty = Period(my_events,today, today+datetime.timedelta(days=62))
    activity_sixty_list = next_sixty.get_occurrences()


    ''' There are 'occurrences' without ids, they are events only and usually repeat.
    Only occurrences that are entered in the occurrence table have ids, so
    I am isolating those occurrences WITH ids from within the events so that I can have a
    detail view for those occurrences.'''

    act_with_id_sixty_list=[]

    for act_with_id_sixty in activity_sixty_list:
        if act_with_id_sixty.id != None:
            act_with_id_sixty_list.append(act_with_id_sixty)

    ''' This will filter the activities that need volunteers.'''

    vol_act_sixty_list = []

    for vol in act_with_id_sixty_list:
        if vol.need_volunteers == True:
            vol_act_sixty_list.append(vol)

    ''' This will filter the activities that need members to bring something.'''
    item_act_sixty_list = []

    for item in act_with_id_sixty_list:
        if item.bring == True:
            item_act_sixty_list.append(item)

    ''' This will filter the activities that need rsvp.'''
    yes_act_sixty_list = []

    for yes in act_with_id_sixty_list:
        if yes.rsvp == True:
            yes_act_sixty_list.append(yes)


    retval = {
              'activity_sixty_list':activity_sixty_list,
              'act_with_id_sixty_list':act_with_id_sixty_list,
              'vol_act_sixty_list':vol_act_sixty_list,
              'item_act_sixty_list':item_act_sixty_list,
              'yes_act_sixty_list':yes_act_sixty_list
              }
    cache.set("ctx:pages:occurrences_next_sixty", retval, 60)
    return retval




def occurrences_next_ninety(request):
    cached = cache.get("ctx:pages:occurrences_next_ninety")
    if cached is not None:
        return cached
    ''' This function retrieves all events and occurrences for the next ninety days. '''
    my_events = Event.objects.all()
    today = datetime.datetime.now()
    next_ninety = Period(my_events,today, today+datetime.timedelta(days=93))
    activity_ninety_list = next_ninety.get_occurrences()


    ''' There are 'occurrences' without ids, they are events only and usually repeat.
    Only occurrences that are entered in the occurrence table have ids, so
    I am isolating those occurrences WITH ids from within the events so that I can have a
    detail view for those occurrences.'''

    act_with_id_ninety_list=[]

    for act_with_id_ninety in activity_ninety_list:
        if act_with_id_ninety.id != None:
            act_with_id_ninety_list.append(act_with_id_ninety)

    ''' This will filter the activities that need volunteers.'''

    vol_act_ninety_list = []

    for vol in act_with_id_ninety_list:
        if vol.need_volunteers == True:
            vol_act_ninety_list.append(vol)

    ''' This will filter the activities that need members to bring something.'''
    item_act_ninety_list = []

    for item in act_with_id_ninety_list:
        if item.bring == True:
            item_act_ninety_list.append(item)

    ''' This will filter the activities that need rsvp.'''
    yes_act_ninety_list = []

    for yes in act_with_id_ninety_list:
        if yes.rsvp == True:
            yes_act_ninety_list.append(yes)


    retval = {
              'activity_ninety_list':activity_ninety_list,
              'act_with_id_ninety_list':act_with_id_ninety_list,
              'vol_act_ninety_list':vol_act_ninety_list,
              'item_act_ninety_list':item_act_ninety_list,
              'yes_act_ninety_list':yes_act_ninety_list
              }
    cache.set("ctx:pages:occurrences_next_ninety", retval, 60)
    return retval



def occurrences_next_twohundred(request):
    cached = cache.get("ctx:pages:occurrences_next_twohundred")
    if cached is not None:
        return cached
    ''' This function retrieves all events and occurrences for the next two hundred days. '''
    my_events = Event.objects.all()
    today = datetime.datetime.now()
    next_twohundred = Period(my_events,today, today+datetime.timedelta(days=200))
    activity_twohundred_list = next_twohundred.get_occurrences()


    ''' There are 'occurrences' without ids, they are events only and usually repeat.
    Only occurrences that are entered in the occurrence table have ids, so
    I am isolating those occurrences WITH ids from within the events so that I can have a
    detail view for those occurrences.'''

    act_with_id_twohundred_list=[]

    for act_with_id_twohundred in activity_twohundred_list:
        if act_with_id_twohundred.id != None:
            act_with_id_twohundred_list.append(act_with_id_twohundred)

    ''' This will filter the activities that need volunteers.'''

    vol_act_twohundred_list = []

    for vol in act_with_id_twohundred_list:
        if vol.need_volunteers == True:
            vol_act_twohundred_list.append(vol)

    ''' This will filter the activities that need members to bring something.'''
    item_act_twohundred_list = []

    for item in act_with_id_twohundred_list:
        if item.bring == True:
            item_act_twohundred_list.append(item)

    ''' This will filter the activities that need rsvp.'''
    yes_act_twohundred_list = []

    for yes in act_with_id_twohundred_list:
        if yes.rsvp == True:
            yes_act_twohundred_list.append(yes)


    retval = {
              'activity_twohundred_list':activity_twohundred_list,
              'act_with_id_twohundred_list':act_with_id_twohundred_list,
              'vol_act_twohundred_list':vol_act_twohundred_list,
              'item_act_twohundred_list':item_act_twohundred_list,
              'yes_act_twohundred_list':yes_act_twohundred_list
              }
    cache.set("ctx:pages:occurrences_next_twohundred", retval, 60)
    return retval


def occurrences_year(request):
    cached = cache.get("ctx:pages:occurrences_year")
    if cached is not None:
        return cached
    ''' This function retrieves all events and occurrences for the next year. '''
    my_events = Event.objects.all()
    today = datetime.datetime.now()
    next_year = Period(my_events,today, today+datetime.timedelta(days=365))
    activity_year_list = next_year.get_occurrences()


    ''' There are 'occurrences' without ids, they are events only and usually repeat.
    Only occurrences that are entered in the occurrence table have ids, so
    I am isolating those occurrences WITH ids from within the events so that I can have a
    detail view for those occurrences.'''

    act_with_id_year_list=[]

    for act_with_id_year in activity_year_list:
        if act_with_id_year.id != None:
            act_with_id_year_list.append(act_with_id_year)

    ''' This will filter the activities that need volunteers.'''

    vol_act_year_list = []

    for vol in act_with_id_year_list:
        if vol.need_volunteers == True:
            vol_act_year_list.append(vol)

    ''' This will filter the activities that need members to bring something.'''
    item_act_year_list = []

    for item in act_with_id_year_list:
        if item.bring == True:
            item_act_year_list.append(item)

    ''' This will filter the activities that need rsvp.'''
    yes_act_year_list = []

    for yes in act_with_id_year_list:
        if yes.rsvp == True:
            yes_act_year_list.append(yes)


    retval = {
              'activity_year_list':activity_year_list,
              'act_with_id_year_list':act_with_id_year_list,
              'vol_act_year_list':vol_act_year_list,
              'item_act_year_list':item_act_year_list,
              'yes_act_year_list':yes_act_year_list
              }
    cache.set("ctx:pages:occurrences_year", retval, 60)
    return retval




''' The following functions are for rendering forms from schedule app into the pages app '''

from pages.forms import VolunteerForm, MemberrsvpForm

def ctx_volunteer_form(request):
    return {'volunteer_form': VolunteerForm()}


from schedule.models import Occurrence, Volunteer, Memberrsvp

def ctx_occurrence_model(request):
    return {'occurrence_model': Occurrence()}


def ctx_volunteer_model(request):
    return {'volunteer_model': Volunteer()}


def ctx_memberrsvp_model(request):
    return {'memberrsvp_model': Memberrsvp()}




def volunteer_renderer(request):
    return _cached_context(
        "ctx:pages:volunteer_renderer",
        60,
        lambda: (lambda rows: {"all_volunteers": rows, "all_volunteers_list": rows})(list(Volunteer.objects.all())),
    )


def memberrsvp_renderer(request):
    return _cached_context(
        "ctx:pages:memberrsvp_renderer",
        60,
        lambda: (lambda rows: {"all_memberrsvps": rows, "all_memberrsvps_list": rows})(list(Memberrsvp.objects.all())),
    )

def ctx_memberrsvp_form(request):
    return {'memberrsvp_form': MemberrsvpForm()}


def feature_renderer(request):
    def _build():
        now = timezone.now()
        all_features = list(Feature.published.all())
        all_features_list = [f for f in all_features if f.publish < now < f.expire]
        return {"all_features": all_features, "all_features_list": all_features_list}

    return _cached_context("ctx:pages:feature_renderer", 60, _build)


def alert_renderer(request):
    def _build():
        now = timezone.now()
        all_alerts = list(Alert.published.all())
        all_alerts_list = [a for a in all_alerts if a.publish < now < a.expire]
        return {"all_alerts": all_alerts, "all_alerts_list": all_alerts_list}

    return _cached_context("ctx:pages:alert_renderer", 60, _build)


def activity_bulletin_board_renderer(request):
    def _build():
        now = timezone.now()
        all_bulletins = list(ActivityBulletinBoard.published.all())
        all_bulletins_list = [b for b in all_bulletins if b.publish < now < b.expire]
        return {"all_bulletins": all_bulletins, "all_bulletins_list": all_bulletins_list}

    return _cached_context("ctx:pages:activity_bulletin_board_renderer", 60, _build)


