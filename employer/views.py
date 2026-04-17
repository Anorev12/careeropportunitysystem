from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPosting, JobCategory, JobTitle, Employer
from .forms import JobPostingForm, EmployerRegisterForm


# ── Helper ──
def get_employer(request):
    try:
        return Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        return None


# ── Register ──
def register_view(request):
    form = EmployerRegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.role = 'employer'
            user.status = 'active'
            user.save()

            Employer.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                company_description=form.cleaned_data['company_description'],
                company_address=form.cleaned_data['company_address'],
                contact_email=form.cleaned_data['contact_email'],
                contact_number=form.cleaned_data['contact_number'],
            )
            messages.success(request, 'Account created! Please log in.')
            return redirect('employer:login')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'employer/register.html', {'form': form})


# ── Login ──
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employer:employer_index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'employer/login.html')


# ── Logout ──
def logout_view(request):
    logout(request)
    return redirect('employer:login')


# ── Dashboard ──
@login_required(login_url='/employer/login/')
def employer_index(request):
    employer = get_employer(request)
    if not employer:
        messages.warning(request, "No employer profile found.")
        job_postings = []
    else:
        job_postings = JobPosting.objects.filter(employer=employer)
    return render(request, 'employer/index.html', {
        'job_postings': job_postings,
        'employer': employer,
    })


# ── Post a Job ──
@login_required(login_url='/employer/login/')
def create_job(request):
    employer = get_employer(request)
    if not employer:
        messages.error(request, "No employer profile found.")
        return redirect('employer:employer_index')

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            category, _ = JobCategory.objects.get_or_create(
                name=form.cleaned_data['category']
            )
            job_title, _ = JobTitle.objects.get_or_create(
                title=form.cleaned_data['job_title'],
                defaults={'category': category}
            )
            JobPosting.objects.create(
                employer=employer,
                job_title=job_title,
                category=category,
                description=form.cleaned_data['description'],
                requirements=form.cleaned_data['requirements'],
                location=form.cleaned_data['location'],
                salary_min=form.cleaned_data['salary_min'],
                salary_max=form.cleaned_data['salary_max'],
                job_type=form.cleaned_data['job_type'],
                status=form.cleaned_data['status'],
                deadline=form.cleaned_data['deadline'],
            )
            messages.success(request, "Job posted successfully!")
            return redirect('employer:employer_index')
    else:
        form = JobPostingForm()
    return render(request, 'employer/edit.html', {'form': form, 'title': 'Post New Job'})


# ── Edit a Job ──
@login_required(login_url='/employer/login/')
def edit_job(request, id):
    job = get_object_or_404(JobPosting, id=id)
    employer = get_employer(request)

    if not employer or job.employer != employer:
        messages.error(request, "Permission denied.")
        return redirect('employer:employer_index')

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            category, _ = JobCategory.objects.get_or_create(
                name=form.cleaned_data['category']
            )
            job_title, _ = JobTitle.objects.get_or_create(
                title=form.cleaned_data['job_title'],
                defaults={'category': category}
            )
            job.job_title = job_title
            job.category = category
            job.description = form.cleaned_data['description']
            job.requirements = form.cleaned_data['requirements']
            job.location = form.cleaned_data['location']
            job.salary_min = form.cleaned_data['salary_min']
            job.salary_max = form.cleaned_data['salary_max']
            job.job_type = form.cleaned_data['job_type']
            job.status = form.cleaned_data['status']
            job.deadline = form.cleaned_data['deadline']
            job.save()
            messages.success(request, "Job updated!")
            return redirect('employer:employer_index')
    else:
        form = JobPostingForm(initial={
            'job_title': job.job_title.title,
            'category': job.category.name,
            'description': job.description,
            'requirements': job.requirements,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'job_type': job.job_type,
            'status': job.status,
            'deadline': job.deadline,
        })
    return render(request, 'employer/edit.html', {'form': form, 'title': 'Edit Job Posting'})


# ── Delete a Job ──
@login_required(login_url='/employer/login/')
def delete_job(request, id):
    job = get_object_or_404(JobPosting, id=id)
    employer = get_employer(request)

    if employer and job.employer == employer:
        job.delete()
        messages.success(request, "Job deleted.")
    else:
        messages.error(request, "Permission denied.")
    return redirect('employer:employer_index')


# ── View a Job ──
@login_required(login_url='/employer/login/')
def view_job(request, id):
    job = get_object_or_404(JobPosting, id=id)
    employer = get_employer(request)

    if not employer or job.employer != employer:
        messages.error(request, "Permission denied.")
        return redirect('employer:employer_index')
    applications = job.applications.all() if hasattr(job, 'applications') else []

    return render(request, 'employer/view_job.html', {
        'job': job,
        'applications': applications,
    })