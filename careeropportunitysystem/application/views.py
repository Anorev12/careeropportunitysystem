from django.shortcuts import render, get_object_or_404, redirect
from .models import Application
from .forms import ApplicationForm

def application_list(request):
    applications = Application.objects.all()
    return render(request, 'application/application_list.html', {'applications': applications})

def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'application/application_detail.html', {'application': application})

def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_list')
    else:
        form = ApplicationForm()
    return render(request, 'application/application_form.html', {'form': form})

def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_list')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'application/application_form.html', {'form': form})

def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        application.delete()
        return redirect('application_list')
    return render(request, 'application/application_confirm_delete.html', {'application': application})