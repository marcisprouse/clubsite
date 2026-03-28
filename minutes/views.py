from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from .models import PostMinute

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity

from .forms import SearchForm

from django.db.models import Count
from django.contrib.auth.decorators import login_required

# These are for the if not request.user.is_authenticated in the views.
'''from django.conf import settings
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin'''




def post_minutes_list(request):
    object_list = PostMinute.published.all()
    paginator = Paginator(object_list, 4) # 4 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'minutes/post_minutes/minutes_list.html',
                 {'page': page,
                  'posts': posts})



def post_minutes_detail(request, year, month, day, post_minutes):
    post_minutes = get_object_or_404(PostMinute, slug=post_minutes,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    return render(request,
                  'minutes/post_minutes/minutes_detail.html',
                  {'post_minutes': post_minutes,
                  })



class PostMinuteListView(ListView):
    queryset = PostMinute.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'minutes/post_minutes/minutes_list.html'



def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='C') + \
                            SearchVector('attendance', weight='A') + \
                            SearchVector('body', weight='A')
            search_query = SearchQuery(query)

            results = PostMinute.published.annotate(
                 search=search_vector,
                 rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    return render(request,
                  'minutes/post_minutes/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})



@login_required
def post_minutes_list_secure(request):
    return render(request, 'minutes/post_minutes/minutes_list.html')


