from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect


class CanonicalHostMiddleware:
    FORCED_CANONICAL_HOSTS = {
        'coyotelakesrecreationclub.org': 'www.coyotelakesrecreationclub.org',
    }

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
        request_host = self._request_host(request)
        forced_canonical_host = self._forced_canonical_host(request, request_host)

        if forced_canonical_host:
            return self._redirect_to_host(request, forced_canonical_host)

        if canonical_host and request_host != canonical_host_normalized and request_host in redirect_hosts:
            return self._redirect_to_host(request, canonical_host)

        return self.get_response(request)

    @staticmethod
    def _redirect_to_host(request, host):
        scheme = 'https' if request.is_secure() or getattr(settings, 'ENV', None) == 'production' else request.scheme
        url = '%s://%s%s' % (scheme, host, request.get_full_path())
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            return HttpResponsePermanentRedirect(url)
        return HttpResponseRedirect(url)

    @classmethod
    def _forced_canonical_host(cls, request, request_host):
        forced_canonical_host = cls.FORCED_CANONICAL_HOSTS.get(request_host)
        if forced_canonical_host:
            return forced_canonical_host

        for source in ('HTTP_ORIGIN', 'HTTP_REFERER'):
            source_host = cls._url_host(request.META.get(source))
            forced_canonical_host = cls.FORCED_CANONICAL_HOSTS.get(source_host)
            if forced_canonical_host:
                return forced_canonical_host

        return None

    @classmethod
    def _request_host(cls, request):
        # Use the raw browser Host header so forwarded host settings cannot
        # hide bare-domain requests from the canonical redirect.
        return cls._normalize_host(request.META.get('HTTP_HOST') or request.get_host())

    @classmethod
    def _url_host(cls, url):
        if not url:
            return ''
        return cls._normalize_host(urlparse(url).netloc)

    @staticmethod
    def _normalize_host(host):
        if not host:
            return ''
        return host.split(':', 1)[0].rstrip('.').lower()
