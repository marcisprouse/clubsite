from django.contrib import admin
from certificates.models import Certificate

# Register your models here.
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_per_page = 1000
    list_display = ("certificate_number", "member_coyote_lakes_address", "name_associated_with_certificate", "is_for_sale", "is_for_sale_as_of_date", "is_club_held", "purchase_date", "certificate_notes", "created", "updated")
    search_fields = ["certificate_number", "member_coyote_lakes_address__route","member_coyote_lakes_address__street_number", "name_associated_with_certificate__user__last_name", "name_associated_with_certificate__user__first_name", "certificate_notes"]
    list_filter = ("is_for_sale", "is_for_sale_as_of_date", "is_club_held")


