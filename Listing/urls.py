from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import listing_detail
from .views import delete_image

urlpatterns = [
    path('listings/', views.listings_page, name='listings'),
    path('create-listing/', views.create_listing, name='create_listing'),  # For creating listings
    path('realtor-dashboard/', views.realtor_dashboard, name='realtor_dashboard'),  # Realtor dashboard
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),  # Detail page for listings
    path('listing/edit/<int:pk>/', views.edit_listing, name='edit_listing'),  # Edit listing
    path('listing/delete/<int:pk>/', views.delete_listing, name='delete_listing'),  # Delete listing
    path('listing/image/delete/', delete_image, name='delete_image'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.contactus, name='contactus'),
    path('', views.homel, name='homel'),
    path('create-rent/', views.create_rent, name='create_rent'),  # For creating rent
    path('location', views.location_list, name='location_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 