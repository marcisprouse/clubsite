import re
import secrets
from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from address.models import Address
from accounts.models import MyProfile
from certificates.models import Certificate
from keys.models import Key
from newsletter.models import Newsletter, Subscription
from userena import settings as userena_settings
from userena.models import UserenaSignup


@dataclass
class CreatedMemberSummary:
    user: User
    profile: MyProfile
    username: str
    password: str
    subscribed_to_newsletter: bool


@dataclass
class HouseholdCreationResult:
    certificate: Certificate
    key_record: Key
    members: list
    board_subject: str
    board_body: str
    welcome_messages: list


def normalize_fragment(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


def generate_username(first_name, last_name, street_number, reserved_usernames=None):
    reserved = set(reserved_usernames or [])
    first_clean = normalize_fragment(first_name)
    last_clean = normalize_fragment(last_name)
    street_clean = normalize_fragment(street_number)

    if not first_clean:
        first_clean = "me"
    if not last_clean:
        last_clean = "member"

    for length in range(2, max(len(first_clean), 2) + 1):
        candidate = f"{last_clean}.{first_clean[:length]}{street_clean}"
        if candidate not in reserved and not User.objects.filter(username=candidate).exists():
            return candidate

    suffix = 2
    while True:
        candidate = f"{last_clean}.{first_clean}{street_clean}{suffix}"
        if candidate not in reserved and not User.objects.filter(username=candidate).exists():
            return candidate
        suffix += 1


def generate_temporary_password(first_name, last_name):
    seed = normalize_fragment(first_name + last_name) or "memberpass"
    base = (seed + "sunsets")[:8]
    if "s" not in base:
        base = (base[:-1] + "s") if len(base) >= 8 else (base + "s")
    password = base.replace("s", "$", 1)
    while True:
        try:
            validate_password(password)
            return password
        except Exception:
            random_tail = secrets.token_hex(2)
            password = f"{seed[:4]}${random_tail}"


def find_general_newsletter():
    return (
        Newsletter.objects.filter(slug="general-newsletter").first()
        or Newsletter.objects.filter(slug="general_newsletter").first()
        or Newsletter.objects.filter(title__iexact="General Newsletter").first()
    )


def subscribe_member_to_general_newsletter(user):
    newsletter = find_general_newsletter()
    if newsletter is None:
        raise ValueError("General Newsletter was not found.")

    subscription, created = Subscription.objects.get_or_create(
        user=user,
        newsletter=newsletter,
        defaults={"subscribed": True, "unsubscribed": False},
    )
    if not created:
        subscription.subscribed = True
        subscription.unsubscribed = False
        subscription.save()


def build_certificate_name(member_forms_data):
    names = []
    for member_data in member_forms_data:
        full_name = f"{member_data['first_name']} {member_data['last_name']}".strip()
        if full_name:
            names.append(full_name)
    return ", ".join(names)


def build_board_subject(members):
    names = " & ".join(member.user.get_full_name() for member in members)
    return f"***IMPT: NEW MEMBER {names}"


def filter_member_forms(member_forms_data):
    filtered = []
    for member_data in member_forms_data:
        if not member_data:
            continue
        if member_data.get("first_name") and member_data.get("last_name") and member_data.get("email"):
            filtered.append(member_data)
    return filtered


def create_household(*, household_data, member_forms_data):
    member_forms_data = filter_member_forms(member_forms_data)
    reserved_usernames = set()

    with transaction.atomic():
        address = Address.objects.create(
            street_number=household_data["certificate_address_street_number"],
            route=household_data["certificate_address_route"],
            raw="",
            formatted=(
                f"{household_data['certificate_address_street_number']} "
                f"{household_data['certificate_address_route']}"
            ).strip(),
        )
        certificate = Certificate.objects.create(
            member_coyote_lakes_address=address,
            purchase_date=household_data["certificate_purchase_date"],
            name_associated_with_certificate=build_certificate_name(member_forms_data),
            is_for_sale=False,
            is_for_sale_as_of_date=None,
            is_club_held=False,
        )

        key_record = None
        if household_data.get("key_number_one"):
            key_record = Key.objects.create(
                key_number_one=household_data["key_number_one"],
                key_number_two=household_data.get("key_number_two"),
                certificate_and_qualifying_address_for_keys=certificate,
                key_notes=household_data.get("key_notes", ""),
            )

        created_members = []
        welcome_messages = []

        for member_data in member_forms_data:
            username = generate_username(
                member_data["first_name"],
                member_data["last_name"],
                household_data["certificate_address_street_number"],
                reserved_usernames=reserved_usernames,
            )
            reserved_usernames.add(username)
            temporary_password = member_data.get("temporary_password") or generate_temporary_password(
                member_data["first_name"],
                member_data["last_name"],
            )
            validate_password(temporary_password)

            user = User.objects.create_user(
                username=username,
                email=member_data["email"],
                password=temporary_password,
                first_name=member_data["first_name"],
                last_name=member_data["last_name"],
            )

            UserenaSignup.objects.update_or_create(
                user=user,
                defaults={
                    "activation_key": userena_settings.USERENA_ACTIVATED,
                    "last_active": timezone.now(),
                },
            )

            residency = member_data["residency"]
            profile = MyProfile.objects.create(
                user=user,
                privacy=member_data["privacy"],
                temporary_password=temporary_password,
                title=member_data.get("title", ""),
                sub_title=member_data.get("sub_title", ""),
                cell_phone=member_data.get("cell_phone", ""),
                other_phone=member_data.get("other_phone", ""),
                is_active_member=residency in {"full_time", "part_time", "renter"},
                is_a_member_full_time_resident=residency == "full_time",
                is_a_member_part_time_resident=residency == "part_time",
                is_a_renter_member=residency == "renter",
                is_a_landlord_with_transferred_membership=residency == "landlord",
                is_other=residency == "other",
                member_coyote_lakes_qualifying_address=certificate,
                exclude_member_coyote_lakes_address_from_site=member_data.get(
                    "exclude_address_from_site", False
                ),
                member_notes=member_data.get("member_notes", ""),
                date_first_entered=household_data["certificate_purchase_date"],
            )

            subscribed = False
            if member_data.get("subscribe_to_general_newsletter", True):
                subscribe_member_to_general_newsletter(user)
                subscribed = True

            member = CreatedMemberSummary(
                user=user,
                profile=profile,
                username=username,
                password=temporary_password,
                subscribed_to_newsletter=subscribed,
            )
            created_members.append(member)
            welcome_messages.append(
                {
                    "member": member,
                    "body": render_to_string(
                        "memberadmin/emails/welcome_email.txt",
                        {
                            "member": member,
                            "signin_url": "https://www.coyotelakesrecreationclub.org/accounts/signin/",
                        },
                    ).strip(),
                }
            )

        board_context = {
            "certificate": certificate,
            "key_record": key_record,
            "members": created_members,
            "welcome_messages": welcome_messages,
        }
        board_subject = build_board_subject(created_members)
        board_body = render_to_string("memberadmin/emails/board_body.txt", board_context).strip()

        return HouseholdCreationResult(
            certificate=certificate,
            key_record=key_record,
            members=created_members,
            board_subject=board_subject,
            board_body=board_body,
            welcome_messages=welcome_messages,
        )


def send_board_email(result, recipient):
    if not recipient:
        return
    message = EmailMessage(
        subject=result.board_subject,
        body=result.board_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    message.send(fail_silently=False)
