# from django.shortcuts import render
from .models import Badge
from .forms import CreateBadgeForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django_renderpdf.views import PDFView
from datetime import timedelta
from django.utils import timezone
# from accounts.models import MyProfile

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class BadgeCreateView(CreateView):
    model = Badge
    form_class = CreateBadgeForm
    template_name = 'badges/add_badge.html'
    success_url = reverse_lazy('badges:badge_list')

@method_decorator(staff_member_required, name='dispatch')
class BadgeListView(ListView):
    queryset = Badge.objects.all()
    context_object_name = 'badges'
    template_name = 'badges/badge_list.html'

@method_decorator(staff_member_required, name='dispatch')
class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'badges/badge_detail.html'

@method_decorator(staff_member_required, name='dispatch')
class BadgePDFView(LoginRequiredMixin, PDFView):
    """Generate labels for some Shipments.

    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    template_name = 'badges/badge_list.html'
    prompt_download = True
    download_name = 'badges.pdf'


    def get_context_data(request):
        """Pass some extra context to the template."""

        all_badges = Badge.objects.all()

        all_badges_list=[]

        now = timezone.now()

        for badge in all_badges:

            past = badge.updated - timedelta(seconds=30)
            future = badge.updated + timedelta(seconds=30)

            if past <= now and now <= future:
                all_badges_list.append(badge)


        context = {'all_badges':all_badges,
                  'all_badges_list':all_badges_list
                  }
        return context;

