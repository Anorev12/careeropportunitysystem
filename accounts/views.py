from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='/accounts/login/')   # ← fixed
def index(request):
    """Main landing page — requires authentication."""
    return render(request, 'accounts/index.html')


def login_view(request):
    """Authenticate a user and redirect to the index page."""
    if request.user.is_authenticated:
        return redirect('accounts_index')       # ← fixed

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
                return redirect('accounts_index')   # ← fixed
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """Log the current user out and redirect to the login page."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')