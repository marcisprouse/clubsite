"""
A base contact form for allowing users to send email messages through
a web interface.
"""
import html
from typing import Any, Dict, List, Optional
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms, http
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template import loader
from django.utils.translation import gettext_lazy as _
from collections import OrderedDict
from captcha.fields import CaptchaField
from .models import MembershipApplication

# Typing alias for clarity
StringKeyedDict = Dict[str, Any]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label=_("Your name"), help_text="    ")
    email = forms.EmailField(max_length=200, label=_("Your email address"), help_text="    ")
    body = forms.CharField(widget=forms.Textarea, label=_("Your message"))

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['slobe1022@gmail.com', 'marci@webfairydesign.com']
    subject_template_name = "public_form/public_form_subject.txt"
    template_name = "public_form/public_form.txt"

    def __init__(
        self,
        data: Optional[StringKeyedDict] = None,
        files: Optional[StringKeyedDict] = None,
        request: Optional[http.HttpRequest] = None,
        recipient_list: Optional[List[str]] = None,
        *args,
        **kwargs
    ):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        self.request = request
        if recipient_list is not None:
            self.recipient_list = recipient_list
        super().__init__(data=data, files=files, *args, **kwargs)

    def message(self) -> str:
        template_name = self.template_name() if callable(self.template_name) else self.template_name
        return loader.render_to_string(template_name, self.get_context(), request=self.request)

    def subject(self) -> str:
        template_name = self.subject_template_name() if callable(self.subject_template_name) else self.subject_template_name
        subject = loader.render_to_string(template_name, self.get_context(), request=self.request)
        return "".join(subject.splitlines())

    def get_context(self) -> Dict[str, Any]:
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")

        unescaped_body = html.unescape(self.cleaned_data.get("body", ""))
        context = dict(self.cleaned_data, site=get_current_site(self.request))
        context["body"] = mark_safe(unescaped_body)
        return context

    def save(self, fail_silently: bool = False) -> None:
        if not self.is_valid():
            raise ValueError("Cannot send message from invalid contact form")

        message = EmailMessage(
            subject=self.subject(),
            body=self.message(),
            from_email=self.from_email,
            to=self.recipient_list,
            headers={
                "Reply-To": f'{self.cleaned_data["name"]} <{self.cleaned_data["email"]}>'
            },
        )
        message.send(fail_silently=fail_silently)


class AkismetContactForm(ContactForm):
    SPAM_MESSAGE = _("Your message was classified as spam.")

    def clean_body(self) -> str:
        from akismet import Akismet

        akismet_api = Akismet(
            key=getattr(settings, "AKISMET_API_KEY", None),
            blog_url=getattr(settings, "AKISMET_BLOG_URL", None),
        )
        akismet_kwargs = {
            "user_ip": self.request.META.get("REMOTE_ADDR"),
            "user_agent": self.request.META.get("HTTP_USER_AGENT"),
            "comment_author": self.cleaned_data.get("name"),
            "comment_author_email": self.cleaned_data.get("email"),
            "comment_content": self.cleaned_data.get("body"),
            "comment_type": "contact-form",
        }

        if akismet_api.comment_check(**akismet_kwargs):
            raise forms.ValidationError(self.SPAM_MESSAGE)

        return self.cleaned_data["body"]


class CustomContactForm(AkismetContactForm):
    REASON = (
        ('', ''),
        ('Information Request', 'Information Request'),
    )
    reason = forms.ChoiceField(choices=REASON, label='Reason', help_text="    ")
    captcha = CaptchaField()
    hidden_field = forms.CharField(required=False, widget=forms.HiddenInput)

    template_name = 'public_form/public_form.txt'
    subject_template_name = "public_form/public_form_subject.txt"

    def __init__(self, request, *args, **kwargs):
        super().__init__(
            request=request,
            recipient_list=['slobe1022@gmail.com', 'marci@webfairydesign.com'],
            *args, **kwargs
        )
        fields_keyOrder = ['reason', 'name', 'email', 'body', 'captcha', 'hidden_field']
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('hidden_field'):
            raise forms.ValidationError("Spam detected.")
        return cleaned_data

    def clean_body(self):
        body = self.cleaned_data['body']
        spam_keywords = ['LeadConnect', 'boltleadgeneration.com', 'Try LeadConnect', 'Eric Jones']
        for keyword in spam_keywords:
            if keyword.lower() in body.lower():
                raise forms.ValidationError("Your message was flagged as spam.")
        return super().clean_body()


class MembershipApplicationForm(forms.ModelForm):
    SPAM_MESSAGE = _("Your application was classified as spam.")
    captcha = CaptchaField()
    hidden_field = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        fields_key_order = [
            "deed_owner_names",
            "address",
            "phone_1",
            "phone_2",
            "primary_address",
            "previous_owner_names",
            "membership_number",
            "key_number",
            "tenant_names_contact",
            "badge_1_name",
            "badge_1_phone",
            "badge_1_email",
            "badge_2_name",
            "badge_2_phone",
            "badge_2_email",
            "captcha",
            "hidden_field",
        ]
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("hidden_field"):
            raise forms.ValidationError("Spam detected.")
        self._check_akismet()
        return cleaned_data

    def _akismet_application_payload(self):
        return {
            "user_ip": self.request.META.get("REMOTE_ADDR") if self.request else None,
            "user_agent": self.request.META.get("HTTP_USER_AGENT") if self.request else None,
            "comment_author": self.cleaned_data.get("deed_owner_names"),
            "comment_author_email": self.cleaned_data.get("badge_1_email")
            or self.cleaned_data.get("badge_2_email"),
            "comment_content": "\n".join(
                [
                    self.cleaned_data.get("deed_owner_names", ""),
                    self.cleaned_data.get("address", ""),
                    self.cleaned_data.get("primary_address", ""),
                    self.cleaned_data.get("tenant_names_contact", ""),
                ]
            ),
            "comment_type": "membership-application",
        }

    def clean_tenant_names_contact(self):
        value = self.cleaned_data.get("tenant_names_contact", "") or ""
        spam_keywords = ["LeadConnect", "boltleadgeneration.com", "Try LeadConnect", "Eric Jones"]
        if any(keyword.lower() in value.lower() for keyword in spam_keywords):
            raise forms.ValidationError("Your application was flagged as spam.")
        return value

    def _check_akismet(self):
        # Fail open if Akismet has an outage; we still have captcha + honeypot.
        try:
            from akismet import Akismet

            akismet_api = Akismet(
                key=getattr(settings, "AKISMET_API_KEY", None),
                blog_url=getattr(settings, "AKISMET_BLOG_URL", None),
            )
            if akismet_api.comment_check(**self._akismet_application_payload()):
                raise forms.ValidationError(self.SPAM_MESSAGE)
        except forms.ValidationError:
            raise
        except Exception:
            return

    class Meta:
        model = MembershipApplication
        fields = [
            "deed_owner_names",
            "address",
            "phone_1",
            "phone_2",
            "primary_address",
            "previous_owner_names",
            "membership_number",
            "key_number",
            "tenant_names_contact",
            "badge_1_name",
            "badge_1_phone",
            "badge_1_email",
            "badge_2_name",
            "badge_2_phone",
            "badge_2_email",
        ]
        labels = {
            "deed_owner_names": "Deed Owner(s) Names",
            "phone_1": "Phone #1",
            "phone_2": "Phone #2",
            "primary_address": "Primary Address",
            "previous_owner_names": "Previous Owner's Names",
            "membership_number": "Membership #",
            "key_number": "Key #",
            "tenant_names_contact": "If rented: tenant names/contact info",
            "badge_1_name": "Badge 1 Name",
            "badge_1_phone": "Badge 1 Phone",
            "badge_1_email": "Badge 1 Email",
            "badge_2_name": "Badge 2 Name",
            "badge_2_phone": "Badge 2 Phone",
            "badge_2_email": "Badge 2 Email",
        }
