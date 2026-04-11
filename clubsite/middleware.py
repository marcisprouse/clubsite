from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, 'CANONICAL_HOST', None)
        redirect_hosts = getattr(settings, 'CANONICAL_REDIRECT_HOSTS', [])

        if canonical_host and request.get_host() in redirect_hosts:
            url = request.build_absolute_uri()
            url = url.replace('://%s' % request.get_host(), '://%s' % canonical_host, 1)
            return HttpResponsePermanentRedirect(url)

        return self.get_response(request)
