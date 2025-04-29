from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from orders.models import Order
from .forms import UserProfileForm, CustomUserCreationForm
from .models import User  # Import the custom User model from local models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta

# Add the custom logout view
def logout_view(request):
    """Custom logout view that adds a success message and redirects to home"""
    # Only log out if the user is authenticated
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully')
    return redirect('core:home')

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'orders': orders
    }
    return render(request, 'account/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'account/profile_edit.html', {'form': form})

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'account/orders.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        email = request.POST.get('email')
        
        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already in use.')
            return render(request, 'account/register.html', {'form': form})
        
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.is_active = False  # User needs to verify email
            user.save()
            
            # Send verification email
            subject = 'Welcome to Grocefy - Verify Your Email'
            html_message = render_to_string('account/email/verify_email.html', {
                'user': user,
                'verification_url': request.build_absolute_uri(
                    f'/accounts/verify-email/{user.id}/'
                )
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'account/register.html', {'form': form})

def verify_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Check if the verification link is expired (24 hours)
    if not user.is_active and user.date_joined < timezone.now() - timedelta(hours=24):
        messages.error(request, 'The verification link has expired. Please register again.')
        return redirect('accounts:register')
    
    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified successfully. You can now log in.')
        return redirect('accounts:login')
    else:
        messages.info(request, 'Your email is already verified. You can log in.')
        return redirect('accounts:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')  # This gets the value from the checkbox
        
        # Debug message to see if remember_me is being received
        print(f"Remember me checkbox value: {remember_me}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Handle "Remember Me" checkbox
                if remember_me:
                    # If checkbox is checked, session will persist for 2 weeks
                    request.session.set_expiry(1209600)  # 2 weeks in seconds
                else:
                    # If checkbox is not checked, session will expire when browser closes
                    request.session.set_expiry(0)
                
                login(request, user)
                
                # Save a flag indicating if the user chose to be remembered
                if remember_me:
                    request.session['remember_me'] = True
                
                # Redirect all users to the home page, including staff/admin users
                # This allows admin users to see the Dashboard button in the header
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('core:home')
            else:
                messages.error(request, 'Your account is not active. Please check your email for verification link.')
        else:
            messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'account/login.html')
