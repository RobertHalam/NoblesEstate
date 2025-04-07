#urls.py
from django.urls import path
from .views import register_normal_user, register_realtor_user
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/normal/', register_normal_user, name='register_normal_user'),
    path('register/realtor/', register_realtor_user, name='register_realtor_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification_view, name='email_verification'),
    path('request-verification-email/', views.request_verification_email, name='request_verification_email'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.password_reset, name='password_reset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)