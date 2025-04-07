from django import forms
from .models import Listing,AddMore,Detail,Subscription,Rent

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude=['realtor']

        def clean_estateType(self):
            estate_type = self.cleaned_data.get('estateType')
            if estate_type == 'select':
                raise forms.ValidationError("Please select a valid estate type.")
            return estate_type
        def clean_roofType(self):
            estate_type = self.cleaned_data.get('roofType')
            if estate_type == 'select':
                raise forms.ValidationError("Please select a valid estate type.")
            return estate_type
        def clean_constructionType(self):
            estate_type = self.cleaned_data.get('constructionType')
            if estate_type == 'select':
                raise forms.ValidationError("Please select a valid estate type.")
            return estate_type

class AddMoreForm(forms.ModelForm):
    class Meta:
        model = AddMore
        fields = '__all__'

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = '__all__'
        exclude=['listing']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'

class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        
        fields = '__all__'
        exclude=['realtor']



class LocationFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="Name")
    category = forms.CharField(max_length=20, required=False, label="Category")
    state = forms.CharField(max_length=50, required=False, label="State")
    city = forms.CharField(max_length=50, required=False, label="City")
    street = forms.CharField(max_length=200, required=False, label="Street")
    pincode = forms.CharField(max_length=6, required=False, label="Pincode")