from django.urls import path
from django.views.generic import TemplateView
# from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

app_name='for_sale'

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name="for_sale/certificates_for_sale.html"), login_url='/accounts/signin/?next=/accounts/'), name='certificates_sale'),
]
