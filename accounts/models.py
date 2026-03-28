from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from userena.models import UserenaBaseProfile
from address.models import AddressField
from certificates.models import Certificate
from django.utils import timezone
# from phone_field import PhoneField
from django.core.validators import RegexValidator
from django.utils.html import format_html
from django.contrib import admin


def from_20300():
    '''
    Returns the next default value for the `ones` field,
    starts from 20300
    '''
    # Retrieve a list of `YourModel` instances, sort them by
    # the `ones` field and get the largest entry
    largest = MyProfile.objects.all().order_by('member_id').last()
    if not largest:
        # largest is `None` if `YourModel` has no instances
        # in which case we return the start value of 20300
        return 20300
    # If an instance of `YourModel` is returned, we get it's
    # `ones` attribute and increment it by 1
    return largest.member_id + 1

class MyProfile(UserenaBaseProfile):
    class Meta:
        app_label = "accounts"
        managed = True
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    user = models.OneToOneField(User,
                                 unique=True,
                                 verbose_name=_('user'),
                                 related_name='my_profile',
                                 on_delete=models.CASCADE,
                                 help_text="Process:  See instructions for adding a user. If the user name is not in the drop down, you must add them to the User table first.")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.user:
            self.user.delete()

    temporary_password = models.CharField(max_length=25, help_text="Enter the temporary password you provided to create this user's account. Be EXACT since they will use this password to log in for the first time.")
    member_id = models.PositiveIntegerField(unique=True, blank=True, null=True, editable=False, default=from_20300)
    title = models.CharField(max_length=4, blank=True, help_text="i.e. Dr., Mr., etc. Can be left blank")
    sub_title = models.CharField(max_length=4, blank=True, help_text="i.e. Jr., III, etc. Can be left blank")
    cell_phone = models.CharField(validators = [phoneNumberRegex], max_length = 16, blank=True, null=True, help_text="Enter in the format 5555555555")
    other_phone = models.CharField(validators = [phoneNumberRegex], max_length = 16, blank=True, null=True, help_text="Enter in the format 5555555555")
    is_active_member = models.BooleanField(default=False, help_text='This person is an active member. Could be a qualifying home-owner or renter. Usually landlord qualifying home-owner is not an active member. Check if true. Leave blank if false.')
    is_a_member_full_time_resident = models.BooleanField(default=False, help_text='This active member lives in our neighborhood all months of the year. Check if true. Leave blank if false.')
    is_a_renter_member = models.BooleanField(default=False, help_text='This active member is renting a home owned by a landlord who has transferred their membership to them. Check if true. Leave blank if false.')
    is_a_member_part_time_resident = models.BooleanField(default=False, help_text='This active member does not live in our neighborhood all months of the year. Check if true. Leave blank if false.')
    member_coyote_lakes_qualifying_address = models.ForeignKey(Certificate, on_delete=models.PROTECT, related_name='member_coyote_lakes_qualifying_address', blank=True, null=True, help_text='Choose address from dropdown, if applies to this profile.')
    exclude_member_coyote_lakes_address_from_site = models.BooleanField(default=False, help_text='Check if member requests that their address does NOT show up on site information. Leave blank to keep address appearing on site.')
    member_part_time_away_address = AddressField(related_name='member_part_time_away_address', null=True, blank=True, help_text='Only enter if this profile has two homes and go away for summer, but they hold the Coyote Lakes membership, not a renter; enter their away address here. Leave blank if does not apply.')
    is_a_landlord_with_transferred_membership = models.BooleanField(default=False, help_text='This person owns a qualifying home with a membership certificate, but has transferred their membership to their renter. Check if true. Leave blank if false.')
    landlord_away_address = AddressField(related_name='landlord_away_address', null=True, blank=True, help_text='Only enter if this profile owns a home with a membership, but their renters use the membership; enter their away address here. Leave blank if does not apply.')
    is_other = models.BooleanField(default=False, help_text="Check if this person doesn't fit other boxes.  May be community contact person.")
    other_contact_address = AddressField(related_name='other_contact_address', null=True, blank=True, help_text='Only enter if this profile is a non-member contact; enter address here. Leave blank if does not apply.')
    about_me = models.TextField(_('about me'), blank=True, help_text="    ")
    MONTH_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )
    birth_month = models.CharField(max_length=10,
                              choices=MONTH_CHOICES,
                              blank=True, null=True, default=None, help_text="   ")
    DAY_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
        (16, '16'),
        (17, '17'),
        (18, '18'),
        (19, '19'),
        (20, '20'),
        (21, '21'),
        (22, '22'),
        (23, '23'),
        (24, '24'),
        (25, '25'),
        (26, '26'),
        (27, '27'),
        (28, '28'),
        (29, '29'),
        (30, '30'),
        (31, '31'),
    )
    birth_day = models.SmallIntegerField(
                              choices=DAY_CHOICES,
                              blank=True, null=True, default=None, help_text="   ")
    favorite_activity = models.TextField(_('favorite activity'), blank=True, help_text="    ")
    favorite_snack = models.CharField(_('favorite snack'), max_length=125, blank=True, help_text="    ")
    member_notes = models.TextField(_('member notes'), blank=True, help_text="For administrative purposes")
    date_first_entered = models.DateField(default=timezone.now, blank=True, help_text="Enter date first entered from old table information.")
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.user
        return u"%s, %s ------ %s" % (self.user.last_name, self.user.first_name, self.user)


