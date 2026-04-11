from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import LoginForm, RegisterForm
from accounts.models import Applicant
from .models import Application, Interview
from .forms import ApplicationForm, ApplicationStatusForm, InterviewForm
from employer.models import JobPosting


def get_applicant(request):
    try:
        return request.user.applicant_profile
    except AttributeError:
        return None


def application_login_view(request):
    if request.user.is_authenticated:
        return redirect('application:application_list')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.status == 'suspended':
            messages.error(request, 'Your account has been suspended.')
        else:
            login(request, user)
            messages.success(request, f'Welcome back, {user.fullname}!')
            return redirect('application:application_list')

    return render(request, 'application/login.html', {
        'form':     form,
        'reg_form': RegisterForm(),
    })


def application_register_view(request):
    if request.user.is_authenticated:
        return redirect('application:application_list')

    reg_form = RegisterForm(request.POST or None)
    if request.method == 'POST' and reg_form.is_valid():
        user = reg_form.save()
        if user.role == 'applicant':
            Applicant.objects.create(user=user)
        login(request, user)
        messages.success(request, 'Account created! Welcome to the Applications Portal.')
        return redirect('application:application_list')

    return render(request, 'application/login.html', {
        'form':     LoginForm(request),
        'reg_form': reg_form,
    })


def application_logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('application:application_login')


@login_required(login_url='/application/login/')
def application_list(request):
    applicant = get_applicant(request)
    if applicant:
        applications = Application.objects.filter(applicant=applicant).select_related(
            'job_posting', 'job_posting__employer', 'job_posting__job_title'
        )
    else:
        applications = Application.objects.all().select_related(
            'applicant__user', 'job_posting', 'job_posting__employer'
        )
    return render(request, 'application/application_list.html', {'applications': applications})


@login_required(login_url='/application/login/')
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, pk=job_id)
    applicant = get_applicant(request)

    if not applicant:
        messages.error(request, "Only applicants can apply for jobs.")
        return redirect('application:application_list')

    if Application.objects.filter(applicant=applicant, job_posting=job).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('application:application_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.applicant   = applicant
            app.job_posting = job
            app.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('application:application_list')
    else:
        form = ApplicationForm(initial={'job_posting': job})

    return render(request, 'application/apply_job.html', {'form': form, 'job': job})


@login_required(login_url='/application/login/')
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    interviews  = application.interviews.all()
    return render(request, 'application/application_detail.html', {
        'application': application,
        'interviews':  interviews,
    })


@login_required(login_url='/application/login/')
def withdraw_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    applicant   = get_applicant(request)

    if not applicant or application.applicant != applicant:
        messages.error(request, "Permission denied.")
        return redirect('application:application_list')

    if application.status not in ('accepted', 'rejected'):
        application.status = 'withdrawn'
        application.save()
        messages.success(request, "Application withdrawn.")
    else:
        messages.warning(request, "Cannot withdraw a finalised application.")

    return redirect('application:application_list')


@login_required(login_url='/application/login/')
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application status updated.")
            return redirect('application:application_detail', pk=pk)
    else:
        form = ApplicationStatusForm(instance=application)

    return render(request, 'application/update_status.html', {
        'form':        form,
        'application': application,
    })


@login_required(login_url='/application/login/')
def schedule_interview(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)

    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            messages.success(request, "Interview scheduled.")
            return redirect('application:application_detail', pk=application_pk)
    else:
        form = InterviewForm()

    return render(request, 'application/schedule_interview.html', {
        'form':        form,
        'application': application,
    })


@login_required(login_url='/application/login/')
def edit_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk)

    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview updated.")
            return redirect('application:application_detail', pk=interview.application.pk)
    else:
        form = InterviewForm(instance=interview)

    return render(request, 'application/schedule_interview.html', {
        'form':        form,
        'application': interview.application,
        'edit_mode':   True,
    })


@login_required(login_url='/application/login/')
def delete_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    app_pk    = interview.application.pk
    interview.delete()
    messages.success(request, "Interview deleted.")
    return redirect('application:application_detail', pk=app_pk)