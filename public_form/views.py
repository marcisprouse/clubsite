"""
View which can render and send email from a contact form.
"""
import logging

from django import http
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.views.generic.edit import CreateView

from .forms import (
    ContactForm,
    StringKeyedDict,
    CustomContactForm,
    MembershipApplicationForm,
)
from .models import MembershipApplication
from .services import render_membership_application_pdf

logger = logging.getLogger(__name__)


class ContactFormView(FormView):
    form_class = ContactForm
    recipient_list = None
    success_url = reverse_lazy("public_form_sent")
    template_name = "public_form/public_form.html"

    def form_valid(self, form) -> http.HttpResponse:
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self) -> StringKeyedDict:
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})

        # We may also have been given a recipient list when
        # instantiated.
        if self.recipient_list is not None:
            kwargs.update({"recipient_list": self.recipient_list})
        return kwargs


class CustomContactFormView(FormView):
    form_class = CustomContactForm
    recipient_list = None
    template_name = 'public_form/public_form.html'


    def form_valid(self, form):
        form.save()
        return super(CustomContactFormView, self).form_valid(form)

    def get_form_kwargs(self):
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super(CustomContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        # This is in a method instead of the success_url attribute
        # because doing it as an attribute would involve a
        # module-level call to reverse(), creating a circular
        # dependency between the URLConf (which imports this module)
        # and this module (which would need to access the URLConf to
        # make the reverse() call).
        return reverse_lazy('public_form_sent')


def some_view(request):
    if request.POST:
        form = CustomContactForm(request.POST)

        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            human = True
    else:
        form = CustomContactForm()

    return render(request, 'public_form/public_form.html', {'form': form})


class MembershipApplicationCreateView(CreateView):
    model = MembershipApplication
    form_class = MembershipApplicationForm
    template_name = "public_form/membership_application.html"
    success_url = reverse_lazy("membership_application_sent")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self._send_board_notification()
        return response

    def _send_board_notification(self):
        application = self.object
        if application is None:
            return

        admin_url = self.request.build_absolute_uri(
            reverse("admin:public_form_membershipapplication_change", args=[application.pk])
        )
        pdf_bytes = render_membership_application_pdf(
            [application],
            base_url=self.request.build_absolute_uri("/"),
        )
        context = {
            "application": application,
            "admin_url": admin_url,
        }
        message = EmailMessage(
            subject=render_to_string(
                "public_form/membership_application_board_subject.txt",
                context,
            ).strip(),
            body=render_to_string(
                "public_form/membership_application_board.txt",
                context,
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["board@coyotelakesrecreationclub.org"],
            reply_to=[application.badge_1_email] if application.badge_1_email else None,
        )
        message.attach(
            f"membership_application_{application.pk}.pdf",
            pdf_bytes,
            "application/pdf",
        )
        try:
            message.send(fail_silently=False)
        except Exception:
            logger.exception(
                "Failed to send board notification for membership application %s",
                application.pk,
            )
