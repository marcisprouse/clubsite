from django import forms
from django.forms import ModelForm
from .models import Badge
from accounts.models import MyProfile
from django.utils import timezone
# from multiselectfield import MultiSelectField
# from django.forms import ModelMultipleChoiceField, DateField
# from django.forms import CheckboxSelectMultiple



class ActiveMemberChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        first_name = obj.user.first_name or obj.user.username
        last_name = obj.user.last_name or ""
        display_name = f"{last_name}, {first_name}".strip(", ")
        return f"{display_name} (#{obj.member_id})"


class CreateBadgeForm(ModelForm):
    class Meta:
        model = Badge
        fields = "__all__"

    members = ActiveMemberChoiceField(
        queryset=MyProfile.objects.all().order_by('user__last_name', 'user__first_name', 'member_id'),
        widget=forms.SelectMultiple(attrs={"size": 16})
    )

    print_date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    badge_color = forms.ChoiceField(choices=Badge.COLOR_CHOICES, initial='blue')


    def __init__(self, *args, **kwargs):
        super(CreateBadgeForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['members'].queryset = MyProfile.objects.filter(is_active_member=True).order_by(
                'user__last_name', 'user__first_name', 'member_id'
            )
        self.fields['members'].help_text = "Search by last name, first name, or member number, then check one or more members."
