from django import forms
from django.forms import ModelForm
from .models import Badge
from accounts.models import MyProfile
# from multiselectfield import MultiSelectField
# from django.forms import ModelMultipleChoiceField, DateField
# from django.forms import CheckboxSelectMultiple



class CreateBadgeForm(ModelForm):
    class Meta:
        model = Badge
        fields = '__all__'

    members = forms.ModelMultipleChoiceField(
        queryset=MyProfile.objects.all().order_by('user__username'),
        widget=forms.CheckboxSelectMultiple
    )

    print_date = forms.DateField()
    badge_color = forms.ChoiceField(choices=Badge.COLOR_CHOICES)


    def __init__(self, *args, **kwargs):
        super(CreateBadgeForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['members'].queryset = MyProfile.objects.filter(is_active_member=True).order_by('user__username')

