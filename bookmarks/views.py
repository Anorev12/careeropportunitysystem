from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bookmark
from .forms import BookmarkForm


# ── Login ──
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/bookmarks/')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/bookmarks/')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'bookmarks/login.html')


# ── Logout ──
def logout_view(request):
    logout(request)
    return redirect('/bookmarks/login/')


# ── Helper ──
def _get_applicant_or_redirect(request):
    if request.user.role != 'applicant':
        messages.error(request, 'Only applicants can manage bookmarks.')
        return None
    try:
        return request.user.applicant_profile
    except Exception:
        messages.error(request, 'Applicant profile not found.')
        return None


# ── Bookmark List ──
@login_required(login_url='/bookmarks/login/')
def bookmark_list(request):
    applicant = _get_applicant_or_redirect(request)
    if not applicant:
        return redirect('/accounts/dashboard/')

    bookmarks = Bookmark.objects.filter(applicant=applicant)
    return render(request, 'bookmarks/bookmark_list.html', {
        'bookmarks': bookmarks,
    })


# ── Bookmark Add ──
@login_required(login_url='/bookmarks/login/')
def bookmark_add(request):
    applicant = _get_applicant_or_redirect(request)
    if not applicant:
        return redirect('/accounts/dashboard/')

    form = BookmarkForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        bookmark = form.save(commit=False)
        bookmark.applicant = applicant
        bookmark.save()
        messages.success(request, f'"{bookmark.job_title}" bookmarked!')
        return redirect('/bookmarks/')

    return render(request, 'bookmarks/bookmark_form.html', {
        'form': form, 'action': 'Add',
    })


# ── Bookmark Edit ──
@login_required(login_url='/bookmarks/login/')
def bookmark_edit(request, pk):
    applicant = _get_applicant_or_redirect(request)
    if not applicant:
        return redirect('/accounts/dashboard/')

    bookmark = get_object_or_404(Bookmark, pk=pk, applicant=applicant)
    form = BookmarkForm(request.POST or None, instance=bookmark)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Bookmark updated.')
        return redirect('/bookmarks/')

    return render(request, 'bookmarks/bookmark_form.html', {
        'form': form, 'action': 'Edit', 'bookmark': bookmark,
    })


# ── Bookmark Delete ──
@login_required(login_url='/bookmarks/login/')
def bookmark_delete(request, pk):
    applicant = _get_applicant_or_redirect(request)
    if not applicant:
        return redirect('/accounts/dashboard/')

    bookmark = get_object_or_404(Bookmark, pk=pk, applicant=applicant)
    if request.method == 'POST':
        bookmark.delete()
        messages.success(request, 'Bookmark removed.')
        return redirect('/bookmarks/')

    return render(request, 'bookmarks/bookmark_confirm_delete.html', {
        'bookmark': bookmark,
    })