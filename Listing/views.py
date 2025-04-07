from django.shortcuts import render, redirect
from .forms import ListingForm,AddMoreForm,DetailForm,RentForm,LocationFilterForm
from django.contrib.auth.decorators import login_required
from accounts.models import RealtorUser
from django.contrib import messages
from .models import Listing, ListingImage, AddMore,Detail,Rent,Location
from django.shortcuts import get_object_or_404

import django_filters
# User Dashboard (for both Realtors and Normal Users)
# @login_required
# def listings_page(request):
#     # Get all listings for browsing
#     listings = Listing.objects.all()

#     return render(request, 'listings_page.html', {'listings': listings})



ESTATE=(
    ('select','Select'),
    ('house','House'),
    ('building', 'Building'),
    ('land', 'Land'),
)

RENT=(
    ('select','Select'),
    ('shop','Shop'),
    ('building', 'Building'),
)

ROOF=(
    ('select','Select'),
    ('tin','Tin'),
    ('cement', 'Cement'),
)
CONSTRUCTION=(
    ('select','Select'),
    ('cement','Cement'),
    ('wood', 'Wood'),
)








@login_required
def listings_page(request):
    # Start with all listings
    listings = Listing.objects.all()
    rents = Rent.objects.all().order_by('price')

    # Filter by estateType (if provided in request)
    estate_type = request.GET.get('estateType')
    if estate_type and estate_type != 'select':
        listings = listings.filter(estateType=estate_type)

    # Filter by constructionType (if provided in request)
    construction_type = request.GET.get('constructionType')
    if construction_type and construction_type != 'select':
        listings = listings.filter(constructionType=construction_type)

    # Filter by roofType (if provided in request)
    roof_type = request.GET.get('roofType')
    if roof_type and roof_type != 'select':
        listings = listings.filter(roofType=roof_type)

    # Filter by price range (if provided in request)
    sort_by = request.GET.get('sort_by', 'price_asc')  # Default to 'price_asc'

    if sort_by == 'price_desc':
        listings = listings.order_by('-price')
    elif sort_by == 'price_asc':
        listings = listings.order_by('price')
    elif sort_by == 'estateType_asc':
        listings = listings.order_by('estateType')  # Ascending order by estateType
    elif sort_by == 'estateType_desc':
        listings = listings.order_by('-estateType')  # Descending order by estateType


    # Filter by created_at (if provided in request)
    created_after = request.GET.get('created_after')
    if created_after:
        listings = listings.filter(created_at__gte=created_after)

    return render(request, 'listings_page.html', {'listings': listings,'rents':rents})




from django.shortcuts import render, get_object_or_404
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    details = listing.detail.first()

    return render(request, 'listing_detail.html', {'listing': listing,'details':details})

# Realtor Dashboard
@login_required
def realtor_dashboard(request):
    if not isinstance(request.user, RealtorUser):
        messages.error(request, "Access denied. Only Realtors can access this page.")
        return redirect('home')  # Redirect to home if not a Realtor


    listings = request.user.listing_set.all()

    return render(request, 'realtor_dashboard.html', {'listings': listings})



@login_required
def edit_listing(request, pk):
    if not isinstance(request.user, RealtorUser):
        messages.error(request, "Access denied. Only Realtors can edit listings.")
        return redirect('home')

    listing = get_object_or_404(Listing, pk=pk, realtor=request.user)
    detail=listing.detail.first()# Assuming a one-to-one relationship with Listing

    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        detail_form = DetailForm(request.POST, request.FILES, instance=detail)
        # form2 = DetailForm(request.POST, request.FILES, instance=listing)
        # if form2.is_valid():
        #      form2.save()
        if form.is_valid() and detail_form.is_valid():
            form.save()
            detail_form.save()

            # Handle additional images: adding new images
            if 'images' in request.FILES:
                additional_images = request.FILES.getlist('images')
                for img in additional_images:
                    if img != listing.image:
                        ListingImage.objects.create(listing=listing, image=img)

            # Handle image deletion (defer deletion to form submission)
            images_to_delete = request.POST.get('delete_images', "")
            if images_to_delete:
                image_ids = [int(image_id) for image_id in images_to_delete.split(",") if image_id.isdigit()]
                ListingImage.objects.filter(id__in=image_ids, listing=listing).delete()



            

            
            



                        # Handle AddMore items (adding, updating, or deleting)
            if 'add_more_items' in request.POST:
                # Process adding or updating AddMore items
                for item_id, item_data in request.POST.items():
                    if item_id.startswith('add_more_item_'):
                        add_more_id = item_id.replace('add_more_item_', '')
                        if add_more_id:
                            add_more_item = AddMore.objects.get(id=add_more_id)
                            add_more_item.item = item_data.get('item')
                            add_more_item.description = item_data.get('description')
                            add_more_item.save()
                        else:
                            # Create a new AddMore item
                            AddMore.objects.create(listing=listing, item=item_data.get('item'), description=item_data.get('description'))

            # Handle deletion of AddMore items
            if 'delete_add_more' in request.POST:
                add_more_ids_to_delete = request.POST.getlist('delete_add_more')
                AddMore.objects.filter(id__in=[int(id) for id in add_more_ids_to_delete]).delete()












            messages.success(request, "Listing updated successfully.")
            return redirect('realtor_dashboard')  
    else:
        form = ListingForm(instance=listing)
        detail_form = DetailForm(instance=detail)

    # Pass additional images to the template for display and deletion
    additional_images = listing.additional_images.all()

        # Fetch all AddMore items related to the listing
    add_more_items = AddMore.objects.filter(listing=listing)










    return render(request, 'edit_listing.html', {
        'form': form,
        'detail_form': detail_form,
        'listing': listing,
        'additional_images': additional_images,
        'add_more_items': add_more_items
    })

@login_required
def delete_listing(request, pk):
    if not isinstance(request.user, RealtorUser):
        messages.error(request, "Access denied. Only Realtors can delete listings.")
        return redirect('home')

    listing = get_object_or_404(Listing, pk=pk, realtor=request.user)
    
    if request.method == 'POST':
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect('realtor_dashboard')

    return render(request, 'delete_listing.html', {'listing': listing})

#Deleting images in the edit view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ListingImage
import json


@csrf_exempt
@login_required
def delete_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')

            image = ListingImage.objects.get(id=image_id, listing__realtor=request.user)
            image.delete()

            return JsonResponse({'success': True})
        except ListingImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found or unauthorized.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})





#Create Listing

@login_required
def create_listing(request):
    if not isinstance(request.user, RealtorUser):
        messages.error(request, "Access denied. Only Realtors can create listings.")
        return redirect('home')
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        form2 = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the Listing instance without saving
            listing = form.save(commit=False)
            listing.realtor = request.user
            listing.image = request.FILES.get('image')  # Use the first image as primary
            listing.save()

            # Process additional images
            if 'images' in request.FILES:
                additional_images = request.FILES.getlist('images')
                for img in additional_images:
                    if img != listing.image:  # Skip the primary image
                        ListingImage.objects.create(listing=listing, image=img)
            
            
            # Detail foem
            
            if form2.is_valid():
                detail = form2.save(commit=False)  # Create Detail instance but don't save yet
                detail.listing = listing  # Associate with the listing
                detail.save()


             # Process "Add More" items (extra items or descriptions)
            add_more_items = request.POST.getlist('add_more_items')
            add_more_descriptions = request.POST.getlist('add_more_descriptions')
            for item, description in zip(add_more_items, add_more_descriptions):
                if item:
                    AddMore.objects.create(listing=listing, item=item, description=description)

            messages.success(request, "Listing created successfully.")
            return redirect('realtor_dashboard')
    else:
        form = ListingForm()
        form2=DetailForm()

    return render(request, 'create_listing.html', {'form': form,'form2':form2})




def aboutus(request):


    return render(request, 'aboutus.html')


def contactus(request):


    return render(request, 'contactus.html')


def homel(request):
    if request.user.is_authenticated:
        if isinstance(request.user, RealtorUser):
            welcome_message = f"Welcome, {request.user.first_name} (Realtor)!"
        else:
            welcome_message = f"Welcome, {request.user.first_name}! (User)"
    else:
        welcome_message = "Welcome to our website!"
    return render(request, 'homel.html', {'welcome_message': welcome_message,})



@login_required
def create_rent(request):
    if not isinstance(request.user, RealtorUser):
        messages.error(request, "Access denied. Only Realtors can create listings.")
        return redirect('home')
    
    if request.method == 'POST':
        form = RentForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Create the Listing instance without saving
            rent = form.save(commit=False)
            rent.realtor = request.user
            rent.image = request.FILES.get('image') 
            rent.save()

           

            messages.success(request, "Listing created successfully.")
            return redirect('realtor_dashboard')
    else:
        form = RentForm()

    return render(request, 'create_rent.html', {'form': form})





def location_list(request):
    form = LocationFilterForm(request.GET or None)
    locations = Location.objects.all()

    if form.is_valid():
        if form.cleaned_data['name']:
            locations = locations.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['category']:
            locations = locations.filter(category__icontains=form.cleaned_data['category'])
        if form.cleaned_data['state']:
            locations = locations.filter(state__icontains=form.cleaned_data['state'])
        if form.cleaned_data['city']:
            locations = locations.filter(city__icontains=form.cleaned_data['city'])
        if form.cleaned_data['street']:
            locations = locations.filter(street__icontains=form.cleaned_data['street'])
        if form.cleaned_data['pincode']:
            locations = locations.filter(pincode__icontains=form.cleaned_data['pincode'])

    context = {
        'form': form,
        'locations': list(locations.values('name', 'category', 'state', 'city', 'street', 'pincode', 'latitude', 'longitude')),
    }
    return render(request, 'locations/location_list.html', context)