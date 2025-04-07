#views.py
from django.shortcuts import render, redirect
from .forms import NormalUserForm, RealtorUserForm
from django.contrib.auth import login,authenticate,logout
from accounts.models import RealtorUser
from django.contrib import messages
import os

#Home Views
def home_view(request):
    if request.user.is_authenticated:
        if isinstance(request.user, RealtorUser):
            welcome_message = f"Welcome, {request.user.first_name} (Realtor)!"
        else:
            welcome_message = f"Welcome, {request.user.first_name}! (User)"
    else:
        welcome_message = "Welcome to our website!"
    return render(request, 'home.html', {'welcome_message': welcome_message,})

from .utils import send_verification_email

#Register Views For Normal User
def register_normal_user(request):
    if request.method == 'POST':
        form = NormalUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            
            # Save user to generate a primary key before verification
            user.save()

            # Create directory if it doesn’t exist
            user_directory = f'media/client/{user.email}'
            os.makedirs(user_directory, exist_ok=True)

            # Send verification email
            send_verification_email(user, request)

            return redirect('login')
    else:
        form = NormalUserForm()

    return render(request, 'users/register_normal_user.html', {'form': form})

#Register Views For Realtor
def register_realtor_user(request):
    if request.method == 'POST':
        form = RealtorUserForm(request.POST)
        if form.is_valid():
            m = request.POST.get('email')
            if os.path.exists('media/realtor/'+m):

                print("file exist")
            else:
                os.makedirs('media/realtor/'+m)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            try:
                user.save()

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('login')
            except Exception as e:
                messages.error(request, "There was an error creating the realtor user: %s" % e)
        else:
            messages.error(request, "There was an error creating the realtor user.")
    else:
        form = RealtorUserForm()

    return render(request, 'users/register_realtor_user.html', {'form': form})

#Login Views
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'users/login.html')

#Logout Views
def logout_view(request):
    logout(request)
    return redirect('home')


#Profile Views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NormalUserProfileForm, RealtorUserProfileForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AvatarUpdateForm, NormalUserProfileForm, RealtorUserProfileForm

@login_required
def profile_view(request):
    user = request.user
    form_class = RealtorUserProfileForm if isinstance(user, RealtorUser) else NormalUserProfileForm
    avatar_form = AvatarUpdateForm(instance=user)

    if request.method == 'POST':
        if 'avatar' in request.FILES:
            # Handle avatar upload
            sub_dir = 'client' if isinstance(user, NormalUser) else 'realtor'
            avatar_dir = os.path.join(settings.MEDIA_ROOT, sub_dir, user.email, 'avatar')
            avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=user)

            if avatar_form.is_valid():
                # Remove all existing files in the avatar folder
                if os.path.isdir(avatar_dir):  # Check if the directory exists
                    for file_path in os.listdir(avatar_dir):  # Iterate through the files in the directory
                        full_path = os.path.join(avatar_dir, file_path)
                        if os.path.isfile(full_path):
                            print(f"Removing old avatar file: {full_path}")
                            os.remove(full_path)

                # Save the new avatar
                avatar_form.save()
                messages.success(request, "Avatar updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Error updating avatar.")


        else:
            # Handle other profile fields if they are submitted (optional)
            form = form_class(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Error updating profile.")

    # IF GET request, load forms with the user's current data
    profile_form = form_class(instance=user)

    return render(request, 'users/profile.html', {
        'profile_form': profile_form,
        'avatar_form': avatar_form,
    })

#Profile Update View
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import NormalUserProfileForm, RealtorUserProfileForm

@login_required
def update_profile_view(request):
    user = request.user
    form_class = RealtorUserProfileForm if isinstance(user, RealtorUser) else NormalUserProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            # Save the form, but only log out the user if the password was changed
            old_password = form.cleaned_data.get("old_password")
            new_password1 = form.cleaned_data.get("new_password1")
            
            # Check if the password was changed
            password_changed = new_password1 is not None and new_password1 != ""

            if password_changed:
                # Log out the user after password change
                logout(request)
                messages.success(request, "Password updated successfully. Please log in again.")
            else:
                messages.success(request, "Profile updated successfully.")

            form.save()  # Save the changes to the user's profile

            if password_changed:
                return redirect('login')  # Redirect to login page after password change
            return redirect('profile')  # Redirect to profile page (or wherever the user should go after update)

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = form_class(instance=user)

    return render(request, 'users/update_profile.html', {'form': form})


#OTP
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()
from .models import NormalUser, RealtorUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .utils import send_verification_email
from django.contrib import messages
from django.shortcuts import redirect

def email_verification_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()

        # Check if the user is a NormalUser or RealtorUser
        user = None
        if NormalUser.objects.filter(pk=uid).exists():
            user = NormalUser.objects.get(pk=uid)
        elif RealtorUser.objects.filter(pk=uid).exists():
            user = RealtorUser.objects.get(pk=uid)

        # If user is found, verify email
        if user and not user.is_email_verified and user.verification_token == token:
            user.is_email_verified = True
            user.verification_token = None  # Clear token after verification
            user.save()

            update_session_auth_hash(request, user)
            messages.success(request, "Your email has been verified successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Email verification link is invalid or expired.")
            return redirect('profile')
    except (TypeError, ValueError, OverflowError, NormalUser.DoesNotExist, RealtorUser.DoesNotExist):
        messages.error(request, "Invalid verification link.")
        return redirect('profile')
    
@login_required
def request_verification_email(request):
    user = request.user
    if not user.is_email_verified:
        send_verification_email(user, request)  # Pass the request object here
        messages.success(request, "A verification email has been sent to your email address.")
    else:
        messages.info(request, "Your email is already verified.")
    return redirect('profile')


#Password Reset
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib import messages
from .forms import PasswordResetRequestForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from accounts.models import NormalUser, RealtorUser  # Import both models

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                # Try to find the user in NormalUser
                user = NormalUser.objects.get(email=email)
            except NormalUser.DoesNotExist:
                try:
                    # If not found in NormalUser, try RealtorUser
                    user = RealtorUser.objects.get(email=email)
                except RealtorUser.DoesNotExist:
                    messages.error(request, "No user found with this email address.")
                    return redirect('password_reset_request')
                
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))

            # Create the password reset URL
            reset_link = f"http://{get_current_site(request).domain}/password-reset/{uid}/{token}/"

            # Send the email
            email_subject = "Password Reset Request"
            email_message = render_to_string('users/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })

            send_mail(
                email_subject,
                email_message,
                'no-reply@example.com',
                [email],
            )

            messages.success(request, "A password reset link has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request, "Invalid email address.")
    else:
        form = PasswordResetRequestForm()

    return render(request, 'users/password_reset_request.html', {'form': form})


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from .forms import NormalUserProfileForm

User = get_user_model()

def password_reset(request, uidb64, token):
    try:
        # Decode the user ID and retrieve the user object
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)

        # Verify the token
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('login')
                else:
                    messages.error(request, "Passwords do not match.")
            return render(request, 'users/password_reset_form.html', {'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, "The password reset link is invalid or expired.")
            return redirect('password_reset_request')
    except (User.DoesNotExist, ValueError, OverflowError):
        messages.error(request, "The password reset link is invalid.")
        return redirect('password_reset_request')

