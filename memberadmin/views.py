import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import NewMemberFormSet, NewMemberHouseholdForm
from .services import create_household, send_board_email

logger = logging.getLogger(__name__)


@method_decorator(staff_member_required, name="dispatch")
class NewMemberHouseholdView(View):
    template_name = "memberadmin/new_member_household.html"

    def get(self, request):
        context = {
            "household_form": NewMemberHouseholdForm(),
            "member_formset": NewMemberFormSet(prefix="members"),
            "result": request.session.pop("new_member_household_result", None),
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
                },
            )

        result = create_household(
            household_data=household_form.cleaned_data,
            member_forms_data=member_formset.cleaned_data,
        )

        board_email_sent = False
        board_email_error = ""
        if household_form.cleaned_data.get("send_board_email") and household_form.cleaned_data.get("board_recipient"):
            try:
                send_board_email(result, household_form.cleaned_data["board_recipient"])
                board_email_sent = True
                messages.success(request, "Board email sent.")
            except Exception as exc:
                board_email_error = str(exc)
                logger.exception("Board email failed for certificate %s", result.certificate.pk)
                messages.warning(request, "Household created, but the board email failed.")

        request.session["new_member_household_result"] = {
            "certificate_id": result.certificate.pk,
            "certificate_number": result.certificate.certificate_number,
            "certificate_address": (
                f"{result.certificate.member_coyote_lakes_address.street_number} "
                f"{result.certificate.member_coyote_lakes_address.route}"
            ).strip(),
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
                    "body": item["body"],
                }
                for item in result.welcome_messages
            ],
        }
        return redirect("memberadmin:new_member_household")

