from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testfarmer', password='password123', role='FARMER')
        self.assertEqual(user.role, 'FARMER')
        self.assertTrue(user.check_password('password123'))

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_login_view(self):
        User.objects.create_user(username='testfarmer', password='password123', role='FARMER')
        response = self.client.post(reverse('login'), {'username': 'testfarmer', 'password': 'password123'})
        self.assertRedirects(response, reverse('dashboard'))
