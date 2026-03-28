from django.urls import path, reverse_lazy
from . import views

app_name='tables'
urlpatterns = [
    path('', views.TableListView.as_view(), name='all_tables'),
    #path('tables', views.TableListView.as_view(), name='all'),
    path('table/<int:pk>', views.TableDetailView.as_view(), name='table_detail'),
    path('table/create',
         views.TableCreateView.as_view(success_url=reverse_lazy('tables:all_tables')), name='table_create'),
    path('table/<int:pk>/update',
         views.TableUpdateView.as_view(success_url=reverse_lazy('tables:all_tables')), name='table_update'),
    path('table/<int:pk>/delete',
         views.TableDeleteView.as_view(success_url=reverse_lazy('tables:all_tables')), name='table_delete'),
    path('table_picture/<int:pk>', views.stream_file, name='table_picture'),
    path('table/<int:pk>/comm',
        views.CommCreateView.as_view(), name='table_comm_create'),
    path('comm/<int:pk>/delete',
        views.CommDeleteView.as_view(success_url=reverse_lazy('tables:all_tables')), name='table_comm_delete'),
]
