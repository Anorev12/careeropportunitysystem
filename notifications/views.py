from django.shortcuts import render, redirect

def notifications_login(request):
    if request.method == 'POST':
        return redirect('/notifications/')
    return render(request, 'careeropportunitysystem/login.html')

def notifications(request):
    return render(request, 'careeropportunitysystem/notifications.html')