#models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import os

# Define the custom manager above the custom user models
class NormalUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)
    


def avatar_upload_path(instance, filename):
    # Different path for each user type
    sub_dir = 'client' if isinstance(instance, NormalUser) else 'realtor'
    return f'{sub_dir}/{instance.email}/avatar/{filename}'



class NormalUser(AbstractUser):
    username = None  # Remove the username field entirely
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, default='default_avatar.jpg', blank=True)
    groups = models.ManyToManyField('auth.Group', related_name='normal_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='normal_user_permissions')
    is_email_verified = models.BooleanField(default=False) 
    verification_token = models.CharField(max_length=100, blank=True, null=True)

    # Use custom manager
    objects = NormalUserManager()

    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields required for registration

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class RealtorUser(AbstractUser):
    username = None  # Remove the username field entirely
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, default='default_avatar.jpg', blank=True)
    phone_number = models.CharField(max_length=20)
    groups = models.ManyToManyField('auth.Group', related_name='realtor_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='realtor_user_permissions')
    is_email_verified = models.BooleanField(default=False)  # New field
    verification_token = models.CharField(max_length=100, blank=True, null=True)

    # Use custom manager
    objects = NormalUserManager()

    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']  # Fields required for registration

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Realtor'
        verbose_name_plural = 'Realtors'
