from django.contrib import admin
from .models import Listing, ListingImage,AddMore,Detail,Subscription,Rent,Location

class ListingImageInline(admin.TabularInline):
    """
    Inline model for displaying and managing additional images
    for a listing directly within the listing admin page.
    """
    model = ListingImage
    extra = 1  # Number of empty slots for adding images
    fields = ('image',)
    max_num = 10  # Maximum number of additional images allowed

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Listing model.
    """
    list_display = ('title', 'realtor', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'realtor__username')
    list_filter = ('created_at', 'updated_at', 'price')
    inlines = [ListingImageInline]  # Embed the additional images in the listing admin

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ListingImage model.
    """
    list_display = ('listing', 'image')
    search_fields = ('listing__title',)


admin.site.register(AddMore)
admin.site.register(Detail)
admin.site.register(Subscription)
admin.site.register(Rent)
admin.site.register(Location)