from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, SimpleTestCase

from .admin import NewsletterAdmin
from .models import Newsletter


class NewsletterAdminTests(SimpleTestCase):
    def setUp(self):
        self.admin = NewsletterAdmin(Newsletter, AdminSite())
        self.request = RequestFactory().get('/admin/newsletter/newsletter/3/change/')

    def test_protected_newsletter_slug_is_readonly_without_prepopulation(self):
        newsletter = Newsletter(slug='general-newsletter')

        form_class = self.admin.get_form(self.request, newsletter)

        self.assertNotIn('slug', form_class.base_fields)
        self.assertEqual(
            self.admin.get_prepopulated_fields(self.request, newsletter),
            {},
        )

    def test_unprotected_newsletter_slug_is_prepopulated(self):
        newsletter = Newsletter(slug='neighborhood-news')

        self.assertEqual(
            self.admin.get_prepopulated_fields(self.request, newsletter),
            {'slug': ('title',)},
        )
