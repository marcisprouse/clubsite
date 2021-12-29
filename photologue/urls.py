from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from .views import (GalleryArchiveIndexView, GalleryDateDetailView, GalleryDayArchiveView, GalleryDetailView,
                    GalleryListView, GalleryMonthArchiveView, GalleryYearArchiveView, PhotoArchiveIndexView,
                    PhotoDateDetailView, PhotoDayArchiveView, PhotoDetailView, PhotoListView, PhotoMonthArchiveView,
                    PhotoYearArchiveView)

"""NOTE: the url names are changing. In the long term, I want to remove the 'pl-'
prefix on all urls, and instead rely on an application namespace 'photologue'.

At the same time, I want to change some URL patterns, e.g. for pagination. Changing the urls
twice within a few releases, could be confusing, so instead I am updating URLs bit by bit.

The new style will coexist with the existing 'pl-' prefix for a couple of releases.

"""

app_name = 'photologue'
urlpatterns = [
    re_path(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
            login_required(GalleryDateDetailView.as_view(month_format='%m'),
            login_url='/accounts/signin/?next=/accounts/'), name='gallery-detail'),
    re_path(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
            login_required(GalleryDayArchiveView.as_view(month_format='%m'),
            login_url='/accounts/signin/?next=/accounts/'), name='gallery-archive-day'),
    re_path(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
            login_required(GalleryMonthArchiveView.as_view(month_format='%m'),
            login_url='/accounts/signin/?next=/accounts/'), name='gallery-archive-month'),
    re_path(r'^gallery/(?P<year>\d{4})/$',
            login_required(GalleryYearArchiveView.as_view(),
            login_url='/accounts/signin/?next=/accounts/'), name='pl-gallery-archive-year'),
    path('gallery/',
         login_required(GalleryArchiveIndexView.as_view(),
         login_url='/accounts/signin/?next=/accounts/'), name='pl-gallery-archive'),
    path('',
         login_required(RedirectView.as_view(
             url=reverse_lazy('photologue:pl-gallery-archive'), permanent=True),
         login_url='/accounts/signin/?next=/accounts/'), name='pl-photologue-root'),
    re_path(r'^gallery/(?P<slug>[\-\d\w]+)/$',
            login_required(GalleryDetailView.as_view(), login_url='/accounts/signin/?next=/accounts/'), name='pl-gallery'),
    path('gallerylist/',
         login_required(GalleryListView.as_view(),
         login_url='/accounts/signin/?next=/accounts/'), name='gallery-list'),

    re_path(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
            login_required(PhotoDateDetailView.as_view(month_format='%m'),
            login_url='/accounts/signin/?next=/accounts/'), name='photo-detail'),
    re_path(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
            login_required(PhotoDayArchiveView.as_view(month_format='%m'),
            login_url='/accounts/signin/?next=/accounts/'), name='photo-archive-day'),
    re_path(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
            login_required(PhotoMonthArchiveView.as_view(month_format='%m'),
            login_url='/accounts/signin/?next=/accounts/'), name='photo-archive-month'),
    re_path(r'^photo/(?P<year>\d{4})/$',
            login_required(PhotoYearArchiveView.as_view(),
            login_url='/accounts/signin/?next=/accounts/'), name='pl-photo-archive-year'),
    path('photo/',
         login_required(PhotoArchiveIndexView.as_view(),
         login_url='/accounts/signin/?next=/accounts/'), name='pl-photo-archive'),

    re_path(r'^photo/(?P<slug>[\-\d\w]+)/$',
            login_required(PhotoDetailView.as_view(),
            login_url='/accounts/signin/?next=/accounts/'), name='pl-photo'),
    path('photolist/',
         login_required(PhotoListView.as_view(),
         login_url='/accounts/signin/?next=/accounts/'), name='photo-list'),
]
