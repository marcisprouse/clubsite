# from django.shortcuts import render
from schedule.models import Event, Occurrence, Volunteer, Memberrsvp
from pages.models import Feature, Alert, ActivityBulletinBoard
# from schedule.periods import Period
# import datetime
from django.views.generic import ListView, DetailView
from .owner import OwnerDeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect, get_object_or_404

# this is for staff only page views
from django.contrib.auth.decorators import user_passes_test


class OccurrenceListView(ListView):
    template_name = "pages/activity_list.html"


    def get_queryset(self):
        all_events = Event.objects.all()
        return { 'all_events' : all_events }


''' class OccurrenceListView(ListView):
    template_name = "pages/index.html"


    def get_queryset(self):
        all_events = Event.objects.all()
        return { 'all_events' : all_events } '''




class VolunteerListView(ListView):
    template_name = "pages/volunteer_list.html"


    def get_queryset(self):
        all_events = Event.objects.all()
        return { 'all_events' : all_events }




class RSVPListView(ListView):
    template_name = "pages/rsvp_list.html"


    def get_queryset(self):
        all_events = Event.objects.all()
        return { 'all_events' : all_events }




class OccurrenceDetailView(DetailView):
    model = Occurrence
    template_name = "pages/activity_detail.html"




class VolunteerDetailView(DetailView):
    model = Occurrence
    template_name = "pages/volunteer_detail.html"




class RSVPDetailView(DetailView):
    model = Occurrence
    template_name = "pages/rsvp_detail.html"



from django.shortcuts import render
from .forms import VolunteerForm

class VolunteerCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Occurrence, id=pk)
        volunteer = Volunteer(text=request.POST['volunteer'], owner=request.user, occurrence=a)
        volunteer.save()
        return redirect(reverse('pages:volunteer_detail', args=[pk]))

        def home(request):
            if request.method == 'POST':
                form = VolunteerForm(request.POST)
                if form.is_valid():
                    pass  # does nothing, just trigger the validation
            else:
                form = VolunteerForm()
            return render(request, 'pages/volunteer_detail.html', {'form': form})



class VolunteerDeleteView(OwnerDeleteView):
    model = Volunteer
    template_name = "pages/volunteer_delete.html"
    def get_success_url(self):
        occurrence = self.object.occurrence
        return reverse('pages:volunteer_detail', args=[occurrence.id])




from .forms import MemberrsvpForm

class MemberrsvpCreateView(LoginRequiredMixin, View):

    def post(self, request, pk) :
        a = get_object_or_404(Occurrence, id=pk)
        memberrsvp = Memberrsvp(
            attending=request.POST['attending'],
            mealchoice = request.POST.get('mealchoice', '------'),
            # mealchoice = request.POST['mealchoice'],
            guests=request.POST['guests'],
            bringing=request.POST['memberrsvp'],
            owner=request.user,
            occurrence=a)
        memberrsvp.save()
        return redirect(reverse('pages:rsvp_detail', args=[pk]))

        def home(request):
            if request.method == 'POST':
                form = MemberrsvpForm(request.POST)
                if form.is_valid():
                    pass  # does nothing, just trigger the validation
            else:
                form = MemberrsvpForm()
            return render(request, 'pages/rsvp_detail.html', {'form': form})



class MemberrsvpDeleteView(OwnerDeleteView):
    model = Memberrsvp
    template_name = "pages/rsvp_delete.html"
    def get_success_url(self):
        occurrence = self.object.occurrence
        return reverse('pages:rsvp_detail', args=[occurrence.id])



# this is for staff only page views

@user_passes_test(lambda user: user.is_staff)
def add_user(request):
    return render(request, 'pages/add_user.html')

@user_passes_test(lambda user: user.is_staff)
def email_blast(request):
    return render(request, 'pages/email_blast.html')

@user_passes_test(lambda user: user.is_staff)
def add_event(request):
    return render(request, 'pages/add_event.html')

@user_passes_test(lambda user: user.is_staff)
def add_feature(request):
    return render(request, 'pages/add_feature.html')

@user_passes_test(lambda user: user.is_staff)
def add_alert(request):
    return render(request, 'pages/add_alert.html')

@user_passes_test(lambda user: user.is_staff)
def add_certificate(request):
    return render(request, 'pages/add_certificate.html')

@user_passes_test(lambda user: user.is_staff)
def report_list(request):
    return render(request, 'pages/report_list.html')

@user_passes_test(lambda user: user.is_staff)
def admin_manual(request):
    return render(request, 'pages/admin_manual.html')




''' These views are for feature event '''

class FeatureListView(ListView):
    queryset = Feature.published.all()
    context_object_name = 'features'
    template_name = 'pages/feature.html'

class FeatureDetailView(DetailView):
    model = Feature


''' These views are for alerts '''

class AlertListView(ListView):
    queryset = Alert.published.all()
    context_object_name = 'alerts'
    template_name = 'pages/alert.html'

class AlertDetailView(DetailView):
    model = Alert


''' These views are for activity bulletin board '''

class ActivityBulletinBoardListView(ListView):
    queryset = ActivityBulletinBoard.published.all()
    context_object_name = 'bulletins'
    template_name = 'pages/bulletin_list.html'

class ActivityBulletinBoardDetailView(DetailView):
    model = ActivityBulletinBoard

