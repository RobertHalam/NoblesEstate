from django.urls import path
from subscriptions import views
from django.http import HttpResponse
from django.shortcuts import redirect

def subscriptions_home(request):
    return HttpResponse("<h1>Welcome to the Subscriptions Page</h1>")

urlpatterns = [
    path('subscribe/<str:plan_name>/', views.create_subscription, name='create_subscription'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', lambda request: redirect('dashboard/')),  # Redirect to the dashboard

    path('myview/', views.myview, name='myview'),
]
