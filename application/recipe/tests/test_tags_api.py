from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def sample_user(email='test@tullyapp.com', password='password'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicTagsApiTests(TestCase):
    """Test the un-authorized user tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags(self):
        """Test Retriving Tags of user without Authentication"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """Test Tags Get API"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrive_only_authenticated_user_tag(self):
        """Test for fetching tags of only authenticated user"""
        user2 = sample_user('test2@tullyapp.com', 'Test Two')
        Tag.objects.create(user=user2, name='Dessert')

        tag = Tag.objects.create(user=self.user, name='Vegan')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_success(self):
        """Test to create Tag via API"""
        payload = {'name': 'Test Tag'}
        res = self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
