from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Interview
from .forms import InterviewForm, InterviewLoginForm, InterviewRegisterForm

INTERVIEW_LOGIN_URL = '/interview/login/'


def interview_login(request):
    if request.user.is_authenticated:
        return redirect('/interview/')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            error = 'Please enter both username and password.'
        else:
            user = authenticate(request, username=username, password=password)
            if user is None:
                error = 'Invalid username or password.'
            else:
                login(request, user)
                return redirect('/interview/')
    return render(request, 'interview/login.html', {'error': error})


def interview_register(request):
    if request.user.is_authenticated:
        return redirect('/interview/')
    form = InterviewRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created. Welcome!')
        return redirect('/interview/')
    return render(request, 'interview/register.html', {'form': form})


def interview_logout(request):
    logout(request)
    return redirect('/interview/login/')


@login_required(login_url=INTERVIEW_LOGIN_URL)
def index(request):
    interviews = Interview.objects.filter(
        created_by=request.user
    ).select_related('applicant__user')
    return render(request, 'interview/index.html', {'interviews': interviews})


@login_required(login_url=INTERVIEW_LOGIN_URL)
def add_interview(request):
    form = InterviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        interview = form.save(commit=False)
        interview.created_by = request.user
        interview.save()
        messages.success(request, 'Interview record added successfully.')
        return redirect('/interview/')
    return render(request, 'interview/addNewInterview.html', {'form': form})


@login_required(login_url=INTERVIEW_LOGIN_URL)
def edit_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk, created_by=request.user)
    form = InterviewForm(request.POST or None, instance=interview)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Interview record updated.')
        return redirect('/interview/')
    return render(request, 'interview/addNewInterview.html', {
        'form':      form,
        'interview': interview,
        'editing':   True,
    })


@login_required(login_url=INTERVIEW_LOGIN_URL)
def delete_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk, created_by=request.user)
    if request.method == 'POST':
        interview.delete()
        messages.success(request, 'Interview record deleted.')
        return redirect('/interview/')
    return render(request, 'interview/confirm_delete.html', {'interview': interview})