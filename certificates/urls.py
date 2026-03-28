from django.urls import path
# from django.urls import reverse_lazy
from . import views
from django.contrib.auth.decorators import login_required

app_name='certificates'

urlpatterns = [
    path('certificate_list', login_required(views.CertificateListView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='certificate_list'),
    path('<int:pk>', login_required(views.CertificateDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='certificate_detail'),
    path('search/home', login_required(views.home_search, login_url='/accounts/signin/?next=/accounts/'), name='home_search'),
]