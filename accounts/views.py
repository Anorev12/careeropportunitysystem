from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ──────────────────────────────────────────────────────────────
# Index Page  —  127.0.0.1:8080/
# ──────────────────────────────────────────────────────────────

@login_required(login_url='/login/')
def index(request):
    """Main landing page — requires authentication."""
    return render(request, 'accounts/index.html')


# ──────────────────────────────────────────────────────────────
# Login Page  —  127.0.0.1:8080/login/
# ──────────────────────────────────────────────────────────────

def login_view(request):
    """Authenticate a user and redirect to the index page."""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.status == 'suspended':
                messages.error(request, 'Your account has been suspended. Please contact the administrator.')
            elif user.status == 'inactive':
                messages.error(request, 'Your account is inactive. Please contact the administrator.')
            else:
                login(request, user)
                messages.success(request, f'Welcome back, {user.fullname}!')
                return redirect('index')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'accounts/login.html')


# ──────────────────────────────────────────────────────────────
# Logout
# ──────────────────────────────────────────────────────────────

def logout_view(request):
    """Log the current user out and redirect to the login page."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')