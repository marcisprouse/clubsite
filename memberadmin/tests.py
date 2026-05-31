from types import SimpleNamespace

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase

from memberadmin.services import (
    format_certificate_address,
    generate_temporary_password,
    generate_username,
)


class MemberAdminTemplateTests(SimpleTestCase):
    def test_board_email_uses_clean_certificate_address(self):
        body = render_to_string(
            "memberadmin/emails/board_body.txt",
            {
                "certificate": SimpleNamespace(certificate_number="12345"),
                "certificate_address": "17829 N Lainie Ct, Surprise, AZ 85378, USA",
                "key_record": None,
                "members": [],
                "welcome_messages": [],
            },
        )

        self.assertIn("17829 N Lainie Ct, Surprise, AZ 85378, USA", body)
        self.assertNotIn("17829 N Lainie Ct N Lainie Ct", body)

    def test_welcome_email_uses_email_as_login_username(self):
        member = SimpleNamespace(
            username="fritzler.mi17829nlainiect",
            password="michael$",
            user=SimpleNamespace(first_name="Michael", email="mikefritzler7@gmail.com"),
        )

        body = render_to_string(
            "memberadmin/emails/welcome_email.txt",
            {
                "member": member,
                "signin_url": "https://www.coyotelakesrecreationclub.org/accounts/signin/",
            },
        )

        self.assertIn("username: mikefritzler7@gmail.com", body)
        self.assertNotIn("username: fritzler.mi17829nlainiect", body)

    def test_format_certificate_address_removes_duplicate_route(self):
        address = format_certificate_address("17829", "N Lainie Ct N Lainie Ct")
        self.assertEqual(address, "17829 N Lainie Ct, Surprise, AZ 85378, USA")

    def test_format_certificate_address_removes_repeated_street_number(self):
        address = format_certificate_address("17829", "17829 N Lainie Ct")
        self.assertEqual(address, "17829 N Lainie Ct, Surprise, AZ 85378, USA")

    def test_format_certificate_address_does_not_duplicate_city_state_zip(self):
        address = format_certificate_address("17829", "N Lainie Ct, Surprise, AZ 85378, USA")
        self.assertEqual(address, "17829 N Lainie Ct, Surprise, AZ 85378, USA")


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
