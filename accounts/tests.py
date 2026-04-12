from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, SimpleTestCase

from accounts.views import signin_to_home


class SigninRedirectTests(SimpleTestCase):
    def test_signin_ignores_next_and_redirects_home(self):
        request = RequestFactory().post(
            '/accounts/signin/?next=/accounts/not-the-homepage/'
        )
        request.user = AnonymousUser()

        with patch('accounts.views.userena_views.signin') as userena_signin:
            userena_signin.return_value = 'response'

            response = signin_to_home(request)

        self.assertEqual(response, 'response')
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
