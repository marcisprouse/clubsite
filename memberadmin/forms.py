from django import forms
from django.forms import formset_factory
from django.utils import timezone


class NewMemberHouseholdForm(forms.Form):
    certificate_address_street_number = forms.CharField(
        label="Street number",
        max_length=20,
        help_text="Example: 11542",
    )
    certificate_address_route = forms.CharField(
        label="Street name",
        max_length=255,
        help_text="Example: W Rattlesnake Ct",
    )
    certificate_purchase_date = forms.DateField(
        label="Purchase date",
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    key_number_one = forms.IntegerField(label="Key number one", required=False)
    key_number_two = forms.IntegerField(label="Key number two", required=False)
    key_notes = forms.CharField(
        label="Key notes",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
    )
    board_recipient = forms.EmailField(
        label="Board email",
        initial="board@coyotelakesrecreationclub.org",
        required=False,
    )
    send_board_email = forms.BooleanField(
        label="Send board email",
        initial=True,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("key_number_two") and not cleaned_data.get("key_number_one"):
            raise forms.ValidationError("Enter key number one before key number two.")
        return cleaned_data


PRIVACY_CHOICES = (
    ("registered", "Registered"),
    ("closed", "Closed"),
)

RESIDENCY_CHOICES = (
    ("full_time", "Full-time resident"),
    ("part_time", "Part-time resident"),
    ("renter", "Renter"),
    ("landlord", "Landlord with transferred membership"),
    ("other", "Other contact"),
)


class NewMemberForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    privacy = forms.ChoiceField(choices=PRIVACY_CHOICES, initial="registered")
    residency = forms.ChoiceField(choices=RESIDENCY_CHOICES, initial="full_time")
    title = forms.CharField(max_length=4, required=False)
    sub_title = forms.CharField(max_length=4, required=False, label="Sub title")
    cell_phone = forms.CharField(max_length=16, required=False)
    other_phone = forms.CharField(max_length=16, required=False)
    temporary_password = forms.CharField(
        required=False,
        help_text="Leave blank to auto-generate a working temporary password.",
    )
    exclude_address_from_site = forms.BooleanField(
        required=False,
        label="Hide address on site",
    )
    subscribe_to_general_newsletter = forms.BooleanField(
        required=False,
        initial=True,
        label="Subscribe to General Newsletter",
    )
    member_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
    )


NewMemberFormSet = formset_factory(
    NewMemberForm,
    extra=1,
    min_num=1,
    validate_min=True,
)

