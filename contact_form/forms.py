from typing import Any, Dict, List, Optional
from collections import OrderedDict
import html

from django import forms, http
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template import loader
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from django.utils.safestring import mark_safe

StringKeyedDict = Dict[str, Any]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label=_("Your name"), help_text=" ")
    email = forms.EmailField(max_length=200, label=_("Your email address"), help_text=" ")
    body = forms.CharField(widget=forms.Textarea, label=_("Your message"))

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['slobe1022@gmail.com', 'marci@webfairydesign.com']
    subject_template_name = "contact_form/contact_form_subject.txt"
    template_name = "contact_form/contact_form.txt"

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
        return loader.render_to_string(self.template_name, self.get_context(), request=self.request)

    def subject(self) -> str:
        subject = loader.render_to_string(self.subject_template_name, self.get_context(), request=self.request)
        return "".join(subject.splitlines())

    def get_context(self) -> StringKeyedDict:
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")

        context = dict(self.cleaned_data, site=get_current_site(self.request))

        # Unescape and mark safe
        unescaped_body = html.unescape(context.get("body", ""))
        context["body"] = mark_safe(unescaped_body)

        return context

    def get_message_dict(self) -> StringKeyedDict:
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")

        return {
            "subject": self.subject(),
            "body": self.message(),
            "from_email": self.from_email,
            "to": self.recipient_list,
            "headers": {
                "Reply-To": f'{self.cleaned_data["name"]} <{self.cleaned_data["email"]}>'
            },
        }

    def save(self, fail_silently: bool = False) -> None:
        EmailMessage(**self.get_message_dict()).send(fail_silently=fail_silently)


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
            "comment_content": self.cleaned_data["body"],
            "comment_type": "contact-form",
        }
        if akismet_api.comment_check(**akismet_kwargs):
            raise forms.ValidationError(self.SPAM_MESSAGE)
        return self.cleaned_data["body"]


class CustomContactForm(AkismetContactForm):
    REASON = (
        ('', ''),
        ('Maintenance Issue', 'Maintenance Issue'),
        ('Account Inquiry', 'Account Inquiry'),
        ('Membership Information', 'Membership Information'),
        ('Activity/Event Inquiry', 'Activity/Event Inquiry'),
        ('Rental Reservation', 'Rental Reservation'),
        ('Badge Request', 'Badge Request'),
        ('Key Issue', 'Key Issue'),
        ('Web Site', 'Web Site'),
        ('Board of Directors', 'Board of Directors'),
        ('Other', 'Other'),
    )

    captcha = CaptchaField()
    template_name = 'contact_form/contact_form.txt'
    subject_template_name = "contact_form/contact_form_subject.txt"

    def __init__(self, request, *args, **kwargs):
        super().__init__(
            request=request,
            recipient_list=['slobe1022@gmail.com', 'marci@webfairydesign.com'],
            *args,
            **kwargs
        )
        self.fields['reason'] = forms.ChoiceField(choices=self.REASON, label='Reason', help_text=" ")
        fields_keyOrder = ['reason', 'name', 'email', 'body', 'captcha']
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)
