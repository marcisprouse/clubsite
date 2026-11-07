import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views import View

from .forms import ExistingHouseholdForm, NewMemberFormSet, NewMemberHouseholdForm
from .services import (
    add_members_to_existing_household,
    create_household,
    format_certificate_address,
    send_board_email,
)

logger = logging.getLogger(__name__)


def result_for_session(result, *, board_email_sent=False, board_email_error=""):
    return {
        "certificate_id": result.certificate.pk,
        "certificate_number": result.certificate.certificate_number,
        "certificate_address": format_certificate_address(
            result.certificate.member_coyote_lakes_address.street_number,
            result.certificate.member_coyote_lakes_address.route,
        ),
        "key_text": str(result.key_record) if result.key_record else "",
        "board_subject": result.board_subject,
        "board_body": result.board_body,
        "board_email_sent": board_email_sent,
        "board_email_error": board_email_error,
        "members": [
            {
                "full_name": member.user.get_full_name(),
                "member_id": member.profile.member_id,
                "username": member.username,
                "email": member.user.email,
                "password": member.password,
                "subscribed_to_newsletter": member.subscribed_to_newsletter,
            }
            for member in result.members
        ],
        "welcome_messages": [
            {
                "full_name": item["member"].user.get_full_name(),
                "email": item["member"].user.email,
                "username": item["member"].username,
                "body": item["body"],
            }
            for item in result.welcome_messages
        ],
    }


def send_requested_board_email(request, form, result, success_message, failure_message):
    board_email_sent = False
    board_email_error = ""
    if form.cleaned_data.get("send_board_email") and form.cleaned_data.get("board_recipient"):
        try:
            send_board_email(result, form.cleaned_data["board_recipient"])
            board_email_sent = True
            messages.success(request, success_message)
        except Exception as exc:
            board_email_error = str(exc)
            logger.exception("Board email failed for certificate %s", result.certificate.pk)
            messages.warning(request, failure_message)
    return board_email_sent, board_email_error


@method_decorator(sensitive_post_parameters(), name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class NewMemberHouseholdView(View):
    template_name = "memberadmin/new_member_household.html"

    def get(self, request):
        context = {
            "household_form": NewMemberHouseholdForm(),
            "member_formset": NewMemberFormSet(prefix="members"),
            "result": request.session.pop("new_member_household_result", None),
            "page_title": "Easy Add - Certificate and Member",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        household_form = NewMemberHouseholdForm(request.POST)
        member_formset = NewMemberFormSet(request.POST, prefix="members")

        if not household_form.is_valid() or not member_formset.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "household_form": household_form,
                    "member_formset": member_formset,
                    "page_title": "Easy Add - Certificate and Member",
                },
            )

        result = create_household(
            household_data=household_form.cleaned_data,
            member_forms_data=member_formset.cleaned_data,
        )

        board_email_sent, board_email_error = send_requested_board_email(
            request,
            household_form,
            result,
            "Board email sent.",
            "Household created, but the board email failed.",
        )
        request.session["new_member_household_result"] = result_for_session(
            result,
            board_email_sent=board_email_sent,
            board_email_error=board_email_error,
        )
        return redirect("memberadmin:new_member_household")


@method_decorator(sensitive_post_parameters(), name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class AddMembersToExistingHouseholdView(View):
    template_name = "memberadmin/new_member_household.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "household_form": ExistingHouseholdForm(),
                "member_formset": NewMemberFormSet(prefix="members"),
                "result": request.session.pop("existing_household_member_result", None),
                "existing_household": True,
                "page_title": "Add Member to Existing Household",
            },
        )

    def post(self, request):
        household_form = ExistingHouseholdForm(request.POST)
        member_formset = NewMemberFormSet(request.POST, prefix="members")

        if not household_form.is_valid() or not member_formset.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "household_form": household_form,
                    "member_formset": member_formset,
                    "existing_household": True,
                    "page_title": "Add Member to Existing Household",
                },
            )

        result = add_members_to_existing_household(
            certificate=household_form.cleaned_data["certificate"],
            member_forms_data=member_formset.cleaned_data,
            member_start_date=household_form.cleaned_data["member_start_date"],
        )
        board_email_sent, board_email_error = send_requested_board_email(
            request,
            household_form,
            result,
            "Board email sent.",
            "Member created, but the board email failed.",
        )
        request.session["existing_household_member_result"] = result_for_session(
            result,
            board_email_sent=board_email_sent,
            board_email_error=board_email_error,
        )
        return redirect("memberadmin:add_members_to_existing_household")
