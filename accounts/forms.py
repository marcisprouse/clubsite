# from django import forms

from userena.utils import get_profile_model

from userena.forms import EditProfileForm


class EditProfileFormExtra(EditProfileForm):
    class Meta:
        model = get_profile_model()
        exclude = ["user", "certificate_number"]