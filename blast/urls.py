from django.urls import path
from django.views.generic import TemplateView


app_name='blast'

urlpatterns = [
    path('blast_activities', TemplateView.as_view(template_name="newsletter/message/general-newsletter/activities.html"), name='blast_activities'),
]