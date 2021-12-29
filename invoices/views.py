from django.shortcuts import render
from certificates.models import Certificate
from django.views.generic import ListView, DetailView


# Create your views here.
class InvoiceListView(ListView):
    queryset = Certificate.objects.all().order_by('name_associated_with_certificate__user__last_name')

    context_object_name = 'invoices'

    template_name = 'invoices/invoice_list.html'


class InvoiceDetailView(DetailView):
    model = Certificate

    template_name = 'invoices/invoice_detail.html'


