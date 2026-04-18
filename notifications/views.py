from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification, AuditLog
from .forms import NotificationForm
from django.contrib.auth import get_user_model

User = get_user_model()

def notifications_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/notifications/')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'notifications/login.html')


def notifications_logout(request):
    logout(request)
    return redirect('/notifications/login/')


@login_required(login_url='/notifications/login/')
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)
    user_notifications.update(is_read=True)
    return render(request, 'notifications/notifications.html', {
        'notifications': user_notifications
    })


@login_required(login_url='/notifications/login/')
def index(request):
    user_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    audit_logs = AuditLog.objects.all()[:10]
    return render(request, 'notifications/index.html', {
        'unread_count': user_notifications,
        'audit_logs': audit_logs
    })


def add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/notifications/')
    else:
        form = NotificationForm()
    return render(request, 'notifications/addNewNotification.html', {'form': form})

def notifications_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'notifications/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'notifications/register.html')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Account created! Please login.')
        return redirect('/notifications/login/')

    return render(request, 'notifications/register.html')