"""clubsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from pages.sitemaps import StaticSitemap

from django.conf.urls import url

sitemaps = {
    'static':StaticSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('userena.urls')),
    path('members/', include('accounts.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('reports/', include('reports.urls')),
    path('blast/', include('blast.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', include('pages.urls')),
    path('minutes/', include('minutes.urls', namespace='minutes')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
    path('badges/', include('badges.urls', namespace='badges')),
    path('invoices/', include('invoices.urls', namespace='invoices')),
    path('ads/', include('ads.urls')),
    path('tables/', include('tables.urls')),
    path('schedule/', include('schedule.urls')),
    path('contact/', include('contact_form.urls')),
    path('public/', include('public_form.urls')),
    path('captcha/', include('captcha.urls')),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('android-chrome-192x192.png', serve, {
            'path': 'static/android-chrome-192x192.png',
        }
    ),
]

urlpatterns += [
    path('site.webmanifest', serve, {
            'path': 'static/site.webmanifest',
        }
    ),
]



admin.site.site_header = "Coyote Lakes Recreation Club Admin Panel"
admin.site.site_title = "Coyote Lakes Recreation Club Portal"
admin.site.index_title = "Welcome to the Coyote Lakes Recreation Club Portal!"
