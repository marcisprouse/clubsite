from django.urls import path
# from django.views.generic import TemplateView
# from django.urls import reverse_lazy
from . import views
from django.contrib.auth.decorators import login_required

app_name='invoices'

urlpatterns = [
    path('invoice_list', login_required(views.InvoiceListView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='invoice_list'),
    path('<int:pk>', login_required(views.InvoiceDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='invoice_detail'),
]