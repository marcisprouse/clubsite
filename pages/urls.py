from django.urls import path
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from . import views
from django.contrib.auth.decorators import login_required

app_name='pages'

urlpatterns = [
    path('', TemplateView.as_view(template_name="pages/index.html"), name='home'),
    path('wp/', TemplateView.as_view(template_name="pages/index.html"), name='redirect_home'),
    path('about/', TemplateView.as_view(template_name="pages/our_club.html"), name='our_club'),
    # path('test/', TemplateView.as_view(template_name="pages/test.html"), name='test'),
    path('about/history', TemplateView.as_view(template_name="pages/history.html"), name='history'),
    path('about/timeline', TemplateView.as_view(template_name="pages/timeline.html"), name='timeline'),
    path('about/board_members', TemplateView.as_view(template_name="pages/board_members.html"), name='board_members'),

    path('rental', TemplateView.as_view(template_name="pages/rent_club_public.html"), name='public_rental'),

    path('contest', TemplateView.as_view(template_name="pages/rules_login_win.html"), name='rules_login_win'),

    path('feature', login_required(views.FeatureListView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='feature'),
    path('feature/<int:pk>', login_required(views.FeatureDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='feature_details'),

    path('information/dues', login_required(TemplateView.as_view(template_name="pages/paying_dues.html"), login_url='/accounts/signin/?next=/accounts/'), name='paying_dues'),
    path('information/rent', login_required(TemplateView.as_view(template_name="pages/rent_club.html"), login_url='/accounts/signin/?next=/accounts/'), name='rent_club'),
    path('information/bylaws', login_required(TemplateView.as_view(template_name="pages/bylaws.html"), login_url='/accounts/signin/?next=/accounts/'), name='bylaws'),
    path('information/rules', login_required(TemplateView.as_view(template_name="pages/rules_regs.html"), login_url='/accounts/signin/?next=/accounts/'), name='rules_regs'),
    path('information/pool', login_required(TemplateView.as_view(template_name="pages/pool_info_rules.html"), login_url='/accounts/signin/?next=/accounts/'), name='pool_info_rules'),

    path('birthdays', login_required(TemplateView.as_view(template_name="pages/birthday.html"), login_url='/accounts/signin/?next=/accounts/'), name='birthdays'),

    path('instruction/add_user', views.add_user, name='add_user'),
    path('instruction/email_blast', views.email_blast, name='email_blast'),
    path('instruction/add_event', views.add_event, name='add_event'),
    path('instruction/add_feature', views.add_feature, name='add_feature'),
    path('instruction/add_alert', views.add_alert, name='add_alert'),
    path('instruction/add_certificate', views.add_certificate, name='add_certificate'),

    path('reports/report_list', views.report_list, name='report_list'),
    path('instructions/admin_manual', views.admin_manual, name='admin_manual'),

    path('activity', views.OccurrenceListView.as_view(), name='activity_list'),
    path('activity/<int:pk>', views.OccurrenceDetailView.as_view(), name='activity_detail'),
    path('activity/bulletin', login_required(TemplateView.as_view(template_name="pages/bulletin_list.html"), login_url='/accounts/signin/?next=/accounts/'), name='bulletin_list'),

    path('activity/vol', login_required(views.VolunteerListView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='volunteer_list'),
    path('activity/vol/<int:pk>', login_required(views.VolunteerDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='volunteer_detail'),
    path('activity/vol/<int:pk>/volunteer', login_required(views.VolunteerCreateView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='volunteer_create'),
    path('volunteer/<int:pk>/delete', login_required(views.VolunteerDeleteView.as_view(success_url=reverse_lazy('pages:volunteer_list')), login_url='/accounts/signin/?next=/accounts/'), name='volunteer_delete'),

    path('activity/respond', login_required(views.RSVPListView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='rsvp_list'),
    path('activity/respond/<int:pk>', login_required(views.RSVPDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='rsvp_detail'),
    path('activity/respond/<int:pk>/memberrsvp', login_required(views.MemberrsvpCreateView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='memberrsvp_create'),
    path('memberrsvp/<int:pk>/delete', login_required(views.MemberrsvpDeleteView.as_view(success_url=reverse_lazy('pages:rsvp_list')), login_url='/accounts/signin/?next=/accounts/'), name='rsvp_delete'),
]

handler404="home.views.handle_not_found"
# handler403="home.views.handle_not_found"
# handler500="home.views.handle_not_found"

