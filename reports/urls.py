from django.urls import path
from . import views


urlpatterns = [
    path('certificate_report', views.export_certificates_xls, name='certificate_report'),
    path('certificate_full_report', views.export_certificate_full_xls, name='certificate_full_report'),
    path('member_report', views.export_users_xls, name='member_report'),
    path('key_report', views.export_keys_xls, name='key_report'),
    path('event_volunteer_report', views.export_events_volunteers_xls, name='event_volunteer_report'),
    path('event_rsvp_report', views.export_events_rsvp_xls, name='event_rsvp_report'),
    path('contacts', views.export_contacts_xls, name='contacts'),
    path('badges_report', views.export_badges_xls, name='badges_report'),
    path('logins_report', views.export_logins_xls, name='logins_report'),
    path('blast_subscriptions', views.export_blast_subscriptions_xls, name='blast_subscriptions'),
]