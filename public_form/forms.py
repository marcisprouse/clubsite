"""
A base contact form for allowing users to send email messages through
a web interface.
"""

from typing import Any, Dict, List, Optional

from django import forms, http
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import gettext_lazy as _
from collections import OrderedDict
from captcha.fields import CaptchaField

# Parameters to a form being handled from a live request will actually
# be instances of django.utils.datastructures.MultiValueDict, but this
# is declared as a typing.Dict for a few reasons:
#
# * MultiValueDict is a subclass of dict, so instances of
#   MultiValueDict will pass type checks.
#
# * Testing of forms more typically passes in plain dict for the form
#   arguments, so supporting it is useful.
#
# * PEP 560, which allows dropping the typing module's aliases and
#   subscripting the actual types, was adopted for Python 3.7, but
#   currently we support back to Python 3.5.
StringKeyedDict = Dict[str, Any]


class ContactForm(forms.Form):
    """
    The base contact form class from which all contact form classes
    should inherit.
    """

    name = forms.CharField(max_length=100, label=_("Your name"), help_text="    ")
    email = forms.EmailField(max_length=200, label=_("Your email address"), help_text="    ")
    body = forms.CharField(widget=forms.Textarea, label=_("Your message"))

    from_email = settings.DEFAULT_FROM_EMAIL

    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

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
        """
        Render the body of the message to a string.
        """
        template_name = (
            self.template_name() if callable(self.template_name) else self.template_name
        )
        return loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )

    def subject(self) -> str:
        """
        Render the subject of the message to a string.
        """
        template_name = (
            self.subject_template_name()
            if callable(self.subject_template_name)
            else self.subject_template_name
        )
        subject = loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )
        return "".join(subject.splitlines())

    def get_context(self) -> StringKeyedDict:
        """
        Return the context used to render the templates for the email
        subject and body.
        By default, this context includes:
        * All of the validated values in the form, as variables of the
          same names as their fields.
        * The current ``Site`` object, as the variable ``site``.
        * Any additional variables added by context processors (this
          will be a ``RequestContext``).
        """
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        return dict(self.cleaned_data, site=get_current_site(self.request))

    def get_message_dict(self) -> StringKeyedDict:
        """
        Generate the various parts of the message and return them in a
        dictionary, suitable for passing directly as keyword arguments
        to ``django.core.mail.send_mail()``.
        By default, the following values are returned:
        * ``from_email``
        * ``message``
        * ``recipient_list``
        * ``subject``
        """
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")
        message_dict = {}
        for message_part in ("from_email", "message", "recipient_list", "subject"):
            attr = getattr(self, message_part)
            message_dict[message_part] = attr() if callable(attr) else attr
        return message_dict

    def save(self, fail_silently: bool = False) -> None:
        """
        Build and send the email message.
        """
        send_mail(fail_silently=fail_silently, **self.get_message_dict())


class AkismetContactForm(ContactForm):
    """
    Contact form which doesn't add any extra fields, but does add an
    Akismet spam check to the validation routine.
    Requires the Python Akismet library, and two configuration
    parameters: an Akismet API key and the URL the key is associated
    with. These can be supplied either as the settings AKISMET_API_KEY
    and AKISMET_BLOG_URL, or the environment variables
    PYTHON_AKISMET_API_KEY and PYTHON_AKISMET_BLOG_URL.
    """

    SPAM_MESSAGE = _("Your message was classified as spam.")

    def clean_body(self) -> str:
        from akismet import Akismet

        akismet_api = Akismet(
            key=getattr(settings, "AKISMET_API_KEY", None),
            blog_url=getattr(settings, "AKISMET_BLOG_URL", None),
        )
        akismet_kwargs = {
            "user_ip": self.request.META["REMOTE_ADDR"],
            "user_agent": self.request.META.get("HTTP_USER_AGENT"),
            "comment_author": self.cleaned_data.get("name"),
            "comment_author_email": self.cleaned_data.get("email"),
            "comment_content": self.cleaned_data["body"],
            "comment_type": "contact-form",
        }
        if akismet_api.comment_check(**akismet_kwargs):
            raise forms.ValidationError(self.SPAM_MESSAGE)
        return self.cleaned_data["body"]




class CustomContactForm(ContactForm):
    def __init__(self, request, *args, **kwargs):
        super(CustomContactForm, self).__init__(request=request, recipient_list = ['info@coyotelakesrecreationclub.org'], *args, **kwargs)
        fields_keyOrder = ['reason', 'name', 'email', 'body', 'captcha']
        # if (self.fields.has_key('keyOrder')):
        if 'keyOrder' in self.fields:

            self.fields.keyOrder = fields_keyOrder
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)

    REASON = (
        ('',''),
        ('Information Request', 'Information Request')
    )
    reason = forms.ChoiceField(choices=REASON, label='Reason', help_text="    ")
    captcha = CaptchaField()
    template_name = 'public_form/public_form.txt'
    subject_template_name = "public_form/public_form_subject.txt"




