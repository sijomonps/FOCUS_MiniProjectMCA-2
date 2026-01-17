from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
import json
import random

from .models import StudySession, Assignment, QuickNote, SubjectFolder
from django.db import models


# Superuser check decorator
def superuser_required(view_func):
    """Decorator to ensure user is a superuser"""
    decorated_view = user_passes_test(
        lambda u: u.is_superuser,
        login_url='dashboard'
    )(view_func)
    return decorated_view

# Preset motivational quotes
MOTIVATIONAL_QUOTES = [
    "The secret of getting ahead is getting started.",
    "Focus on being productive instead of busy.",
    "Small daily improvements lead to stunning results.",
    "Your focus determines your reality.",
    "The only way to do great work is to love what you do.",
    "Success is the sum of small efforts repeated daily.",
    "Don't watch the clock; do what it does. Keep going.",
    "The future depends on what you do today.",
    "Believe you can and you're halfway there.",
    "It always seems impossible until it's done.",
    "Quality is not an act, it is a habit.",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don't stop when you're tired. Stop when you're done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
    "Little things make big days.",
    "It's going to be hard, but hard does not mean impossible.",
    "Don't wait for opportunity. Create it.",
]


# Authentication Views
def signup_view(request):
    """User signup view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# Dashboard View
@login_required
def dashboard_view(request):
    """Main dashboard view"""
    user = request.user
    
    # Get today's study time (in minutes)
    today_total_minutes = StudySession.get_today_total(user)
    
    # Format today's total - show hours if >= 60 minutes, otherwise show minutes
    if today_total_minutes >= 60:
        hours = today_total_minutes // 60
        remaining_mins = today_total_minutes % 60
        if remaining_mins > 0:
            today_total = f"{hours}h {remaining_mins}m"
        else:
            today_total = f"{hours}h"
    else:
        today_total = f"{today_total_minutes}m"
    
    # Get study streak
    streak = StudySession.get_study_streak(user)
    
    # Get weekly data for chart
    weekly_data = StudySession.get_weekly_data(user)
    
    # Prepare weekly chart data
    chart_labels = []
    chart_data = []
    for date, minutes in sorted(weekly_data.items()):
        chart_labels.append(date.strftime('%a'))  # Mon, Tue, etc.
        chart_data.append(minutes)
    
    # Get monthly data for chart - aggregated by month (last 6 months)
    now = timezone.now()
    chart_labels_monthly = []
    chart_data_monthly = []
    
    # Get last 6 months of data aggregated by month
    for i in range(5, -1, -1):  # 5, 4, 3, 2, 1, 0 (oldest to newest)
        # Calculate the target month
        target_date = now - timedelta(days=i * 30)  # Approximate
        target_month = target_date.month
        target_year = target_date.year
        
        # Get total minutes for that month
        month_sessions = StudySession.objects.filter(
            user=user,
            date__year=target_year,
            date__month=target_month
        )
        total_minutes = sum(s.duration for s in month_sessions)
        
        chart_labels_monthly.append(target_date.strftime('%b'))  # Only month name (Jan, Feb, etc.)
        chart_data_monthly.append(total_minutes)
    
    # Get pending assignments (up to 6 for preview)
    assignments = Assignment.objects.filter(user=user, status='pending')[:6]
    
    # Greeting message
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    # Calculate subject breakdown for Pie Chart
    subject_sessions = StudySession.objects.filter(user=user)
    subject_totals = {}
    total_minutes = 0
    
    for session in subject_sessions:
        subject = session.subject
        minutes = session.duration
        subject_totals[subject] = subject_totals.get(subject, 0) + minutes
        total_minutes += minutes
    
    subject_breakdown = []
    if total_minutes > 0:
        for subject, minutes in subject_totals.items():
            percentage = round((minutes / total_minutes) * 100, 1)
            subject_breakdown.append({
                'subject': subject,
                'minutes': minutes,
                'hours': round(minutes / 60, 1),
                'percentage': percentage
            })
    
    # Sort by percentage descending
    subject_breakdown.sort(key=lambda x: x['percentage'], reverse=True)
    
    # Get monthly total hours
    current_month_sessions = StudySession.objects.filter(user=user, date__month=datetime.now().month, date__year=datetime.now().year)
    monthly_total_minutes = sum(s.duration for s in current_month_sessions)
    monthly_total_hours = round(monthly_total_minutes / 60, 1)

    # Prepare Calendar Assignments Data
    all_assignments = Assignment.objects.filter(user=user).exclude(status='completed')
    calendar_assignments = []
    for assign in all_assignments:
        calendar_assignments.append({
            'title': assign.title,
            'deadline': assign.deadline.isoformat(), # This format is safer for JS
            'subject': assign.subject
        })

    # Prepare Subjects List
    subjects = SubjectFolder.objects.filter(user=user)

    # Leaderboard Logic
    # 1. Top Monthly Study Time
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    top_study_users = User.objects.filter(study_sessions__date__gte=month_start) \
        .annotate(total_duration=models.Sum('study_sessions__duration')) \
        .order_by('-total_duration')[:5]
    
    top_study_time_data = []
    for u in top_study_users:
        duration = u.total_duration or 0
        hours = round(duration / 60, 1)
        top_study_time_data.append({
            'username': u.username,
            'value': f"{hours}h",
            'rank': 0 # Will assign index + 1 in template or here
        })

    # Get ALL study time users for modal
    all_study_users = User.objects.filter(study_sessions__date__gte=month_start) \
        .annotate(total_duration=models.Sum('study_sessions__duration')) \
        .order_by('-total_duration')
    
    all_study_time_list = []
    for u in all_study_users:
        duration = u.total_duration or 0
        hours = round(duration / 60, 1)
        all_study_time_list.append({
            'username': u.username,
            'value': f"{hours}h"
        })

    # 2. Top Streaks (calculating for all users - manageable for mini project)
    # Note: For production, store streak in user model field
    all_users = User.objects.all()
    user_streaks_list = []
    for u in all_users:
        s = StudySession.get_study_streak(u)
        if s > 0: # Only show active streaks
            user_streaks_list.append({'username': u.username, 'streak': s, 'value': s})
    
    # Sort and take top 5
    user_streaks_list.sort(key=lambda x: x['streak'], reverse=True)
    top_streaks_data = user_streaks_list[:5]
    
    # All streaks for modal
    all_streaks_list = [{'username': u['username'], 'value': u['streak']} for u in user_streaks_list]

    context = {
        'greeting': greeting,
        'quote': random.choice(MOTIVATIONAL_QUOTES),
        'today_total': today_total,
        'monthly_total_hours': monthly_total_hours,
        'streak': streak,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'chart_labels_monthly': json.dumps(chart_labels_monthly),
        'chart_data_monthly': json.dumps(chart_data_monthly),
        'chart_subject_labels': json.dumps([item['subject'] for item in subject_breakdown]),
        'chart_subject_data': json.dumps([item['minutes'] for item in subject_breakdown]),
        'assignments': assignments,
        'subject_breakdown': subject_breakdown,
        'subjects': subjects,
        'calendar_assignments_json': json.dumps(calendar_assignments),
        'top_study_time': top_study_time_data,
        'top_streaks': top_streaks_data,
        'all_streaks_json': json.dumps(all_streaks_list),
        'all_study_time_json': json.dumps(all_study_time_list),
    }
    
    return render(request, 'core/dashboard.html', context)


# Study Timer View
@login_required
def study_view(request):
    """Study timer page"""
    # Get subjects from SubjectFolder
    folder_subjects = SubjectFolder.objects.filter(user=request.user).values_list('name', flat=True)
    
    # Get subjects from past sessions (legacy compatibility)
    session_subjects = StudySession.objects.filter(user=request.user).values_list('subject', flat=True).distinct()
    
    # Combine and sort unique subjects
    all_subjects = sorted(list(set(list(folder_subjects) + list(session_subjects))))
    
    context = {
        'subjects': all_subjects,
    }
    
    return render(request, 'core/study.html', context)


@login_required
@require_POST
def save_study_session(request):
    """Save study session via AJAX"""
    try:
        data = json.loads(request.body)
        subject = data.get('subject')
        duration = data.get('duration')  # in minutes
        
        if not subject or not duration:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Create study session
        session = StudySession.objects.create(
            user=request.user,
            subject=subject,
            duration=duration,
            date=timezone.now().date()
        )
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'message': 'Study session saved successfully!'
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Assignments View
@login_required
def assignments_view(request):
    """Assignments page with treemap view"""
    pending_assignments = Assignment.objects.filter(user=request.user, status='pending')
    completed_assignments = Assignment.objects.filter(user=request.user, status='completed').order_by('-completed_at')[:5]
    
    # Prepare assignment data for treemap
    assignments_data = []
    for assignment in pending_assignments:
        assignments_data.append({
            'id': assignment.id,
            'title': assignment.title,
            'subject': assignment.subject,
            'deadline': assignment.deadline.isoformat(),
            'estimated_hours': float(assignment.estimated_hours),
            'hours_remaining': assignment.hours_remaining(),
            'days_remaining': assignment.days_remaining(),
            'urgency': assignment.urgency,
        })
    
    context = {
        'pending_assignments': pending_assignments,
        'completed_assignments': completed_assignments,
        'assignments_json': json.dumps(assignments_data),
    }
    
    return render(request, 'core/assignments.html', context)


@login_required
@require_POST
def add_assignment(request):
    """Add new assignment via AJAX"""
    try:
        data = json.loads(request.body)
        
        # Parse deadline string to datetime object
        deadline_str = data.get('deadline')
        # Handle ISO format: 2024-12-25T23:59
        deadline_datetime = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        # Make timezone aware
        deadline_datetime = timezone.make_aware(deadline_datetime)
        
        assignment = Assignment.objects.create(
            user=request.user,
            title=data.get('title'),
            deadline=deadline_datetime,
        )
        
        return JsonResponse({
            'success': True,
            'assignment': {
                'id': assignment.id,
                'title': assignment.title,
                'subject': assignment.subject,
                'deadline': assignment.deadline.isoformat(),
                'estimated_hours': float(assignment.estimated_hours),
                'hours_remaining': assignment.hours_remaining(),
                'days_remaining': assignment.days_remaining(),
                'urgency': assignment.urgency,
            }
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def complete_assignment(request, assignment_id):
    """Mark assignment as completed"""
    try:
        assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
        assignment.status = 'completed'
        assignment.completed_at = timezone.now()
        assignment.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def delete_assignment(request, assignment_id):
    """Delete an assignment"""
    try:
        assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
        assignment.delete()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_all_completed_assignments(request):
    """Get all completed assignments for see more functionality"""
    try:
        completed = Assignment.objects.filter(
            user=request.user, 
            status='completed'
        ).order_by('-completed_at')
        
        completed_data = []
        for assignment in completed:
            completed_data.append({
                'id': assignment.id,
                'title': assignment.title,
                'subject': assignment.subject,
                'completed_at': assignment.completed_at.strftime('%b %d, %Y') if assignment.completed_at else ''
            })
        
        return JsonResponse({'success': True, 'completed': completed_data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Quick Notes View
@login_required
def notes_view(request):
    """Quick Notes page with subject folders"""
    # Get all subject folders for the user with note counts
    folders = SubjectFolder.objects.filter(user=request.user).annotate(
        note_count=models.Count('quick_notes')
    )
    
    # Get total notes count
    total_notes = QuickNote.objects.filter(user=request.user).count()
    
    # Get selected folder
    folder_id = request.GET.get('folder')
    selected_folder = None
    notes = None
    pinned_notes = None
    
    if folder_id:
        try:
            selected_folder = SubjectFolder.objects.get(id=folder_id, user=request.user)
            # Get pinned notes first (max 4)
            pinned_notes = QuickNote.objects.filter(
                user=request.user, 
                subject_folder=selected_folder,
                is_pinned=True
            ).order_by('-pinned_at')[:4]
            # Get all other notes (excluding pinned)
            notes = QuickNote.objects.filter(
                user=request.user, 
                subject_folder=selected_folder,
                is_pinned=False
            ).order_by('-updated_at')
        except SubjectFolder.DoesNotExist:
            notes = QuickNote.objects.none()
            pinned_notes = QuickNote.objects.none()
    else:
        # Show all notes when no folder selected
        pinned_notes = QuickNote.objects.filter(
            user=request.user,
            is_pinned=True
        ).order_by('-pinned_at')[:4]
        notes = QuickNote.objects.filter(
            user=request.user,
            is_pinned=False
        ).order_by('-updated_at')
    
    context = {
        'folders': folders,
        'selected_folder': selected_folder,
        'notes': notes,
        'pinned_notes': pinned_notes,
        'total_notes': total_notes,
    }
    
    return render(request, 'core/notes.html', context)


@login_required
@require_POST
def create_subject_folder(request):
    """Create a new subject folder"""
    try:
        data = json.loads(request.body)
        folder_name = data.get('name', '').strip()
        
        if not folder_name:
            return JsonResponse({'error': 'Folder name is required'}, status=400)
        
        # Check if folder already exists
        if SubjectFolder.objects.filter(user=request.user, name=folder_name).exists():
            return JsonResponse({'error': 'A folder with this name already exists'}, status=400)
        
        folder = SubjectFolder.objects.create(
            user=request.user,
            name=folder_name
        )
        
        return JsonResponse({
            'success': True,
            'folder_id': folder.id,
            'folder_name': folder.name,
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def create_note(request):
    """Create a new note in a folder"""
    try:
        data = json.loads(request.body)
        folder_id = data.get('folder_id')
        title = data.get('title', 'Untitled Note').strip()
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        folder = None
        if folder_id:
            try:
                folder = SubjectFolder.objects.get(id=folder_id, user=request.user)
            except SubjectFolder.DoesNotExist:
                return JsonResponse({'error': 'Folder not found'}, status=404)
        
        note = QuickNote.objects.create(
            user=request.user,
            subject_folder=folder,
            subject=folder.name if folder else 'General',
            title=title,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'note_id': note.id,
            'note_title': note.title,
            'note_content': note.content,
            'created_at': note.created_at.strftime('%b %d, %Y at %I:%M %p'),
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def delete_note(request):
    """Delete a note"""
    try:
        data = json.loads(request.body)
        note_id = data.get('note_id')
        
        note = QuickNote.objects.get(id=note_id, user=request.user)
        note.delete()
        
        return JsonResponse({'success': True})
    
    except QuickNote.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def delete_folder(request):
    """Delete a subject folder and all its notes"""
    try:
        data = json.loads(request.body)
        folder_id = data.get('folder_id')
        
        folder = SubjectFolder.objects.get(id=folder_id, user=request.user)
        folder.delete()  # This will cascade delete all notes in the folder
        
        return JsonResponse({'success': True})
    
    except SubjectFolder.DoesNotExist:
        return JsonResponse({'error': 'Folder not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def delete_subject_folder(request):
    """Delete a subject folder from dashboard"""
    try:
        data = json.loads(request.body)
        folder_id = data.get('folder_id')
        
        if not folder_id:
            return JsonResponse({'error': 'Folder ID is required'}, status=400)
        
        folder = SubjectFolder.objects.get(id=folder_id, user=request.user)
        folder_name = folder.name
        folder.delete()  # This will cascade delete all notes in the folder
        
        return JsonResponse({
            'success': True,
            'message': f'Subject "{folder_name}" deleted successfully'
        })
    
    except SubjectFolder.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def save_quick_note(request):
    """Save quick note after study session"""
    try:
        data = json.loads(request.body)
        
        note = QuickNote.objects.create(
            user=request.user,
            subject=data.get('subject'),
            content=data.get('content'),
            study_duration=data.get('duration'),
        )
        
        return JsonResponse({
            'success': True,
            'note_id': note.id,
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def update_note(request):
    """Update an existing note"""
    try:
        data = json.loads(request.body)
        note_id = data.get('note_id')
        title = data.get('title', 'Untitled').strip()
        content = data.get('content', '').strip()
        
        if not note_id:
            return JsonResponse({'error': 'Note ID is required'}, status=400)
        
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        note = QuickNote.objects.get(id=note_id, user=request.user)
        note.title = title
        note.content = content
        note.save()
        
        return JsonResponse({
            'success': True,
            'note_id': note.id,
            'note_title': note.title,
            'note_content': note.content,
            'updated_at': note.updated_at.strftime('%b %d, %Y at %I:%M %p'),
        })
    
    except QuickNote.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def toggle_pin_note(request):
    """Toggle pin status for a note (max 4 pinned per folder)"""
    try:
        data = json.loads(request.body)
        note_id = data.get('note_id')
        
        if not note_id:
            return JsonResponse({'error': 'Note ID is required'}, status=400)
        
        note = QuickNote.objects.get(id=note_id, user=request.user)
        
        if note.is_pinned:
            # Unpin the note
            note.is_pinned = False
            note.pinned_at = None
            note.save()
            return JsonResponse({
                'success': True,
                'is_pinned': False,
                'message': 'Note unpinned'
            })
        else:
            # Check if already 4 pinned notes in this folder
            pinned_count = QuickNote.objects.filter(
                user=request.user,
                subject_folder=note.subject_folder,
                is_pinned=True
            ).count()
            
            if pinned_count >= 4:
                return JsonResponse({
                    'error': 'Maximum 4 notes can be pinned per subject. Unpin another note first.',
                    'max_reached': True
                }, status=400)
            
            # Pin the note
            note.is_pinned = True
            note.pinned_at = timezone.now()
            note.save()
            return JsonResponse({
                'success': True,
                'is_pinned': True,
                'message': 'Note pinned'
            })
    
    except QuickNote.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# ADMIN VIEWS - Superuser Only
# ========================================

@login_required
@superuser_required
def admin_dashboard_view(request):
    """Admin dashboard with overview of all users and system stats"""
    # Get all users (excluding the current admin for user list)
    all_users = User.objects.all().order_by('-date_joined')
    total_users = all_users.count()
    
    # Get active users (logged in within last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    active_users = User.objects.filter(last_login__gte=week_ago).count()
    
    # Get total study sessions and time
    total_sessions = StudySession.objects.count()
    total_study_minutes = StudySession.objects.aggregate(total=models.Sum('duration'))['total'] or 0
    total_study_hours = round(total_study_minutes / 60, 1)
    
    # Get total assignments
    total_assignments = Assignment.objects.count()
    pending_assignments = Assignment.objects.filter(status='pending').count()
    completed_assignments = Assignment.objects.filter(status='completed').count()
    
    # Get total notes
    total_notes = QuickNote.objects.count()
    
    # Get recent users (last 5)
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # Calculate user stats for display
    user_stats = []
    for user in all_users[:10]:  # Top 10 users
        user_study_time = StudySession.objects.filter(user=user).aggregate(
            total=models.Sum('duration')
        )['total'] or 0
        user_assignments = Assignment.objects.filter(user=user).count()
        user_notes = QuickNote.objects.filter(user=user).count()
        
        user_stats.append({
            'user': user,
            'study_minutes': user_study_time,
            'study_hours': round(user_study_time / 60, 1),
            'assignments': user_assignments,
            'notes': user_notes,
        })
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_sessions': total_sessions,
        'total_study_hours': total_study_hours,
        'total_assignments': total_assignments,
        'pending_assignments': pending_assignments,
        'completed_assignments': completed_assignments,
        'total_notes': total_notes,
        'recent_users': recent_users,
        'user_stats': user_stats,
    }
    
    return render(request, 'core/admin_dashboard.html', context)


@login_required
@superuser_required
def admin_users_view(request):
    """View and manage all users"""
    users = User.objects.all().order_by('-date_joined')
    
    # Calculate stats for each user
    user_list = []
    for user in users:
        study_time = StudySession.objects.filter(user=user).aggregate(
            total=models.Sum('duration')
        )['total'] or 0
        assignments_count = Assignment.objects.filter(user=user).count()
        completed_assignments = Assignment.objects.filter(user=user, status='completed').count()
        notes_count = QuickNote.objects.filter(user=user).count()
        folders_count = SubjectFolder.objects.filter(user=user).count()
        
        user_list.append({
            'user': user,
            'study_hours': round(study_time / 60, 1),
            'study_minutes': study_time,
            'assignments': assignments_count,
            'completed_assignments': completed_assignments,
            'notes': notes_count,
            'folders': folders_count,
        })
    
    context = {
        'users': user_list,
        'total_users': len(user_list),
    }
    
    return render(request, 'core/admin_users.html', context)


@login_required
@superuser_required
def admin_user_detail_view(request, user_id):
    """View detailed information about a specific user"""
    target_user = get_object_or_404(User, id=user_id)
    
    # Get user's study sessions
    study_sessions = StudySession.objects.filter(user=target_user).order_by('-created_at')[:20]
    total_study_time = StudySession.objects.filter(user=target_user).aggregate(
        total=models.Sum('duration')
    )['total'] or 0
    
    # Get user's assignments
    assignments = Assignment.objects.filter(user=target_user).order_by('-created_at')[:20]
    
    # Get user's notes
    notes = QuickNote.objects.filter(user=target_user).order_by('-updated_at')[:20]
    
    # Get user's folders
    folders = SubjectFolder.objects.filter(user=target_user)
    
    # Subject breakdown
    subject_sessions = StudySession.objects.filter(user=target_user)
    subject_totals = {}
    for session in subject_sessions:
        subject_totals[session.subject] = subject_totals.get(session.subject, 0) + session.duration
    
    subject_breakdown = sorted(
        [{'subject': k, 'minutes': v, 'hours': round(v/60, 1)} for k, v in subject_totals.items()],
        key=lambda x: x['minutes'],
        reverse=True
    )
    
    context = {
        'target_user': target_user,
        'study_sessions': study_sessions,
        'total_study_hours': round(total_study_time / 60, 1),
        'total_study_minutes': total_study_time,
        'assignments': assignments,
        'pending_assignments': Assignment.objects.filter(user=target_user, status='pending').count(),
        'completed_assignments': Assignment.objects.filter(user=target_user, status='completed').count(),
        'notes': notes,
        'folders': folders,
        'subject_breakdown': subject_breakdown,
    }
    
    return render(request, 'core/admin_user_detail.html', context)


@login_required
@superuser_required
@require_POST
def admin_toggle_user_status(request):
    """Toggle user active status (enable/disable)"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)
        
        target_user = User.objects.get(id=user_id)
        
        # Don't allow disabling yourself
        if target_user == request.user:
            return JsonResponse({'error': 'Cannot disable your own account'}, status=400)
        
        # Don't allow disabling other superusers
        if target_user.is_superuser:
            return JsonResponse({'error': 'Cannot disable superuser accounts'}, status=400)
        
        target_user.is_active = not target_user.is_active
        target_user.save()
        
        status_text = 'enabled' if target_user.is_active else 'disabled'
        return JsonResponse({
            'success': True,
            'is_active': target_user.is_active,
            'message': f'User {target_user.username} has been {status_text}'
        })
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@superuser_required
@require_POST
def admin_delete_user(request):
    """Delete a user and all their data"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)
        
        target_user = User.objects.get(id=user_id)
        
        # Don't allow deleting yourself
        if target_user == request.user:
            return JsonResponse({'error': 'Cannot delete your own account'}, status=400)
        
        # Don't allow deleting other superusers
        if target_user.is_superuser:
            return JsonResponse({'error': 'Cannot delete superuser accounts'}, status=400)
        
        username = target_user.username
        target_user.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'User {username} has been deleted'
        })
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)