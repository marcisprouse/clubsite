from django.test import SimpleTestCase
from django.urls import reverse

from pages.models import Feature


class FeatureModelTests(SimpleTestCase):
    def test_get_absolute_url_uses_registered_feature_detail_route(self):
        feature = Feature(id=98, title="Test Feature", slug="test-feature")

        self.assertEqual(
            feature.get_absolute_url(),
            reverse("pages:feature_details", args=[98]),
        )
