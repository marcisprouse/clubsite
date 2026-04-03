"""
Example URLConf for a contact form.
If all you want is the basic ContactForm with default behavior,
include this URLConf somewhere in your URL hierarchy (for example, at
``/contact/``)
"""

from django.urls import path
from django.views.generic import TemplateView

# from public_form.views import ContactFormView
from public_form.views import CustomContactFormView, MembershipApplicationCreateView

urlpatterns = [
    # path("", ContactFormView.as_view(), name="public_form"),
    path('', CustomContactFormView.as_view(), name='public_form'),
    path(
        "membership-application/",
        MembershipApplicationCreateView.as_view(),
        name="membership_application",
    ),
    path(
        "membership-application/sent/",
        TemplateView.as_view(template_name="public_form/membership_application_sent.html"),
        name="membership_application_sent",
    ),
    path(
        "sent/",
        TemplateView.as_view(template_name="public_form/public_form_sent.html"),
        name="public_form_sent",
    ),
]
