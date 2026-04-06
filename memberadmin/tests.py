from django.contrib.auth.models import User
from django.test import TestCase

from memberadmin.services import generate_temporary_password, generate_username


class MemberAdminServiceTests(TestCase):
    def test_generate_username_uses_rule(self):
        username = generate_username("Melauree", "Housman", "19663")
        self.assertEqual(username, "housman.me19663")

    def test_generate_username_extends_first_name_until_unique(self):
        User.objects.create_user(username="housman.me19663", password="testpass$1")
        username = generate_username("Melvin", "Housman", "19663")
        self.assertEqual(username, "housman.mel19663")

    def test_generate_password_returns_working_string(self):
        password = generate_temporary_password("Tod", "Cummings")
        self.assertGreaterEqual(len(password), 8)
        self.assertIn("$", password)

