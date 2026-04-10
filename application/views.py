from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, Interview
from .forms import ApplicationForm, ApplicationStatusForm, InterviewForm
from employer.models import JobPosting


# ── helper ────────────────────────────────────────────────────────────────────

def get_applicant(request):
    try:
        return request.user.applicant_profile
    except AttributeError:
        return None


# ── Application List ──────────────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
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


# ── Apply for a Job ───────────────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, pk=job_id)
    applicant = get_applicant(request)

    if not applicant:
        messages.error(request, "Only applicants can apply for jobs.")
        return redirect('application_list')

    if Application.objects.filter(applicant=applicant, job_posting=job).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('application_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.applicant   = applicant
            app.job_posting = job
            app.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('application_list')
    else:
        form = ApplicationForm(initial={'job_posting': job})

    return render(request, 'application/apply_job.html', {'form': form, 'job': job})


# ── Application Detail ────────────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    interviews  = application.interviews.all()
    return render(request, 'application/application_detail.html', {
        'application': application,
        'interviews':  interviews,
    })


# ── Withdraw Application ──────────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
def withdraw_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    applicant   = get_applicant(request)

    if not applicant or application.applicant != applicant:
        messages.error(request, "Permission denied.")
        return redirect('application_list')

    if application.status not in ('accepted', 'rejected'):
        application.status = 'withdrawn'
        application.save()
        messages.success(request, "Application withdrawn.")
    else:
        messages.warning(request, "Cannot withdraw a finalised application.")

    return redirect('application_list')


# ── Update Application Status ─────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application status updated.")
            return redirect('application_detail', pk=pk)
    else:
        form = ApplicationStatusForm(instance=application)

    return render(request, 'application/update_status.html', {
        'form':        form,
        'application': application,
    })


# ── Schedule Interview ────────────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
def schedule_interview(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)

    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            messages.success(request, "Interview scheduled.")
            return redirect('application_detail', pk=application_pk)
    else:
        form = InterviewForm()

    return render(request, 'application/schedule_interview.html', {
        'form':        form,
        'application': application,
    })


# ── Edit Interview ────────────────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
def edit_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk)

    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview updated.")
            return redirect('application_detail', pk=interview.application.pk)
    else:
        form = InterviewForm(instance=interview)

    return render(request, 'application/schedule_interview.html', {
        'form':        form,
        'application': interview.application,
        'edit_mode':   True,
    })


# ── Delete Interview ──────────────────────────────────────────────────────────

@login_required(login_url='/employer/login/')
def delete_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    app_pk    = interview.application.pk
    interview.delete()
    messages.success(request, "Interview deleted.")
    return redirect('application_detail', pk=app_pk)