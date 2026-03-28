# import form class from django
from django import forms
# from django.forms import ModelForm
# from schedule.models import Memberrsvp


class VolunteerForm(forms.Form):
    volunteer = forms.CharField(required=True, max_length=500, min_length=3, strip=True, help_text="Please let us know how you can help. Any amount of help is so apprecitated! If your profile has contact information, it will automatically appear.")


class MemberrsvpForm(forms.Form):
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )

    CHOICES = (
        ('------', '------'),
        ('Basket', 'Basket'),
        ('Decadent Dessert', 'Decadent Dessert'),
        ('Service', 'Service'),
        ('None - Maybe Next Year', 'None - Maybe Next Year'),
    )

    attending = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Attending:",
                                  initial='', widget=forms.Select(), required=True)

    mealchoice = forms.ChoiceField(choices = CHOICES, label="Which item will you bring for fundraising silent auction?",
                                  initial='------', widget=forms.Select(), required=False)

    guests = forms.CharField(required=False, max_length=500, min_length=3, strip=True, label="Notes:", help_text='Please indicate in this box the names of guests you plan to bring and whether or not they are club members or OUTSIDE of Coyote Lakes neighborhood.')

    memberrsvp = forms.CharField(required=False, max_length=500, min_length=3, strip=True, label="Notes:", help_text="This event is asking for you to bring a dish or an item.  Are you bringing something? Please indicate what in this box.  Thank you!")








