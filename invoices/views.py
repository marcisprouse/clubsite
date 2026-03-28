from django.shortcuts import render
from certificates.models import Certificate
from django.views.generic import ListView, DetailView

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class InvoiceListView(ListView):
    queryset = Certificate.objects.all().order_by('certificate_number')

    context_object_name = 'invoices'

    template_name = 'invoices/invoice_list.html'

@method_decorator(staff_member_required, name='dispatch')
class InvoiceDetailView(DetailView):
    model = Certificate

    template_name = 'invoices/invoice_detail.html'


