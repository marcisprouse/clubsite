from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, 'CANONICAL_HOST', None)
        canonical_host_normalized = self._normalize_host(canonical_host)
        redirect_hosts = {
            self._normalize_host(host)
            for host in getattr(settings, 'CANONICAL_REDIRECT_HOSTS', [])
        }
        redirect_hosts.update(
            self._normalize_host(host)
            for host in getattr(settings, 'SITE_DOMAINS', [])
            if self._normalize_host(host) != canonical_host_normalized
        )
        request_host = self._normalize_host(request.get_host())

        if canonical_host and request_host != canonical_host_normalized and request_host in redirect_hosts:
            scheme = 'https' if request.is_secure() or getattr(settings, 'ENV', None) == 'production' else request.scheme
            url = '%s://%s%s' % (scheme, canonical_host, request.get_full_path())
            return HttpResponsePermanentRedirect(url)

        return self.get_response(request)

    @staticmethod
    def _normalize_host(host):
        if not host:
            return ''
        return host.split(':', 1)[0].rstrip('.').lower()
