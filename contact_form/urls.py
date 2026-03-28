"""
Example URLConf for a contact form.
If all you want is the basic ContactForm with default behavior,
include this URLConf somewhere in your URL hierarchy (for example, at
``/contact/``)
"""

from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# from contact_form.views import ContactFormView
from contact_form.views import CustomContactFormView



urlpatterns = [
    # path("", ContactFormView.as_view(), name="contact_form"),
    path('', login_required(CustomContactFormView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='contact_form'),
    path(
        "sent/",
        login_required(TemplateView.as_view(template_name="contact_form/contact_form_sent.html"), login_url='/accounts/signin/?next=/accounts/'),
        name="contact_form_sent",
    ),
]
