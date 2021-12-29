from django.db import models
from certificates.models import Certificate

# Create your models here.
class Key(models.Model):
    key_number_one = models.PositiveIntegerField(unique=True, help_text='This number may not be greater than 2147483647')
    key_number_two = models.PositiveIntegerField(blank=True, null=True, help_text='This number may not be greater than 2147483647')
    certificate_and_qualifying_address_for_keys = models.OneToOneField(Certificate, on_delete=models.CASCADE, related_name='certificate_and_qualifying_address_for_keys', blank=True, null=True, help_text="If certificate needed does not appear, it needs to be created first.")
    key_notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['key_number_one']

    def __str__(self):
        if not self.key_number_two:
            return u"Key Number Assigned: %s" % (self.key_number_one)
        else:
            return u"Key Numbers Assigned: %s and %s" % (self.key_number_one, self.key_number_two)