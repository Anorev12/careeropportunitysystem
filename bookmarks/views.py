from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bookmark
from .forms import BookmarkForm


# LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        return redirect('bookmarks:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Session management
            request.session['username'] = user.username
            request.session['is_logged_in'] = True

            messages.success(request, 'Login successful.')
            return redirect('bookmarks:home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'bookmarks/login.html')


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('bookmarks:login')


# HOME PAGE AFTER LOGIN
@login_required(login_url='/bookmarks/login/')
def home_view(request):
    username = request.session.get('username', request.user.username)

    return render(request, 'bookmarks/home.html', {
        'username': username
    })


# EDIT PROFILE PAGE
@login_required(login_url='/bookmarks/login/')
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('bookmarks:home')

    return render(request, 'bookmarks/edit_profile.html')


# HELPER FUNCTION
def _get_applicant_or_redirect(request):
    try:
        if request.user.role != 'applicant':
            messages.error(request, 'Only applicants can manage bookmarks.')
            return None
    except Exception:
        pass

    try:
        return request.user.applicant_profile
    except Exception:
        messages.error(request, 'Applicant profile not found.')
        return None


# VIEW RECORDS / BOOKMARK LIST
@login_required(login_url='/bookmarks/login/')
def bookmark_list(request):
    applicant = _get_applicant_or_redirect(request)

    if not applicant:
        return redirect('bookmarks:home')

    bookmarks = Bookmark.objects.filter(applicant=applicant)

    return render(request, 'bookmarks/bookmark_list.html', {
        'bookmarks': bookmarks,
    })


# ADD NEW RECORD
@login_required(login_url='/bookmarks/login/')
def bookmark_add(request):
    applicant = _get_applicant_or_redirect(request)

    if not applicant:
        return redirect('bookmarks:home')

    form = BookmarkForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        bookmark = form.save(commit=False)
        bookmark.applicant = applicant
        bookmark.save()

        messages.success(request, f'"{bookmark.job_title}" added successfully.')
        return redirect('bookmarks:list')

    return render(request, 'bookmarks/bookmark_form.html', {
        'form': form,
        'action': 'Add',
    })


# EDIT BOOKMARK
@login_required(login_url='/bookmarks/login/')
def bookmark_edit(request, pk):
    applicant = _get_applicant_or_redirect(request)

    if not applicant:
        return redirect('bookmarks:home')

    bookmark = get_object_or_404(Bookmark, pk=pk, applicant=applicant)
    form = BookmarkForm(request.POST or None, instance=bookmark)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Record updated successfully.')
        return redirect('bookmarks:list')

    return render(request, 'bookmarks/bookmark_form.html', {
        'form': form,
        'action': 'Edit',
        'bookmark': bookmark,
    })


# DELETE BOOKMARK
@login_required(login_url='/bookmarks/login/')
def bookmark_delete(request, pk):
    applicant = _get_applicant_or_redirect(request)

    if not applicant:
        return redirect('bookmarks:home')

    bookmark = get_object_or_404(Bookmark, pk=pk, applicant=applicant)

    if request.method == 'POST':
        bookmark.delete()
        messages.success(request, 'Record removed successfully.')
        return redirect('bookmarks:list')

    return render(request, 'bookmarks/bookmark_confirm_delete.html', {
        'bookmark': bookmark,
    })

@login_required(login_url='/bookmarks/login/')
def home_view(request):
    username = request.session.get('username', request.user.username)

    return render(request, 'bookmarks/home.html', {
        'username': username
    })