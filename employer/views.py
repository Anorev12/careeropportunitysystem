from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPosting, Employer
from .forms import JobPostingForm

def get_employer(request):
    try:
        return Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        return None

@login_required
def employer_index(request):
    employer = get_employer(request)
    if not employer:
        messages.warning(request, "No employer profile found. Ask admin to create one.")
        job_postings = []
    else:
        job_postings = JobPosting.objects.filter(employer=employer)
    return render(request, 'employer/index.html', {
        'job_postings': job_postings,
        'employer': employer,
    })

@login_required
def create_job(request):
    employer = get_employer(request)
    if not employer:
        messages.error(request, "No employer profile found.")
        return redirect('employer_index')

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('employer_index')
    else:
        form = JobPostingForm()

    return render(request, 'employer/edit.html', {'form': form, 'title': 'Post New Job'})

@login_required
def edit_job(request, id):
    job = get_object_or_404(JobPosting, id=id)
    employer = get_employer(request)

    if not employer or job.employer != employer:
        messages.error(request, "Permission denied.")
        return redirect('employer_index')

    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated!")
            return redirect('employer_index')
    else:
        form = JobPostingForm(instance=job)

    return render(request, 'employer/edit.html', {'form': form, 'title': 'Edit Job Posting'})

@login_required
def delete_job(request, id):
    job = get_object_or_404(JobPosting, id=id)
    employer = get_employer(request)

    if employer and job.employer == employer:
        job.delete()
        messages.success(request, "Job deleted.")
    else:
        messages.error(request, "Permission denied.")

    return redirect('employer_index')

@login_required
def view_job(request, id):
    job = get_object_or_404(JobPosting, id=id)
    employer = get_employer(request)

    if not employer or job.employer != employer:
        messages.error(request, "Permission denied.")
        return redirect('employer_index')

    try:
        applications = job.application_set.all()
    except Exception:
        applications = []

    return render(request, 'employer/view_job.html', {
        'job': job,
        'applications': applications,
    })