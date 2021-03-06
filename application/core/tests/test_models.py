from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@tullyapp.com', password='password'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)


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
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertTrue(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the Ingredient creation and String value"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Chataka"
        )
        self.assertTrue(str(ingredient), ingredient.name)
