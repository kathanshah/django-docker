from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """docstring for UserManager."""

    def create_user(self, email, password=None, **extraFields):
        """Creates and Saves a new User"""
        if not email:
            raise ValueError('Email is required for user creation')
        user = self.model(email=self.normalize_email(email), **extraFields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, email, password=None):
        """Creates new Super User"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User which accepts without username field"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
