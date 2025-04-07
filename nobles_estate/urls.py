
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Welcome to PayPal Subscription System</h1>")




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('listing/', include('Listing.urls')),
    path('subscriptions/', include('subscriptions.urls')),
]


