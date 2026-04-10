from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bookmark
from .forms import BookmarkForm


def _get_applicant_or_redirect(request):
    """Helper: return applicant profile or None if user is not an applicant."""
    if request.user.role != 'applicant':
        messages.error(request, 'Only applicants can manage bookmarks.')
        return None
    try:
        return request.user.applicant_profile
    except Exception:
        messages.error(request, 'Applicant profile not found.')
        return None


@login_required
def bookmark_list(request):
    """List all bookmarks for the logged-in applicant."""
    applicant = _get_applicant_or_redirect(request)
    if not applicant:
        return redirect('/accounts/dashboard/')

    bookmarks = Bookmark.objects.filter(applicant=applicant)
    return render(request, 'bookmarks/bookmark_list.html', {
        'bookmarks': bookmarks,
    })


@login_required
def bookmark_add(request):
    """Add a new bookmark."""
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


@login_required
def bookmark_edit(request, pk):
    """Edit an existing bookmark."""
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


@login_required
def bookmark_delete(request, pk):
    """Delete a bookmark (POST only)."""
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