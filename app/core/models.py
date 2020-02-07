from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """docstring for UserManager."""
    def __init__(self, arg):
        super(UserManager, self).__init__()
        self.arg = arg

    def create_user(self, email, password=None, **extraFields):
        """Creates and Saves a new User"""
        user = self.model(email=email, **extraFields)
        user.set_password(password)
        user.save(using=self._db)

        return user

# Create your models here.
