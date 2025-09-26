from django.test import TestCase
from django.urls import reverse

from core.settings import API_VERSION

from task.models import Task
from authentication.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class TaskTests(APITestCase):

    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/api/{API_VERSION}/task')
        self.assertEqual(response.status_code, 200)

    def test_view_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(f'/api/{API_VERSION}/task')
        self.assertEqual(response.status_code, 401)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)

    