from django.contrib import admin
from django.contrib.admin.utils import quote
from django.http import Http404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from weasyprint import HTML

from .models import MembershipApplication


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = ("deed_owner_names", "phone_1", "badge_1_email", "submitted_at", "download_pdf_link")
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/download-pdf/",
                self.admin_site.admin_view(self.download_single_pdf),
                name="public_form_membershipapplication_download_pdf",
            ),
        ]
        return custom_urls + urls

    def _render_pdf_response(self, request, applications, filename):
        html = render_to_string(
            "public_form/membership_application_pdf.html",
            {
                "applications": applications,
                "generated_at": timezone.localtime(),
            },
        )
        pdf_bytes = HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf()
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def download_pdf_link(self, obj):
        url = reverse(
            "admin:public_form_membershipapplication_download_pdf",
            args=[quote(obj.pk)],
        )
        return format_html('<a href="{}" title="Download PDF" style="font-size:18px;">&#128229;</a>', url)

    download_pdf_link.short_description = "PDF"

    def download_single_pdf(self, request, object_id):
        try:
            application = self.get_queryset(request).get(pk=object_id)
        except MembershipApplication.DoesNotExist as exc:
            raise Http404("Application not found") from exc
        filename = f"membership_application_{application.pk}.pdf"
        return self._render_pdf_response(request, [application], filename)

    @admin.action(description="Download Selected Applications As PDF")
    def download_selected_as_pdf(self, request, queryset):
        applications = queryset.order_by("submitted_at")
        return self._render_pdf_response(request, applications, "membership_applications.pdf")
