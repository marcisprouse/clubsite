from schedule.models import Event
from certificates.models import Certificate
from schedule.periods import Period
from accounts.models import MyProfile
# from django.shortcuts import render
import datetime
# from django import forms
# from django.template.loader import get_template
# from django.template.loader import render_to_string






def events_renderer(request):
    all_events = Event.objects.all()
    all_events_list=[]

    for event in all_events:
        all_events_list.append(event)

    retval = {'all_events':all_events,
              'all_events_list':all_events_list
              }
    return retval;



def members_renderer(request):
    all_members = MyProfile.objects.all().order_by('user__last_name')
    all_members_list=[]

    for member in all_members:
        all_members_list.append(member)

    retval = {'all_members':all_members,
              'all_members_list':all_members_list,
              }

    return retval;

''' This is mostly used for the sale table. That's why it is ordered by for sale as of date. '''
def certificates_renderer(request):
    all_certificates = Certificate.objects.all().order_by('is_for_sale_as_of_date')
    all_certificates_list=[]
    all_certificates_for_sale=[]
    all_certificates_for_sale_not_club=[]

    for certificate in all_certificates:
        all_certificates_list.append(certificate)

    for cert in all_certificates_list:
        if cert.is_for_sale == True:
            all_certificates_for_sale.append(cert)

    for c in all_certificates_for_sale:
        if c.is_club_held == False:
            all_certificates_for_sale_not_club.append(c)

    retval = {'all_certificates':all_certificates,
              'all_certificates_list':all_certificates_list,
              'all_certificates_for_sale':all_certificates_for_sale,
              'all_certificates_for_sale_not_club':all_certificates_for_sale_not_club
              }
    return retval;



def occurrences_this_week_index(request):
    my_events = Event.objects.all()
    today = datetime.datetime.now()
    this_week = Period(my_events, today, today+datetime.timedelta(days=7))
    occ_for_event_in_week_list = this_week.get_occurrences()


    context = {
              'occ_for_event_in_week_list':occ_for_event_in_week_list
              }
    return context



def occurrences_this_week(request):
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

    return retval;



def occurrences_next_thirty(request):
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

    return retval;



def occurrences_next_sixty(request):
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
    return retval;




def occurrences_next_ninety(request):
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
    return retval;



def occurrences_next_twohundred(request):
    ''' This function retrieves all events and occurrences for the next ninety days. '''
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
    return retval;



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
    all_volunteers = Volunteer.objects.all()
    all_volunteers_list=[]

    for volunteer in all_volunteers:
        all_volunteers_list.append(volunteer)

    retval = {'all_volunteers':all_volunteers,
              'all_volunteers_list':all_volunteers_list
              }
    return retval;


def memberrsvp_renderer(request):
    all_memberrsvps = Memberrsvp.objects.all()
    all_memberrsvps_list=[]

    for memberrsvp in all_memberrsvps:
        all_memberrsvps_list.append(memberrsvp)

    retval = {'all_memberrsvps':all_memberrsvps,
              'all_memberrsvps_list':all_memberrsvps_list
              }
    return retval;

def ctx_memberrsvp_form(request):
    return {'memberrsvp_form': MemberrsvpForm()}




