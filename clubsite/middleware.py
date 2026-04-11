from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, 'CANONICAL_HOST', None)
        redirect_hosts = getattr(settings, 'CANONICAL_REDIRECT_HOSTS', [])

        if canonical_host and request.get_host() in redirect_hosts:
            scheme = 'https' if request.is_secure() else request.scheme
            url = '%s://%s%s' % (scheme, canonical_host, request.get_full_path())
            return HttpResponsePermanentRedirect(url)

        return self.get_response(request)
