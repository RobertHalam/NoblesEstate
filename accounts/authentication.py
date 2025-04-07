#authentication.py
from django.contrib.auth.backends import ModelBackend
from .models import NormalUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = NormalUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except NormalUser.DoesNotExist:
            return None
        
from django.contrib.auth.backends import BaseBackend
from .models import RealtorUser

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            # Find the user by email
            user = RealtorUser.objects.get(email=email)
            if user.check_password(password):  # Verify password
                return user
        except RealtorUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return RealtorUser.objects.get(id=user_id)
        except RealtorUser.DoesNotExist:
            return None