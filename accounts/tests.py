from unittest.mock import Mock, patch

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings

from accounts.views import signin_to_home
from clubsite.middleware import CanonicalHostMiddleware


class SigninRedirectTests(SimpleTestCase):
    def test_signin_ignores_next_and_redirects_home(self):
        request = RequestFactory().post(
            '/accounts/signin/?next=/accounts/not-the-homepage/'
        )
        request.user = AnonymousUser()

        with patch('accounts.views.userena_views.signin') as userena_signin:
            userena_signin.return_value = HttpResponse('response')

            response = signin_to_home(request)

        self.assertEqual(response.content, b'response')
        redirect_function = userena_signin.call_args.kwargs['redirect_signin_function']
        self.assertEqual(redirect_function('/accounts/not-the-homepage/', None), '/')

    def test_signin_redirects_authenticated_user_home(self):
        request = RequestFactory().get('/accounts/signin/')
        request.user = type('AuthenticatedUser', (), {'is_authenticated': True})()

        with patch('accounts.views.userena_views.signin') as userena_signin:
            response = signin_to_home(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        userena_signin.assert_not_called()

    def test_signin_response_is_not_cached(self):
        request = RequestFactory().get('/accounts/signin/')
        request.user = AnonymousUser()

        with patch('accounts.views.userena_views.signin') as userena_signin:
            userena_signin.return_value = HttpResponse('signin form')
            response = signin_to_home(request)

        self.assertIn('no-store', response['Cache-Control'])


class CanonicalHostMiddlewareTests(SimpleTestCase):
    @override_settings(
        CANONICAL_HOST='www.coyotelakesrecreationclub.org',
        CANONICAL_REDIRECT_HOSTS=['coyotelakesrecreationclub.org'],
        ENV='production',
    )
    def test_redirects_bare_domain_to_www(self):
        get_response = Mock(return_value=HttpResponse('ok'))
        middleware = CanonicalHostMiddleware(get_response)
        request = RequestFactory().get(
            '/accounts/signin/?next=/accounts/',
            HTTP_HOST='coyotelakesrecreationclub.org',
        )

        response = middleware(request)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response['Location'],
            'https://www.coyotelakesrecreationclub.org/accounts/signin/?next=/accounts/',
        )
        get_response.assert_not_called()

    @override_settings(
        CANONICAL_HOST='www.coyotelakesrecreationclub.org',
        CANONICAL_REDIRECT_HOSTS=['coyotelakesrecreationclub.org'],
        ENV='production',
    )
    def test_redirects_bare_domain_with_port(self):
        middleware = CanonicalHostMiddleware(Mock(return_value=HttpResponse('ok')))
        request = RequestFactory().get(
            '/accounts/signin/',
            HTTP_HOST='COYOTELAKESRECREATIONCLUB.ORG:443',
        )

        response = middleware(request)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response['Location'],
            'https://www.coyotelakesrecreationclub.org/accounts/signin/',
        )

    @override_settings(
        CANONICAL_HOST='www.coyotelakesrecreationclub.org',
        CANONICAL_REDIRECT_HOSTS=[],
        SITE_DOMAINS=['www.coyotelakesrecreationclub.org', 'coyotelakesrecreationclub.org'],
        ENV='production',
    )
    def test_redirects_bare_site_domain_even_without_redirect_hosts_setting(self):
        get_response = Mock(return_value=HttpResponse('ok'))
        middleware = CanonicalHostMiddleware(get_response)
        request = RequestFactory().get(
            '/',
            HTTP_HOST='coyotelakesrecreationclub.org',
        )

        response = middleware(request)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response['Location'],
            'https://www.coyotelakesrecreationclub.org/',
        )
        get_response.assert_not_called()

    @override_settings(
        CANONICAL_HOST='coyotelakesrecreationclub.org',
        CANONICAL_REDIRECT_HOSTS=[],
        SITE_DOMAINS=['www.coyotelakesrecreationclub.org', 'coyotelakesrecreationclub.org'],
        ENV='production',
    )
    def test_forces_bare_domain_to_www_even_if_env_canonical_host_is_wrong(self):
        get_response = Mock(return_value=HttpResponse('ok'))
        middleware = CanonicalHostMiddleware(get_response)
        request = RequestFactory().get(
            '/accounts/signin/',
            HTTP_HOST='coyotelakesrecreationclub.org',
        )

        response = middleware(request)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response['Location'],
            'https://www.coyotelakesrecreationclub.org/accounts/signin/',
        )
        get_response.assert_not_called()

    @override_settings(
        CANONICAL_HOST='www.coyotelakesrecreationclub.org',
        CANONICAL_REDIRECT_HOSTS=['coyotelakesrecreationclub.org'],
        ENV='production',
        USE_X_FORWARDED_HOST=True,
    )
    def test_redirects_bare_browser_host_even_when_forwarded_host_is_www(self):
        get_response = Mock(return_value=HttpResponse('ok'))
        middleware = CanonicalHostMiddleware(get_response)
        request = RequestFactory().get(
            '/accounts/signin/',
            HTTP_HOST='coyotelakesrecreationclub.org',
            HTTP_X_FORWARDED_HOST='www.coyotelakesrecreationclub.org',
        )

        response = middleware(request)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response['Location'],
            'https://www.coyotelakesrecreationclub.org/accounts/signin/',
        )
        get_response.assert_not_called()

    @override_settings(
        CANONICAL_HOST='www.coyotelakesrecreationclub.org',
        CANONICAL_REDIRECT_HOSTS=['coyotelakesrecreationclub.org'],
        ENV='production',
    )
    def test_allows_canonical_host(self):
        get_response = Mock(return_value=HttpResponse('ok'))
        middleware = CanonicalHostMiddleware(get_response)
        request = RequestFactory().get(
            '/',
            HTTP_HOST='www.coyotelakesrecreationclub.org',
        )

        response = middleware(request)

        self.assertEqual(response.status_code, 200)
        get_response.assert_called_once_with(request)
