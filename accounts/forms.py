#froms.py
from django import forms
from .models import NormalUser, RealtorUser

class NormalUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = NormalUser
        fields = ('first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if email already exists in RealtorUser
        if RealtorUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered as a realtor.")
        
        return email

    def save(self, commit=True):
        # Override save to hash the password correctly
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user


class RealtorUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = RealtorUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if email already exists in NormalUser
        if NormalUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered as a user.")
        
        return email

    def save(self, commit=True):
        # Override save to hash the password correctly
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user

    

#User Update 
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import NormalUser, RealtorUser

class NormalUserProfileForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput, required=False, label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, required=False, label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, required=False, label="Confirm New Password"
    )


    class Meta:
        model = NormalUser
        fields = ('first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # If new passwords are provided, validate them
        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise ValidationError("New passwords do not match.")
            password_validation.validate_password(new_password1, self.instance)

        # If old password is provided, check if it is correct
        if old_password and not self.instance.check_password(old_password):
            self.add_error('old_password', 'Old password is incorrect.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class RealtorUserProfileForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput, required=False, label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, required=False, label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, required=False, label="Confirm New Password"
    )

    class Meta:
        model = RealtorUser
        fields = ('first_name', 'last_name','phone_number')

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # If new passwords are provided, validate them
        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise ValidationError("New passwords do not match.")
            password_validation.validate_password(new_password1, self.instance)

        # If old password is provided, check if it is correct
        if old_password and not self.instance.check_password(old_password):
            self.add_error('old_password', 'Old password is incorrect.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
    
class AvatarUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, label="Upload New Avatar")

    class Meta:
        model = NormalUser  # This will work for both user types
        fields = ('avatar',)


#Password Reset
from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email", max_length=254)