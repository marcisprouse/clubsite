import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.csrf import csrf_failure as default_csrf_failure

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django_renderpdf.views import PDFView
from userena import views as userena_views
# from django.views import View
from accounts.models import MyProfile

logger = logging.getLogger(__name__)


@never_cache
def signin_to_home(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('/')

    return userena_views.signin(
        request,
        redirect_signin_function=lambda redirect=None, user=None: '/',
    )


def csrf_failure(request, reason=''):
    logger.warning(
        'CSRF failure path=%s host=%s origin=%s referer=%s reason=%s',
        request.path,
        request.META.get('HTTP_HOST'),
        request.META.get('HTTP_ORIGIN'),
        request.META.get('HTTP_REFERER'),
        reason,
    )

    if request.path == settings.LOGIN_URL:
        host = getattr(settings, 'CANONICAL_HOST', 'www.coyotelakesrecreationclub.org')
        return HttpResponseRedirect('https://%s%s' % (host, settings.LOGIN_URL))

    return default_csrf_failure(request, reason=reason)


class ContactPDFView(LoginRequiredMixin, PDFView):
    """Generate labels for some Shipments.

    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    template_name = 'userena/contact_pdf.html'
    download_name = 'contacts.pdf'


    def get_context_data(request):
        """Pass some extra context to the template."""


        all_members = MyProfile.objects.all().order_by('user__last_name')
        all_members_list=[]

        for member in all_members:
            all_members_list.append(member)


        context = {'request':request,
                  'all_members':all_members,
                  'all_members_list':all_members_list,

                  }

        return context;
