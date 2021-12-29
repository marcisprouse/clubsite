from django.contrib.sitemaps import Sitemap
from django.urls import reverse



class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return [
            'pages:home',
            'pages:our_club',
            'pages:history',
            'pages:timeline',
            'pages:board_members',
            'pages:public_rental',
            'pages:activity_list',
            'schedule',
            'userena_signup',
            'contact_form',
            'userena_signin'
            ]

    def location(self, item):
        return reverse(item)
