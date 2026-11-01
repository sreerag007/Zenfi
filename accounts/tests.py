from django.test import TestCase
from rest_framework.test import APIClient


class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_google_auth_endpoint_exists(self):
        response = self.client.post('/accounts/google_auth/', {})
        self.assertNotEqual(response.status_code, 404)
