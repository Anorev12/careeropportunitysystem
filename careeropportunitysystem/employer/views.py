from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPosting


def employer_index(request):
    job_postings = JobPosting.objects.all()
    return render(request, 'employer/index.html', {
        'job_postings': job_postings
    })


def apply_job(request, id):
    job = get_object_or_404(JobPosting, id=id)

    return render(request, 'employer/apply.html', {
        'job': job
    })


def edit_job(request, id):
    job = get_object_or_404(JobPosting, id=id)

    return render(request, 'employer/edit.html', {
        'job': job
    })


def delete_job(request, id):
    job = get_object_or_404(JobPosting, id=id)
    job.delete()

    return redirect('employer_index')