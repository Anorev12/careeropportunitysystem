from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification, AuditLog


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
    # Mark all as read when viewed
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