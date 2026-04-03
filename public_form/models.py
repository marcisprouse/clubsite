from django.db import models


class MembershipApplication(models.Model):
    deed_owner_names = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_1 = models.CharField(max_length=50)
    phone_2 = models.CharField(max_length=50, blank=True)
    primary_address = models.CharField(max_length=255, blank=True)

    previous_owner_names = models.CharField(max_length=255, blank=True)
    membership_number = models.CharField(max_length=100, blank=True)
    key_number = models.CharField(max_length=100, blank=True)

    tenant_names_contact = models.TextField(
        blank=True,
        help_text="If home is rented, provide tenant names and contact information.",
    )

    badge_1_name = models.CharField(max_length=255)
    badge_1_phone = models.CharField(max_length=50, blank=True)
    badge_1_email = models.EmailField(blank=True)

    badge_2_name = models.CharField(max_length=255, blank=True)
    badge_2_phone = models.CharField(max_length=50, blank=True)
    badge_2_email = models.EmailField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-submitted_at",)

    def __str__(self):
        return f"{self.deed_owner_names} ({self.submitted_at:%Y-%m-%d})"
