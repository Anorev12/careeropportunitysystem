from django.shortcuts import render

def notifications(request):
    return render(request, 'careeropportunitysystem/notifications.html')