from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


def sample_user(email='test@tullyapp.com', password='password'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicIngredientApiTests(TestCase):
    """Test the un-authorized user Ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags(self):
        """Test Retriving Ingredients of user without Authentication"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the authorized user Ingredients API"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_ingredients(self):
        """Test Ingredients Get API"""
        Ingredient.objects.create(user=self.user, name='Vegan')
        Ingredient.objects.create(user=self.user, name='Dessert')

        res = self.client.get(INGREDIENT_URL)

        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrive_only_authenticated_user_ingredient(self):
        """Test for fetching Ingredient of only authenticated user"""
        user2 = sample_user('test2@tullyapp.com', 'Test Two')
        Ingredient.objects.create(user=user2, name='Dessert')

        tag = Ingredient.objects.create(user=self.user, name='Vegan')

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_ingredient_success(self):
        """Test to create Ingredient via API"""
        payload = {'name': 'Test Ingredient'}
        res = self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredients_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
