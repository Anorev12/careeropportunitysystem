from django.shortcuts import render, redirect

def notifications_login(request):
    if request.method == 'POST':
        return redirect('/notifications/')
    return render(request, 'notifications/login.html')

def notifications(request):
    return render(request, 'notifications/notifications.html')