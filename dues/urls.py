from django.urls import path
# from django.urls import reverse_lazy
from . import views
from django.contrib.auth.decorators import login_required

app_name='dues'

urlpatterns = [
    path('balance_list', login_required(views.BalanceListView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='balance_list'),
    path('<int:pk>', login_required(views.BalanceDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='balance_detail'),
]