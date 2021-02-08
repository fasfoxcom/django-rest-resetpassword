from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase


class BaseAPITest(APITestCase):
    def setUp(self, password=None) -> None:
        User = get_user_model()
        self.user = User(username="John Smith", email="john@example.com")
        self.user.set_password("123")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def user_factory(self, username="peter", email="peter@example.com", password="123"):
        User = get_user_model()
        user = User(username=username, email=email, password=password)
        user.save()
        return user


class ResetPasswordAPITest(BaseAPITest):
    def test_request_reset_password_with_valid_email_or_password(self):
        self.user_factory()

        # Check if input field can be either an email or a username
        settings.DJANGO_REST_LOOKUP_FIELDS = ["email", "username"]
        data = {
            "email_or_username": self.user.username,
        }
        response = self.client.post(reverse("reset-password-request"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["status"])
        self.assertEqual(len(response.data["error"]), 0)
        msg = "A password reset token has been sent to the provided email address"
        self.assertEqual(response.data["message"], msg)
        self.assertEqual(response.data["data"][0], self.user.email)

        # Check if input field can be either an email or a username
        data = {
            "email_or_username": self.user.email,
        }
        response = self.client.post(reverse("reset-password-request"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["status"])
        self.assertEqual(len(response.data["error"]), 0)
        msg = "A password reset token has been sent to the provided email address"
        self.assertEqual(response.data["message"], msg)
        self.assertEqual(response.data["data"][0], self.user.email)

    def test_request_reset_password_with_valid_email(self):
        self.user_factory()

        settings.DJANGO_REST_LOOKUP_FIELDS = ["email"]
        data = {
            "email_or_username": self.user.username,
        }
        # Check that if the look-up field is email
        # we can't filter by username.
        response = self.client.post(reverse("reset-password-request"), data)
        self.assertEqual(response.status_code, 400)

        data = {
            "email_or_username": self.user.email,
        }
        response = self.client.post(reverse("reset-password-request"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["status"])
        self.assertEqual(len(response.data["error"]), 0)
        msg = "A password reset token has been sent to the provided email address"
        self.assertEqual(response.data["message"], msg)
        self.assertEqual(response.data["data"][0], self.user.email)

    def test_request_reset_password_with_no_params(self):
        data = {}
        response = self.client.post(reverse("reset-password-request"), data)
        self.assertEqual(response.status_code, 400)
