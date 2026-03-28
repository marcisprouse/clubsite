"""
View which can render and send email from a contact form.
"""

from django import http
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render

from .forms import ContactForm, StringKeyedDict, CustomContactForm


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

