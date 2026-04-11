from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from accounts.views import signin_to_home


class SigninRedirectTests(SimpleTestCase):
    def test_signin_ignores_next_and_redirects_home(self):
        request = RequestFactory().post(
            '/accounts/signin/?next=/accounts/not-the-homepage/'
        )

        with patch('accounts.views.userena_views.signin') as userena_signin:
            userena_signin.return_value = 'response'

            response = signin_to_home(request)

        self.assertEqual(response, 'response')
        redirect_function = userena_signin.call_args.kwargs['redirect_signin_function']
        self.assertEqual(redirect_function('/accounts/not-the-homepage/', None), '/')
