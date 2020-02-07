from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        email = "testmanagement@tullyapp.com"
        password = "password"
        self.admin_user = get_user_model().objects.create_super_user(
            email=email,
            password=password
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='testmanagement2@tullyapp.com',
            password=password,
            name="Kathan Shah"
        )

    def test_users_listed(self):
        """Test that users are listed on users page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

