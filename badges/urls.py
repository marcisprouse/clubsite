from django.urls import path, re_path
from django.views.generic import TemplateView
# from django.urls import reverse_lazy
from . import views
import userena
from django.contrib.auth.decorators import login_required

app_name='badges'

urlpatterns = [
    path('', login_required(views.BadgeCreateView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='add_badge'),
    # path('labels/labels', login_required(TemplateView.as_view(template_name="badges/badge_labels.html"), login_url='/accounts/signin/?next=/accounts/'), name='badge_labels'),
    path('labels/labels/<username>', login_required(userena.views.profile_badge_detail, login_url='/accounts/signin/?next=/accounts/'), name='badge_labels'),
    path('labels/', login_required(views.BadgePDFView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='badge_list'),
    path('labels/<int:pk>', login_required(views.BadgeDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='badge_detail'),
]