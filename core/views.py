from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
import json
import random

from .models import StudySession, Assignment, QuickNote, SubjectFolder, SupportMessage
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
        if request.user.is_superuser:
            return redirect('admin_dashboard')
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
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.is_superuser:
                    return redirect('admin_dashboard')
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    
    # Get approved feedbacks for marquee
    approved_feedbacks = SupportMessage.objects.filter(
        message_type='feedback',
        is_approved_feedback=True
    ).select_related('sender').order_by('-created_at')[:10]
    
    return render(request, 'core/login.html', {
        'form': form,
        'approved_feedbacks': approved_feedbacks
    })


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
    
    # Get pending assignments with deadlines (up to 6 for preview)
    # Filter out assignments without deadlines since they can't be scheduled
    assignments = Assignment.objects.filter(
        user=user, 
        deadline__isnull=False
    ).exclude(status='completed').order_by('deadline')[:6]
    
    # Get assignments without deadlines (backlog)
    no_deadline_assignments = Assignment.objects.filter(
        user=user,
        deadline__isnull=True
    ).exclude(status='completed').order_by('-created_at')[:10]
    
    # Enhanced greeting message with precise timing
    now = timezone.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 17:
        greeting = "Good afternoon!"
    elif 17 <= hour < 21:
        greeting = "Good evening!"
    else:
        greeting = "Hello there!"  # Late night or very early morning
    
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
        # Only include assignments with deadlines
        if assign.deadline:
            local_deadline = timezone.localtime(assign.deadline)
            calendar_assignments.append({
                'title': assign.title,
                'deadline': local_deadline.strftime('%Y-%m-%dT%H:%M:%S'),
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

    # Get total pending count (all non-completed assignments, including those without deadlines)
    pending_assignments_count = Assignment.objects.filter(user=user).exclude(status='completed').count()

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
        'no_deadline_assignments': no_deadline_assignments,
        'pending_assignments_count': pending_assignments_count,
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
    
    # Add greeting message
    now = timezone.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        greeting = "Ready to focus?"
    elif 12 <= hour < 17:
        greeting = "Afternoon focus time!"
    elif 17 <= hour < 21:
        greeting = "Evening study session?"
    else:
        greeting = "Late night productivity?"
    
    context = {
        'subjects': all_subjects,
        'greeting': greeting,
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
        
        # Get updated today's total and streak
        today_total = StudySession.get_today_total(request.user)
        current_streak = StudySession.get_study_streak(request.user)
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'message': 'Study session saved successfully!',
            'today_total_minutes': today_total,
            'current_streak': current_streak
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_today_study_time(request):
    """Get user's total study time for today from database"""
    try:
        today_total = StudySession.get_today_total(request.user)
        return JsonResponse({
            'success': True,
            'today_total_minutes': today_total
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_dashboard_stats(request):
    """Get updated dashboard statistics via AJAX"""
    try:
        user = request.user
        
        # Get today's study time (in minutes)
        today_total_minutes = StudySession.get_today_total(user)
        
        # Format today's total
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
        chart_labels = []
        chart_data = []
        for date, minutes in sorted(weekly_data.items()):
            chart_labels.append(date.strftime('%a'))
            chart_data.append(minutes)
        
        # Get monthly data for chart
        now = timezone.now()
        chart_labels_monthly = []
        chart_data_monthly = []
        for i in range(5, -1, -1):
            target_date = now - timedelta(days=i * 30)
            target_month = target_date.month
            target_year = target_date.year
            month_sessions = StudySession.objects.filter(
                user=user,
                date__year=target_year,
                date__month=target_month
            )
            total_minutes = sum(s.duration for s in month_sessions)
            chart_labels_monthly.append(target_date.strftime('%b'))
            chart_data_monthly.append(total_minutes)
        
        # Get monthly total hours
        current_month_sessions = StudySession.objects.filter(
            user=user, 
            date__month=datetime.now().month, 
            date__year=datetime.now().year
        )
        monthly_total_minutes = sum(s.duration for s in current_month_sessions)
        monthly_total_hours = round(monthly_total_minutes / 60, 1)
        
        # Calculate subject breakdown for Pie Chart
        subject_sessions = StudySession.objects.filter(user=user)
        subject_totals = {}
        total_minutes_all = 0
        for session in subject_sessions:
            subject = session.subject
            minutes = session.duration
            subject_totals[subject] = subject_totals.get(subject, 0) + minutes
            total_minutes_all += minutes
        
        subject_labels = []
        subject_data = []
        if total_minutes_all > 0:
            sorted_subjects = sorted(subject_totals.items(), key=lambda x: x[1], reverse=True)
            for subject, minutes in sorted_subjects:
                subject_labels.append(subject)
                subject_data.append(minutes)
        
        # Get pending assignments count
        pending_count = Assignment.objects.filter(user=user).exclude(status='completed').count()
        
        # Leaderboard data
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Top study time this month
        top_study_users = User.objects.filter(study_sessions__date__gte=month_start) \
            .annotate(total_duration=models.Sum('study_sessions__duration')) \
            .order_by('-total_duration')[:5]
        top_study_time_list = []
        for u in top_study_users:
            duration = u.total_duration or 0
            hours = round(duration / 60, 1)
            top_study_time_list.append({'username': u.username, 'value': f"{hours}h"})
        
        # Top streaks
        all_users = User.objects.all()
        user_streaks = []
        for u in all_users:
            s = StudySession.get_study_streak(u)
            if s > 0:
                user_streaks.append({'username': u.username, 'streak': s, 'value': s})
        user_streaks.sort(key=lambda x: x['streak'], reverse=True)
        top_streaks_list = user_streaks[:5]
        
        # All data for modal
        all_study_users = User.objects.filter(study_sessions__date__gte=month_start) \
            .annotate(total_duration=models.Sum('study_sessions__duration')) \
            .order_by('-total_duration')
        all_study_time_list = []
        for u in all_study_users:
            duration = u.total_duration or 0
            hours = round(duration / 60, 1)
            all_study_time_list.append({'username': u.username, 'value': f"{hours}h"})
        all_streaks_list = [{'username': u['username'], 'value': u['streak']} for u in user_streaks]
        
        return JsonResponse({
            'success': True,
            'today_total': today_total,
            'today_total_minutes': today_total_minutes,
            'streak': streak,
            'monthly_total_hours': monthly_total_hours,
            'pending_count': pending_count,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'chart_labels_monthly': chart_labels_monthly,
            'chart_data_monthly': chart_data_monthly,
            'subject_labels': subject_labels,
            'subject_data': subject_data,
            'top_streaks': top_streaks_list,
            'top_study_time': top_study_time_list,
            'all_streaks': all_streaks_list,
            'all_study_time': all_study_time_list,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Assignments View
@login_required
def assignments_view(request):
    """Assignments page with Kanban board view"""
    # Get pending assignments (todo, in_progress, or legacy 'pending' status)
    pending_assignments = Assignment.objects.filter(
        user=request.user
    ).exclude(status='completed')
    
    completed_assignments = Assignment.objects.filter(user=request.user, status='completed').order_by('-completed_at')[:5]
    
    # Prepare assignment data for Kanban board
    assignments_data = []
    for assignment in pending_assignments:
        # Handle deadline properly (could be None)
        deadline_str = ''
        if assignment.deadline:
            local_deadline = timezone.localtime(assignment.deadline)
            deadline_str = local_deadline.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Map legacy 'pending' status to 'todo'
        status = assignment.status if assignment.status in ['todo', 'in_progress'] else 'todo'
        assignments_data.append({
            'id': assignment.id,
            'title': assignment.title,
            'description': assignment.description,
            'subject': assignment.subject,
            'deadline': deadline_str,
            'estimated_hours': float(assignment.estimated_hours),
            'hours_remaining': assignment.hours_remaining(),
            'days_remaining': assignment.days_remaining(),
            'urgency': assignment.urgency,
            'priority': assignment.priority,
            'status': status,
        })
    
    # Add greeting message
    now = timezone.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        greeting = "Time to tackle your tasks!"
    elif 12 <= hour < 17:
        greeting = "Afternoon productivity!"
    elif 17 <= hour < 21:
        greeting = "Evening assignments!"
    else:
        greeting = "Working late?"
    
    context = {
        'pending_assignments': pending_assignments,
        'completed_assignments': completed_assignments,
        'assignments_json': json.dumps(assignments_data),
        'greeting': greeting,
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
        deadline_datetime = None
        
        # Only process deadline if provided and not null/empty
        if deadline_str and str(deadline_str).strip() and deadline_str != 'null':
            try:
                # Handle ISO format: 2024-12-25T23:59 or just date 2024-12-25
                if 'T' in str(deadline_str):
                    deadline_datetime = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
                else:
                    # If no time provided, default to end of day (23:59)
                    deadline_datetime = datetime.strptime(str(deadline_str) + 'T23:59', '%Y-%m-%dT%H:%M')
                # Make timezone aware using the current timezone
                deadline_datetime = timezone.make_aware(deadline_datetime, timezone.get_current_timezone())
            except ValueError as e:
                # If parsing fails, set deadline to None
                print(f"Deadline parsing error: {e}")
                deadline_datetime = None
        
        assignment = Assignment.objects.create(
            user=request.user,
            title=data.get('title'),
            description=data.get('description', ''),
            priority=data.get('priority', 'normal'),
            deadline=deadline_datetime,
            status=data.get('status', 'todo'),  # Use status from form
        )
        
        # Handle deadline format properly (could be None)
        deadline_str = ''
        if assignment.deadline:
            local_deadline = timezone.localtime(assignment.deadline)
            deadline_str = local_deadline.strftime('%Y-%m-%dT%H:%M:%S')
        
        return JsonResponse({
            'success': True,
            'assignment': {
                'id': assignment.id,
                'title': assignment.title,
                'description': assignment.description,
                'subject': assignment.subject,
                'deadline': deadline_str,
                'estimated_hours': float(assignment.estimated_hours),
                'hours_remaining': assignment.hours_remaining(),
                'days_remaining': assignment.days_remaining(),
                'urgency': assignment.urgency,
                'priority': assignment.priority,
                'status': assignment.status,
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
def update_assignment_status(request, assignment_id):
    """Update assignment status (todo, in_progress)"""
    try:
        import json
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status not in ['todo', 'in_progress']:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
        assignment.status = new_status
        assignment.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def update_assignment(request, assignment_id):
    """Update assignment details (title, description, priority, deadline, status)"""
    try:
        import json
        data = json.loads(request.body)
        
        assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
        
        # Update fields if provided
        if 'title' in data:
            assignment.title = data['title']
        if 'description' in data:
            assignment.description = data['description']
        if 'priority' in data:
            assignment.priority = data['priority']
        if 'status' in data and data['status'] in ['todo', 'in_progress']:
            assignment.status = data['status']
        
        # Handle deadline - can be empty string to clear
        if 'deadline' in data:
            deadline_str = data['deadline']
            if deadline_str:
                try:
                    from datetime import datetime
                    deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                    assignment.deadline = deadline
                except:
                    pass
            else:
                assignment.deadline = None
        
        assignment.save()
        
        # Return updated assignment data
        assignment_data = {
            'id': assignment.id,
            'title': assignment.title,
            'subject': assignment.subject,
            'description': assignment.description,
            'priority': assignment.priority,
            'deadline': assignment.deadline.isoformat() if assignment.deadline else None,
            'status': assignment.status,
        }
        
        return JsonResponse({'success': True, 'assignment': assignment_data})
    
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
    
    # Add greeting message
    now = timezone.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        greeting = "Ready to take notes?"
    elif 12 <= hour < 17:
        greeting = "Afternoon note-taking!"
    elif 17 <= hour < 21:
        greeting = "Evening study notes?"
    else:
        greeting = "Late night thoughts?"
    
    context = {
        'folders': folders,
        'selected_folder': selected_folder,
        'notes': notes,
        'pinned_notes': pinned_notes,
        'total_notes': total_notes,
        'greeting': greeting,
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


@login_required
@superuser_required
def admin_generate_report(request):
    """Generate PDF report of all users and their activities"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from io import BytesIO
    
    # Create the HttpResponse object with PDF headers
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Container for the PDF elements
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#6699BB')
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#333333')
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Title
    elements.append(Paragraph('FOCUS - User Activity Report', title_style))
    elements.append(Paragraph(f'Generated on: {timezone.now().strftime("%B %d, %Y at %H:%M")}', normal_style))
    elements.append(Spacer(1, 20))
    
    # Platform Statistics
    elements.append(Paragraph('Platform Overview', heading_style))
    
    total_users = User.objects.count()
    total_sessions = StudySession.objects.count()
    total_study_minutes = StudySession.objects.aggregate(total=models.Sum('duration'))['total'] or 0
    total_assignments = Assignment.objects.count()
    total_notes = QuickNote.objects.count()
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Users', str(total_users)],
        ['Total Study Sessions', str(total_sessions)],
        ['Total Study Time', f'{round(total_study_minutes / 60, 1)} hours'],
        ['Total Assignments', str(total_assignments)],
        ['Total Notes', str(total_notes)],
    ]
    
    stats_table = Table(stats_data, colWidths=[200, 150])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6699BB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 30))
    
    # All Users Summary Table
    elements.append(Paragraph('All Users Summary', heading_style))
    
    users = User.objects.all().order_by('-date_joined')
    user_data = [['Username', 'Email', 'Status', 'Role', 'Study Time', 'Assignments', 'Notes', 'Joined']]
    
    for user in users:
        study_time = StudySession.objects.filter(user=user).aggregate(
            total=models.Sum('duration')
        )['total'] or 0
        assignments_count = Assignment.objects.filter(user=user).count()
        notes_count = QuickNote.objects.filter(user=user).count()
        
        user_data.append([
            user.username,
            user.email or 'N/A',
            'Active' if user.is_active else 'Disabled',
            'Admin' if user.is_superuser else 'User',
            f'{round(study_time / 60, 1)}h',
            str(assignments_count),
            str(notes_count),
            user.date_joined.strftime('%Y-%m-%d')
        ])
    
    user_table = Table(user_data, colWidths=[80, 120, 60, 50, 70, 70, 50, 80])
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#669977')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    elements.append(user_table)
    
    # Individual User Details
    elements.append(PageBreak())
    elements.append(Paragraph('Individual User Details', title_style))
    
    for user in users:
        elements.append(Paragraph(f'User: {user.username}', heading_style))
        
        # User info
        info_text = f"Email: {user.email or 'N/A'} | Status: {'Active' if user.is_active else 'Disabled'} | "
        info_text += f"Role: {'Administrator' if user.is_superuser else 'Regular User'} | "
        info_text += f"Joined: {user.date_joined.strftime('%B %d, %Y')}"
        elements.append(Paragraph(info_text, normal_style))
        
        # Study Sessions Summary
        study_sessions = StudySession.objects.filter(user=user)
        total_time = study_sessions.aggregate(total=models.Sum('duration'))['total'] or 0
        
        # Subject breakdown
        subject_totals = {}
        for session in study_sessions:
            subject_totals[session.subject] = subject_totals.get(session.subject, 0) + session.duration
        
        if subject_totals:
            elements.append(Paragraph('Study Time by Subject:', normal_style))
            subject_data = [['Subject', 'Time Studied']]
            for subject, minutes in sorted(subject_totals.items(), key=lambda x: x[1], reverse=True):
                subject_data.append([subject, f'{round(minutes / 60, 1)} hours ({minutes} min)'])
            subject_data.append(['TOTAL', f'{round(total_time / 60, 1)} hours'])
            
            subject_table = Table(subject_data, colWidths=[200, 150])
            subject_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CCBB66')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8e8e8')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ]))
            elements.append(subject_table)
        else:
            elements.append(Paragraph('No study sessions recorded.', normal_style))
        
        # Assignments
        assignments = Assignment.objects.filter(user=user)
        pending = assignments.filter(status='pending').count()
        completed = assignments.filter(status='completed').count()
        elements.append(Paragraph(f'Assignments: {pending} pending, {completed} completed', normal_style))
        
        # Notes
        notes_count = QuickNote.objects.filter(user=user).count()
        folders_count = SubjectFolder.objects.filter(user=user).count()
        elements.append(Paragraph(f'Notes: {notes_count} notes in {folders_count} folders', normal_style))
        
        elements.append(Spacer(1, 20))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and create response
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FOCUS_User_Report_{timezone.now().strftime("%Y%m%d_%H%M")}.pdf"'
    response.write(pdf)
    
    return response


@login_required
@superuser_required
def admin_passwords_view(request):
    """View and manage user passwords"""
    users = User.objects.all().order_by('username')
    
    user_list = []
    for user in users:
        user_list.append({
            'user': user,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
        })
    
    context = {
        'users': user_list,
        'total_users': len(user_list),
    }
    
    return render(request, 'core/admin_passwords.html', context)


@login_required
@superuser_required
@require_POST
def admin_change_password(request):
    """Change a user's password"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        new_password = data.get('new_password')
        
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)
        
        if not new_password:
            return JsonResponse({'error': 'New password is required'}, status=400)
        
        if len(new_password) < 6:
            return JsonResponse({'error': 'Password must be at least 6 characters long'}, status=400)
        
        target_user = User.objects.get(id=user_id)
        
        # Set the new password
        target_user.set_password(new_password)
        target_user.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Password for {target_user.username} has been changed successfully'
        })
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# SUPPORT / CHAT VIEWS
# ========================================

@login_required
def support_view(request):
    """Support/Chat page for users to communicate with admin"""
    user = request.user
    
    # Get user's messages (sent and received)
    user_messages = SupportMessage.objects.filter(
        models.Q(sender=user) | models.Q(recipient=user)
    ).order_by('-created_at')
    
    # Get user's study sessions for time correction requests
    study_sessions = StudySession.objects.filter(user=user).order_by('-date', '-created_at')[:50]
    
    # Group sessions by subject for easy selection
    session_subjects = {}
    for session in study_sessions:
        if session.subject not in session_subjects:
            session_subjects[session.subject] = []
        session_subjects[session.subject].append({
            'id': session.id,
            'date': session.date.strftime('%b %d, %Y'),
            'duration': session.duration,
            'formatted_duration': f"{session.duration // 60}h {session.duration % 60}m" if session.duration >= 60 else f"{session.duration}m"
        })
    
    # Check for unread admin responses
    unread_count = SupportMessage.objects.filter(
        recipient=user,
        is_read=False
    ).count()
    
    # Count pending and resolved messages for stats
    pending_count = SupportMessage.objects.filter(
        sender=user,
        is_resolved=False
    ).count()
    
    resolved_count = SupportMessage.objects.filter(
        sender=user,
        is_resolved=True
    ).count()
    
    context = {
        'support_messages': user_messages,
        'study_sessions': study_sessions,
        'session_subjects': session_subjects,
        'unread_count': unread_count,
        'pending_count': pending_count,
        'resolved_count': resolved_count,
    }
    
    return render(request, 'core/support.html', context)


@login_required
@require_POST
def send_support_message(request):
    """Send a support message from user to admin"""
    try:
        data = json.loads(request.body)
        message_type = data.get('message_type', 'general')
        subject = data.get('subject', '')
        content = data.get('content', '').strip()
        session_id = data.get('session_id')
        requested_duration = data.get('requested_duration')
        
        if not content:
            return JsonResponse({'error': 'Message content is required'}, status=400)
        
        # Get the first superuser as recipient
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            return JsonResponse({'error': 'No admin available'}, status=400)
        
        # Get study session if this is a time correction request
        study_session = None
        if message_type == 'time_correction' and session_id:
            try:
                study_session = StudySession.objects.get(id=session_id, user=request.user)
            except StudySession.DoesNotExist:
                return JsonResponse({'error': 'Study session not found'}, status=404)
        
        message = SupportMessage.objects.create(
            sender=request.user,
            recipient=admin,
            message_type=message_type,
            subject=subject,
            content=content,
            study_session=study_session,
            requested_duration=requested_duration if message_type == 'time_correction' else None
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'message': 'Message sent successfully!'
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_user_messages(request):
    """Get all messages for the current user"""
    try:
        user = request.user
        user_messages = SupportMessage.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        ).order_by('-created_at')
        
        messages_data = []
        for msg in user_messages:
            messages_data.append({
                'id': msg.id,
                'sender': msg.sender.username,
                'recipient': msg.recipient.username,
                'message_type': msg.message_type,
                'subject': msg.subject,
                'content': msg.content,
                'is_from_user': msg.sender == user,
                'admin_response': msg.admin_response,
                'is_resolved': msg.is_resolved,
                'created_at': msg.created_at.strftime('%b %d, %Y at %I:%M %p'),
                'responded_at': msg.responded_at.strftime('%b %d, %Y at %I:%M %p') if msg.responded_at else None,
            })
        
        return JsonResponse({'success': True, 'messages': messages_data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# ADMIN MESSAGE MANAGEMENT VIEWS
# ========================================

@login_required
@superuser_required
def admin_messages_view(request):
    """Admin view for managing support messages"""
    # Get all support messages
    all_messages = SupportMessage.objects.all().order_by('-created_at')
    
    # Unresolved messages
    unresolved = all_messages.filter(is_resolved=False)
    
    # Group by message type
    time_corrections = unresolved.filter(message_type='time_correction')
    general_messages = unresolved.filter(message_type='general')
    bug_reports = unresolved.filter(message_type='bug_report')
    feedback = unresolved.filter(message_type='feedback')
    
    # Resolved messages
    resolved = all_messages.filter(is_resolved=True)
    
    context = {
        'all_messages': all_messages,
        'unresolved': unresolved,
        'time_corrections': time_corrections,
        'general_messages': general_messages,
        'bug_reports': bug_reports,
        'feedback': feedback,
        'resolved': resolved,
        'unresolved_count': unresolved.count(),
    }
    
    return render(request, 'core/admin_messages.html', context)


@login_required
@superuser_required
@require_POST
def admin_respond_message(request):
    """Admin responds to a support message"""
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        response = data.get('response', '').strip()
        mark_resolved = data.get('mark_resolved', True)
        
        if not message_id:
            return JsonResponse({'error': 'Message ID is required'}, status=400)
        
        if not response:
            return JsonResponse({'error': 'Response is required'}, status=400)
        
        message = SupportMessage.objects.get(id=message_id)
        message.admin_response = response
        message.responded_at = timezone.now()
        message.is_resolved = mark_resolved
        message.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Response sent successfully!'
        })
    
    except SupportMessage.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@superuser_required
@require_POST
def admin_approve_feedback(request):
    """Admin approves feedback to show on login page"""
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        approve = data.get('approve', True)
        
        if not message_id:
            return JsonResponse({'error': 'Message ID is required'}, status=400)
        
        message = SupportMessage.objects.get(id=message_id)
        
        if message.message_type != 'feedback':
            return JsonResponse({'error': 'Only feedback messages can be approved'}, status=400)
        
        message.is_approved_feedback = approve
        message.save()
        
        action = 'approved' if approve else 'unapproved'
        return JsonResponse({
            'success': True,
            'message': f'Feedback {action} successfully!'
        })
    
    except SupportMessage.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# ADMIN STUDY SESSION MANAGEMENT VIEWS
# ========================================

@login_required
@superuser_required
def admin_study_sessions_view(request):
    """Admin view for managing all study sessions"""
    # Get all study sessions grouped by user
    all_sessions = StudySession.objects.all().order_by('-date', '-created_at')
    
    # Get filter parameters
    user_filter = request.GET.get('user')
    subject_filter = request.GET.get('subject')
    date_filter = request.GET.get('date')
    
    if user_filter:
        all_sessions = all_sessions.filter(user__username__icontains=user_filter)
    if subject_filter:
        all_sessions = all_sessions.filter(subject__icontains=subject_filter)
    if date_filter:
        all_sessions = all_sessions.filter(date=date_filter)
    
    # Get all users and subjects for filters
    all_users = User.objects.all().order_by('username')
    all_subjects = StudySession.objects.values_list('subject', flat=True).distinct()
    
    context = {
        'sessions': all_sessions[:100],  # Limit to 100 for performance
        'all_users': all_users,
        'all_subjects': all_subjects,
        'user_filter': user_filter,
        'subject_filter': subject_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'core/admin_study_sessions.html', context)


@login_required
@superuser_required
@require_POST
def admin_edit_session(request):
    """Admin edits a study session duration"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        new_duration = data.get('duration')
        new_subject = data.get('subject')
        
        if not session_id:
            return JsonResponse({'error': 'Session ID is required'}, status=400)
        
        session = StudySession.objects.get(id=session_id)
        
        if new_duration is not None:
            session.duration = int(new_duration)
        if new_subject:
            session.subject = new_subject
        
        session.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Session updated successfully!'
        })
    
    except StudySession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@superuser_required
@require_POST
def admin_delete_session(request):
    """Admin deletes a study session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({'error': 'Session ID is required'}, status=400)
        
        session = StudySession.objects.get(id=session_id)
        username = session.user.username
        subject = session.subject
        duration = session.duration
        session.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Deleted {duration}min {subject} session for {username}'
        })
    
    except StudySession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)