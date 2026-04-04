from django.template.loader import render_to_string
from django.utils import timezone

from weasyprint import HTML


def render_membership_application_pdf(applications, *, base_url=None):
    html = render_to_string(
        "public_form/membership_application_pdf.html",
        {
            "applications": applications,
            "generated_at": timezone.localtime(),
        },
    )
    return HTML(string=html, base_url=base_url).write_pdf()
