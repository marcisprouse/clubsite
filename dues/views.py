from django.shortcuts import render
from .models import Balance
from django.views.generic import ListView, DetailView


# Create your views here.
class BalanceListView(ListView):
    queryset = Balance.objects.all().order_by('cert')

    context_object_name = 'certs'

    template_name = 'dues/balance_list.html'


class BalanceDetailView(DetailView):
    model = Balance

    template_name = 'dues/balance_detail.html'

    def get_context_data(self, **kwargs):

        context = super(BalanceDetailView, self).get_context_data(**kwargs)

        context['last_import_date'] = Balance.objects.latest("updated").updated
        return context
