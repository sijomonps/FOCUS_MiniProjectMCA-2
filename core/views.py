from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.db.models import Sum

from .models import StudySession, Assignment, QuickNote, SubjectFolder


# Authentication Views
def signup_view(request):
    """User signup view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
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
    
    # Get today's study time
    today_total = StudySession.get_today_total(user)
    
    # Get study streak
    streak = StudySession.get_study_streak(user)
    
    # Get weekly data for chart
    weekly_data = StudySession.get_weekly_data(user)
    
    # Prepare chart data (Weekly)
    chart_labels = []
    chart_data = []
    for date, minutes in sorted(weekly_data.items()):
        chart_labels.append(date.strftime('%a'))  # Mon, Tue, etc.
        chart_data.append(minutes)

    # Get monthly data for chart
    monthly_chart_data_raw = StudySession.get_monthly_data(user)
    chart_labels_monthly = []
    chart_data_monthly = []
    for date, minutes in sorted(monthly_chart_data_raw.items()):
        chart_labels_monthly.append(date.strftime('%d')) # Just day number
        chart_data_monthly.append(minutes)
    
    # Get pending assignments (up to 6 for preview list)
    assignments = Assignment.objects.filter(user=user, status='pending')[:6]
    
    # Get all pending assignments for calendar
    all_assignments = Assignment.objects.filter(user=user, status='pending')
    calendar_assignments = []
    for assignment in all_assignments:
        calendar_assignments.append({
            'id': assignment.id,
            'title': assignment.title,
            'subject': assignment.subject,
            'deadline': assignment.deadline.isoformat(),
            'urgency': assignment.urgency,
            'status': assignment.status
        })
    
    # Greeting message
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
        
    # Random motivational quote
    import random
    quotes = [
        "The future belongs to those who believe in the beauty of their dreams.",
        "It always seems impossible until it's done.",
        "Success is the sum of small efforts, repeated day in and day out.",
        "Don't watch the clock; do what it does. Keep going.",
        "The secret of getting ahead is getting started.",
        "Believe you can and you're halfway there.",
        "Study hard what interests you the most in the most undisciplined, irreverent and original manner possible.",
    ]
    quote = random.choice(quotes)
    
    # Calculate Monthly Stats
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    monthly_sessions = StudySession.objects.filter(
        user=user,
        date__gte=start_of_month,
        date__lte=today
    )
    
    # Monthly Total
    monthly_total_minutes = monthly_sessions.aggregate(total=Sum('duration'))['total'] or 0
    monthly_total_hours = round(monthly_total_minutes / 60, 1)
    
    # Subject breakdown (for this month)
    subject_stats = monthly_sessions.values('subject').annotate(
        total_minutes=Sum('duration')
    ).order_by('-total_minutes')
    
    subject_breakdown = []
    for item in subject_stats:
        subject_breakdown.append({
            'subject': item['subject'],
            'hours': round(item['total_minutes'] / 60, 1),
            'minutes': item['total_minutes'],
            'percentage': round((item['total_minutes'] / monthly_total_minutes * 100), 1) if monthly_total_minutes > 0 else 0
        })
    
    # Get subjects for quick add/view
    subjects = SubjectFolder.objects.filter(user=user)

    context = {
        'greeting': greeting,
        'quote': quote,
        'today_total': today_total,
        'streak': streak,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'chart_labels_monthly': json.dumps(chart_labels_monthly),
        'chart_data_monthly': json.dumps(chart_data_monthly),
        'assignments': assignments,
        'calendar_assignments_json': json.dumps(calendar_assignments),
        'subjects': subjects,
        'monthly_total_hours': monthly_total_hours,
        'subject_breakdown': subject_breakdown,
    }
    
    return render(request, 'core/dashboard.html', context)


# Study Timer View
@login_required
def study_view(request):
    """Study timer page"""
    # Get subjects from SubjectFolder
    subjects = SubjectFolder.objects.filter(user=request.user)
    
    context = {
        'subjects': subjects,
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
    completed_assignments = Assignment.objects.filter(user=request.user, status='completed')[:10]
    
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


# Quick Notes View
@login_required
def notes_view(request):
    """Quick Notes page with subject folders"""
    # Get all subject folders for the user
    folders = SubjectFolder.objects.filter(user=request.user)
    
    # Get selected folder
    folder_id = request.GET.get('folder')
    selected_folder = None
    notes = None
    
    if folder_id:
        try:
            selected_folder = SubjectFolder.objects.get(id=folder_id, user=request.user)
            notes = QuickNote.objects.filter(user=request.user, subject_folder=selected_folder)
        except SubjectFolder.DoesNotExist:
            notes = QuickNote.objects.none()
    else:
        # Show all notes without a folder (legacy notes)
        notes = QuickNote.objects.filter(user=request.user, subject_folder__isnull=True)
    
    context = {
        'folders': folders,
        'selected_folder': selected_folder,
        'notes': notes,
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
def edit_note(request):
    """Edit an existing note"""
    try:
        data = json.loads(request.body)
        note_id = data.get('note_id')
        title = data.get('title', 'Untitled Note').strip()
        content = data.get('content', '').strip()
        
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
        })
    
    except QuickNote.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
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
def delete_assignment(request, assignment_id):
    """Delete an assignment"""
    try:
        assignment = Assignment.objects.get(id=assignment_id, user=request.user)
        assignment.delete()
        return JsonResponse({'success': True})
    except Assignment.DoesNotExist:
        return JsonResponse({'error': 'Assignment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
