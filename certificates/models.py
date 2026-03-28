from django.db import models
from address.models import AddressField
from django.utils import timezone


def from_10218():
    '''
    Returns the next default value for the `ones` field,
    starts from 10218
    '''
    # Retrieve a list of `YourModel` instances, sort them by
    # the `ones` field and get the largest entry
    largest = Certificate.objects.all().order_by('certificate_number').last()
    if not largest:
        # largest is `None` if `YourModel` has no instances
        # in which case we return the start value of 10218
        return 10218
    # If an instance of `YourModel` is returned, we get it's
    # `ones` attribute and increment it by 1
    return largest.certificate_number + 1



# Create your models here.
class Certificate(models.Model):
    certificate_number = models.PositiveIntegerField(unique=True, default=from_10218, editable=False, help_text='This number is auto-generated')
    exclude = models.BooleanField(default=False, help_text='Check if you want to exclude this certificate from the Home Lookup Search on the website.')
    name_associated_with_certificate = models.CharField(max_length=100, blank=True, null=True, help_text="Enter a name that associates this certificate to a member or members.")
    member_coyote_lakes_address = AddressField(related_name='member_coyote_lakes_address', null=False, help_text='Enter the Coyote Lakes address associated with the certificate number. If the certificate does not have an address associated with it, use the club address.')
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True, help_text='Delete date if not purchased yet.')
    is_for_sale = models.BooleanField(default=False, help_text='Check if true. Leave blank if false.')
    is_for_sale_as_of_date = models.DateField(default="", null=True, blank=True, help_text="Enter date the certificate is for sale.  Delete default date of now if not for sale.")
    is_club_held = models.BooleanField(default=False, help_text='This is usually true when a member surrenders the certificate to the club without selling. Check if true. Leave blank if false.')
    certificate_notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['certificate_number']


    def __str__(self):
        return u"Cert #: %s ---  %s   %s" % (self.certificate_number, self.member_coyote_lakes_address.street_number, self.member_coyote_lakes_address.route)
