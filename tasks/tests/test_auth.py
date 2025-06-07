"""
Quick test script to verify authentication is working.
Run using: python manage.py test tasks.tests.test_auth
"""
import base64
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_username = 'testuser'
        self.test_email = 'test@example.com'
        self.test_password = 'testpass123'

    def test_registration_and_login(self):
        # Test registration
        registration_data = {
            'username': self.test_username,
            'email': self.test_email,
            'password': self.test_password
        }
        registration_response = self.client.post(
            reverse('register'), registration_data, content_type='application/json'
        )
        self.assertEqual(registration_response.status_code, 201)
        self.assertIn('password', registration_response.json())

        # Test login
        login_data = {
            'username': self.test_username,
            'password': self.test_password
        }
        login_response = self.client.post(
            reverse('login'), login_data, content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn('password', login_response.json())

        # Test authentication with Basic Auth
        credentials = base64.b64encode(
            f"{self.test_username}:{self.test_password}".encode()
        ).decode()
        
        # Try accessing protected endpoint
        tasks_response = self.client.get(
            reverse('task-list'),
            HTTP_AUTHORIZATION=f'Basic {credentials}'
        )
        self.assertEqual(tasks_response.status_code, 200)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'tasks.tests.test_auth'])
