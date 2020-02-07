from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test Creating a new user with email address is successful"""
        email = "testmanagement@tullyapp.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the new email for user is normalized"""
        email = "testmanagement@TULLYAPP.COM"
        password = "password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_new_super_user_is_created(self):
        """Test Creating a new Super User"""
        email = "testmanagement@tullyapp.com"
        password = "password"
        user = get_user_model().objects.create_super_user(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)