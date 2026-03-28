from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'minutes'

urlpatterns = [
    # post views
    # path('', views.post_minutes_list, name='post_minutes_list'),
    # path('', views.PostMinuteListView.as_view(), name='post_minutes_list'),
    path('', login_required(views.PostMinuteListView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='post_minutes_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_minutes>/', login_required(views.post_minutes_detail, login_url='/accounts/signin/?next=/accounts/'),
        name='post_minutes_detail'),
    path('search/', login_required(views.post_search, login_url='/accounts/signin/?next=/accounts/'), name='post_search'),
]
