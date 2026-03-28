from django.shortcuts import render
from .models import Certificate
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchHomeForm

# Create your views here.
class CertificateListView(ListView):
    queryset = Certificate.objects.all().order_by('certificate_number')

    context_object_name = 'certificates'

    template_name = 'certificates/certificate_list.html'


class CertificateDetailView(DetailView):
    model = Certificate

    template_name = 'certificates/certificate_detail.html'



def home_search(request):
    form = SearchHomeForm()
    query = None
    results = []
    results_count = []
    if 'query' in request.GET:
        form = SearchHomeForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('member_coyote_lakes_address__route', weight='A') + \
                            SearchVector('member_coyote_lakes_address__street_number', weight='A') + \
                            SearchVector('member_coyote_lakes_qualifying_address__user__last_name', weight='A') + \
                            SearchVector('member_coyote_lakes_qualifying_address__user__first_name', weight='A')
            search_query = SearchQuery(query)

            results = Certificate.objects.annotate(
                 search=search_vector,
                 rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

            results = list(dict.fromkeys(results))

            for result in results:
                if result.exclude == False and result.name_associated_with_certificate:
                    results_count.append(result)





    return render(request,
                  'certificates/search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'results_count':results_count})


