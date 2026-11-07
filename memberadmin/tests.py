from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory
from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase

from address.models import Address, Country, Locality, State
from certificates.models import Certificate
from memberadmin.forms import ExistingHouseholdForm, NewMemberFormSet
from newsletter.models import Newsletter, Subscription
from memberadmin.services import (
    add_members_to_existing_household,
    create_certificate_address,
    create_household,
    format_certificate_address,
    generate_temporary_password,
    generate_username,
)
from memberadmin.views import NewMemberHouseholdView


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

    def test_welcome_details_use_generated_username_without_email(self):
        member = SimpleNamespace(
            username="harrison.wa11661",
            password="Riverstone$27",
            user=SimpleNamespace(first_name="Walter", email=""),
        )

        body = render_to_string(
            "memberadmin/emails/welcome_email.txt",
            {
                "member": member,
                "signin_url": "https://www.coyotelakesrecreationclub.org/accounts/signin/",
            },
        )

        self.assertIn("username: harrison.wa11661", body)

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

    def test_create_certificate_address_uses_address_model_relations(self):
        address = create_certificate_address("11661", "W Yucca Ct")

        self.assertEqual(address.locality.name, "Surprise")
        self.assertEqual(address.locality.postal_code, "85378")
        self.assertEqual(address.locality.state.name, "Arizona")
        self.assertEqual(address.locality.state.code, "AZ")
        self.assertEqual(address.locality.state.country.name, "United States")
        self.assertEqual(address.locality.state.country.code, "US")
        self.assertEqual(
            address.formatted,
            "11661 W Yucca Ct, Surprise, AZ 85378, USA",
        )

    def test_household_failure_rolls_back_certificate_address(self):
        household_data = {
            "certificate_address_street_number": "11661",
            "certificate_address_route": "W Yucca Ct",
            "certificate_purchase_date": "2026-11-02",
        }
        member_data = [{
            "first_name": "Walter",
            "last_name": "Harrison",
            "email": "walter@example.com",
            "privacy": "registered",
            "residency": "full_time",
            "temporary_password": "short",
            "subscribe_to_general_newsletter": False,
        }]

        with self.assertRaises(ValidationError):
            create_household(
                household_data=household_data,
                member_forms_data=member_data,
            )

        self.assertFalse(Address.objects.exists())
        self.assertFalse(Locality.objects.exists())
        self.assertFalse(State.objects.exists())
        self.assertFalse(Country.objects.exists())
        self.assertFalse(Certificate.objects.exists())

    def test_create_household_succeeds_with_related_certificate_address(self):
        result = create_household(
            household_data={
                "certificate_address_street_number": "11661",
                "certificate_address_route": "W Yucca Ct",
                "certificate_purchase_date": "2026-11-02",
            },
            member_forms_data=[{
                "first_name": "Walter",
                "last_name": "Harrison",
                "email": "walter@example.com",
                "privacy": "registered",
                "residency": "full_time",
                "temporary_password": "Riverstone$27",
                "subscribe_to_general_newsletter": False,
            }],
        )

        self.assertEqual(result.certificate.member_coyote_lakes_address.locality.name, "Surprise")
        self.assertEqual(result.certificate.name_associated_with_certificate, "Walter Harrison")
        self.assertEqual(len(result.members), 1)
        self.assertTrue(result.members[0].user.check_password("Riverstone$27"))

    def test_member_without_email_is_created_and_subscribed_for_future_delivery(self):
        Newsletter.objects.create(
            title="General Newsletter",
            slug="general-newsletter",
            email="board@example.com",
            sender="CLRC Board",
        )
        result = create_household(
            household_data={
                "certificate_address_street_number": "11661",
                "certificate_address_route": "W Yucca Ct",
                "certificate_purchase_date": "2026-11-02",
            },
            member_forms_data=[{
                "first_name": "Walter",
                "last_name": "Harrison",
                "email": "",
                "privacy": "registered",
                "residency": "full_time",
                "temporary_password": "Riverstone$27",
                "subscribe_to_general_newsletter": True,
            }],
        )

        member = result.members[0]
        subscription = Subscription.objects.get(user=member.user)
        self.assertEqual(member.user.email, "")
        self.assertTrue(member.username)
        self.assertTrue(subscription.subscribed)
        self.assertEqual(subscription.email, "")

        member.user.email = "walter@example.com"
        member.user.save(update_fields=["email"])
        subscription = Subscription.objects.get(pk=subscription.pk)
        self.assertEqual(subscription.email, "walter@example.com")

    def test_add_member_to_existing_household_reuses_certificate_and_address(self):
        address = create_certificate_address("11661", "W Yucca Ct")
        certificate = Certificate.objects.create(
            member_coyote_lakes_address=address,
            name_associated_with_certificate="Walter Harrison",
            purchase_date="2022-11-02",
            is_for_sale_as_of_date=None,
        )

        result = add_members_to_existing_household(
            certificate=certificate,
            member_start_date="2026-11-07",
            member_forms_data=[{
                "first_name": "Nance",
                "last_name": "Harrison",
                "email": "nance@example.com",
                "privacy": "registered",
                "residency": "full_time",
                "temporary_password": "Riverstone$28",
                "subscribe_to_general_newsletter": False,
            }],
        )

        certificate.refresh_from_db()
        self.assertEqual(Certificate.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(result.certificate, certificate)
        self.assertEqual(
            result.members[0].profile.member_coyote_lakes_qualifying_address,
            certificate,
        )
        self.assertEqual(
            certificate.name_associated_with_certificate,
            "Walter Harrison, Nance Harrison",
        )

    def test_existing_household_failure_rolls_back_new_member(self):
        address = create_certificate_address("11661", "W Yucca Ct")
        certificate = Certificate.objects.create(
            member_coyote_lakes_address=address,
            name_associated_with_certificate="Walter Harrison",
            purchase_date="2022-11-02",
            is_for_sale_as_of_date=None,
        )

        with self.assertRaises(ValidationError):
            add_members_to_existing_household(
                certificate=certificate,
                member_start_date="2026-11-07",
                member_forms_data=[{
                    "first_name": "Nance",
                    "last_name": "Harrison",
                    "email": "nance@example.com",
                    "privacy": "registered",
                    "residency": "full_time",
                    "temporary_password": "short",
                    "subscribe_to_general_newsletter": False,
                }],
            )

        certificate.refresh_from_db()
        self.assertEqual(certificate.name_associated_with_certificate, "Walter Harrison")
        self.assertFalse(User.objects.filter(email="nance@example.com").exists())
        self.assertEqual(Certificate.objects.count(), 1)


class MemberAdminFormTests(TestCase):
    def member_formset_data(self, first_email, second_email):
        return {
            "members-TOTAL_FORMS": "2",
            "members-INITIAL_FORMS": "0",
            "members-MIN_NUM_FORMS": "1",
            "members-MAX_NUM_FORMS": "1000",
            "members-0-first_name": "Walter",
            "members-0-last_name": "Harrison",
            "members-0-email": first_email,
            "members-0-privacy": "registered",
            "members-0-residency": "full_time",
            "members-1-first_name": "Nance",
            "members-1-last_name": "Harrison",
            "members-1-email": second_email,
            "members-1-privacy": "registered",
            "members-1-residency": "full_time",
        }

    def test_rejects_duplicate_emails_in_same_household(self):
        formset = NewMemberFormSet(
            self.member_formset_data("shared@example.com", "SHARED@example.com"),
            prefix="members",
        )

        self.assertFalse(formset.is_valid())
        self.assertIn(
            "Each member must have a different email address.",
            formset.forms[1].errors["email"],
        )

    def test_rejects_email_already_used_by_existing_user(self):
        User.objects.create_user(
            username="existing",
            email="existing@example.com",
            password="testpass$1",
        )
        data = self.member_formset_data("EXISTING@example.com", "new@example.com")
        formset = NewMemberFormSet(data, prefix="members")

        self.assertFalse(formset.is_valid())
        self.assertIn(
            "A user with this email address already exists.",
            formset.forms[0].errors["email"],
        )

    def test_allows_multiple_members_without_email(self):
        formset = NewMemberFormSet(
            self.member_formset_data("", ""),
            prefix="members",
        )

        self.assertTrue(formset.is_valid(), formset.errors)

    def test_existing_household_form_selects_certificate(self):
        address = create_certificate_address("11661", "W Yucca Ct")
        certificate = Certificate.objects.create(
            member_coyote_lakes_address=address,
            purchase_date="2022-11-02",
            is_for_sale_as_of_date=None,
        )
        form = ExistingHouseholdForm({
            "certificate": certificate.pk,
            "member_start_date": "2026-11-07",
            "board_recipient": "",
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["certificate"], certificate)

    def test_existing_household_page_renders_workflow(self):
        body = render_to_string(
            "memberadmin/new_member_household.html",
            {
                "household_form": ExistingHouseholdForm(),
                "member_formset": NewMemberFormSet(prefix="members"),
                "existing_household": True,
                "page_title": "Add Member to Existing Household",
            },
        )

        self.assertIn("Add Member to Existing Household", body)
        self.assertIn("certificate or address will be created.", body)


class MemberAdminViewTests(SimpleTestCase):
    def test_marks_all_post_parameters_as_sensitive(self):
        request = RequestFactory().get("/member-admin/")
        request.user = SimpleNamespace(is_active=True, is_staff=True)

        with patch.object(NewMemberHouseholdView, "get", return_value=HttpResponse("ok")):
            response = NewMemberHouseholdView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.sensitive_post_parameters, "__ALL__")
