from django.urls import path
from django.views.generic import TemplateView
# from django.urls import reverse_lazy
from . import views
from django.contrib.auth.decorators import login_required

app_name='accounts'

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name="userena/member_table.html"), login_url='/accounts/signin/?next=/accounts/'), name='member_table'),
    # path('pdf/', login_required(TemplateView.as_view(template_name="userena/contact_pdf.html"), login_url='/accounts/signin/?next=/accounts/'), name='contact_pdf'),
    # path('pdf/', login_required(views.ContactPDFView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='contact_pdf'),
    path('pdf/', views.ContactPDFView.as_view(), name='contact_pdf')
]