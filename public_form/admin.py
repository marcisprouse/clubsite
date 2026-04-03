from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from weasyprint import HTML

from .models import MembershipApplication


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = ("deed_owner_names", "phone_1", "badge_1_email", "submitted_at")
    search_fields = (
        "deed_owner_names",
        "address",
        "phone_1",
        "phone_2",
        "badge_1_name",
        "badge_1_email",
        "badge_2_name",
        "badge_2_email",
    )
    readonly_fields = ("submitted_at",)
    actions = ("download_selected_as_pdf",)

    @admin.action(description="Download Selected Applications As PDF")
    def download_selected_as_pdf(self, request, queryset):
        applications = queryset.order_by("submitted_at")
        html = render_to_string(
            "public_form/membership_application_pdf.html",
            {
                "applications": applications,
                "generated_at": timezone.localtime(),
            },
        )
        pdf_bytes = HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf()
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="membership_applications.pdf"'
        return response
