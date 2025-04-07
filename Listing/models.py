from django.db import models
from accounts.models import RealtorUser

from django.utils import timezone




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




class Listing(models.Model):
    realtor = models.ForeignKey(RealtorUser, on_delete=models.CASCADE)

    estateType = models.CharField(max_length=50,choices=ESTATE, default='select')
    constructionType = models.CharField(max_length=50,choices=CONSTRUCTION, default='select')
    roofType = models.CharField(max_length=50,choices=ROOF, default='select')
    constructionDate=models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='listings')  # Primary image

    description = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    pricePerSqft = models.DecimalField(max_digits=10, decimal_places=2)

    # Asddress
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)
    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='listings/extra')

    def __str__(self):
        return f"Image for {self.listing.title}"
    

class Detail(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='detail')
    electricPhase=models.IntegerField(blank=True,null=True)
    electricVolt=models.IntegerField(blank=True,null=True)
    electricAmp=models.IntegerField(blank=True,null=True)
    garageAvailable = models.CharField(max_length=255, blank=True,null=True)
    garageLocation = models.CharField(max_length=255, blank=True,null=True)
    garageCarFits = models.CharField(max_length=255, blank=True,null=True)
    garageDimensionsL = models.CharField(max_length=255, blank=True,null=True)
    garageDimensionsB = models.CharField(max_length=255, blank=True,null=True)
    garageDimensionsH = models.CharField(max_length=255, blank=True,null=True)
    poolAvailable = models.CharField(max_length=255, blank=True,null=True)
    poolDimensiondL = models.CharField(max_length=255, blank=True,null=True)
    poolDimensiondB = models.CharField(max_length=255, blank=True,null=True)
    poolDimensiondH = models.CharField(max_length=255, blank=True,null=True)




class AddMore(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='add_more')
    item = models.CharField(max_length=255)
    description  = models.TextField(blank=True)


class Subscription(models.Model):
    plan= models.CharField(max_length=50)
    date_filled = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.plan

    def save(self, *args, **kwargs):
        # Check if plan is provided (or modified)
        if self.plan and not self.date_filled:
            self.date_filled = timezone.now()  # Set the current time when the email is filled
        super().save(*args, **kwargs)





class Rent(models.Model):
    realtor = models.ForeignKey(RealtorUser, on_delete=models.CASCADE)

    rentType = models.CharField(max_length=50,choices=RENT, default='select')

    addState = models.CharField(max_length=255, blank=True)
    addDistrict = models.CharField(max_length=255, blank=True)
    addArea = models.CharField(max_length=255, blank=True)
    addPin = models.CharField(max_length=6, blank=True)

    image = models.ImageField(upload_to='rent')  # Primary image
    
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




class Location(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
