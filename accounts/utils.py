#utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import uuid

def send_verification_email(user, request):
    token = str(uuid.uuid4())
    user.verification_token = token
    user.save()  # Save the token to the user

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = reverse('email_verification', kwargs={'uidb64': uid, 'token': token})
    full_url = request.build_absolute_uri(verification_url)

    subject = "Verify your email"
    message = f"Please click the link below to verify your email address:\n{full_url}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])