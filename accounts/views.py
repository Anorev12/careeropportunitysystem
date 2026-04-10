from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Applicant, Administrator
from .forms import LoginForm, RegisterForm, UserProfileForm, ApplicantProfileForm


# ─────────────────────────────────────────────
# INDEX / HOME  (127.0.0.1:8080/)
# ─────────────────────────────────────────────
def index(request):
    """Public landing page for Career Opportunity System."""
    return render(request, 'accounts/index.html')


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
def login_view(request):
    """Login page at /accounts/login/"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.status == 'suspended':
            messages.error(request, 'Your account has been suspended.')
        else:
            login(request, user)
            messages.success(request, f'Welcome back, {user.fullname}!')
            return redirect('accounts:dashboard')

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Registration page at /accounts/register/"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # Auto-create profile record based on role
        if user.role == 'applicant':
            Applicant.objects.create(user=user)
        elif user.role == 'admin':
            Administrator.objects.create(
                user=user,
                employee_number=f'EMP-{user.id:05d}'
            )
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


# ─────────────────────────────────────────────
# DASHBOARD  (role-aware)
# ─────────────────────────────────────────────
@login_required
def dashboard(request):
    context = {'user': request.user}

    if request.user.role == 'admin':
        context['total_users']      = User.objects.count()
        context['total_applicants'] = Applicant.objects.count()
        context['total_admins']     = Administrator.objects.count()
        context['recent_users']     = User.objects.order_by('-date_joined')[:5]

    return render(request, 'accounts/dashboard.html', context)


# ─────────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────────
@login_required
def profile_view(request):
    user_form  = UserProfileForm(request.POST or None, instance=request.user)
    applicant_form = None

    if hasattr(request.user, 'applicant_profile'):
        applicant_form = ApplicantProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=request.user.applicant_profile
        )

    if request.method == 'POST':
        forms_valid = user_form.is_valid()
        if applicant_form:
            forms_valid = forms_valid and applicant_form.is_valid()

        if forms_valid:
            user_form.save()
            if applicant_form:
                applicant_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'applicant_form': applicant_form,
    })


# ─────────────────────────────────────────────
# ADMIN: User Management
# ─────────────────────────────────────────────
@login_required
def user_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')

    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def user_detail(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')

    target = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_detail.html', {'target': target})