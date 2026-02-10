from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# Study Session Model
class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subject} - {self.duration} mins"
    
    @classmethod
    def get_today_total(cls, user):
        """Get total study time for today"""
        today = timezone.now().date()
        total = cls.objects.filter(user=user, date=today).aggregate(
            total=models.Sum('duration')
        )['total'] or 0
        return total
    
    @classmethod
    def get_weekly_data(cls, user):
        """Get study time for the last 7 days"""
        today = timezone.now().date()
        week_ago = today - timedelta(days=6)
        
        sessions = cls.objects.filter(
            user=user,
            date__gte=week_ago,
            date__lte=today
        )
        
        # Create dict for each day
        weekly_data = {}
        for i in range(7):
            date = week_ago + timedelta(days=i)
            weekly_data[date] = 0
        
        # Fill in actual data
        for session in sessions:
            if session.date in weekly_data:
                weekly_data[session.date] += session.duration
        
        return weekly_data
    
    @classmethod
    def get_monthly_data(cls, user):
        """Get study time for the last 30 days"""
        today = timezone.now().date()
        month_ago = today - timedelta(days=29)
        
        sessions = cls.objects.filter(
            user=user,
            date__gte=month_ago,
            date__lte=today
        )
        
        # Create dict for each day
        monthly_data = {}
        for i in range(30):
            date = month_ago + timedelta(days=i)
            monthly_data[date] = 0
        
        # Fill in actual data
        for session in sessions:
            if session.date in monthly_data:
                monthly_data[session.date] += session.duration
        
        return monthly_data
    
    @classmethod
    def get_study_streak(cls, user):
        """Calculate consecutive study days"""
        today = timezone.now().date()
        streak = 0
        current_date = today
        
        # Start from today and go backwards
        while True:
            has_studied = cls.objects.filter(user=user, date=current_date).exists()
            if has_studied:
                streak += 1
            else:
                # If this is today and no study yet, continue to yesterday
                # This gives a "grace period" for the current day
                if current_date == today:
                    current_date -= timedelta(days=1)
                    continue
                # If it's any past day without study, streak is broken
                else:
                    break
            
            # Move to previous day
            current_date -= timedelta(days=1)
        
        return streak
    
    @classmethod
    def get_highest_streak(cls, user):
        """Calculate the highest streak ever achieved by the user"""
        # Get all unique study dates for the user
        study_dates = cls.objects.filter(user=user).values_list('date', flat=True).distinct().order_by('date')
        
        if not study_dates:
            return 0
        
        study_dates = list(study_dates)
        max_streak = 1
        current_streak = 1
        
        # Iterate through dates and find longest consecutive streak
        for i in range(1, len(study_dates)):
            if study_dates[i] - study_dates[i-1] == timedelta(days=1):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak


# Assignment Model
class Assignment(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),  # Legacy status, maps to todo
    ]
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    subject = models.CharField(max_length=100, default='General')
    deadline = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.FloatField(default=0, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='low')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['deadline', '-created_at']
        
    def save(self, *args, **kwargs):
        """Override save to handle null deadlines"""
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.subject}"
    
    def days_remaining(self):
        """Calculate days remaining until deadline"""
        if not self.deadline:
            return None
        today = timezone.now().date()
        deadline_date = self.deadline.date() if hasattr(self.deadline, 'date') else self.deadline
        delta = deadline_date - today
        return delta.days
    
    def hours_remaining(self):
        """Calculate hours remaining until deadline"""
        if not self.deadline:
            return None
        now = timezone.now()
        delta = self.deadline - now
        hours = delta.total_seconds() / 3600
        return max(0, round(hours, 1))
    
    def calculate_urgency(self):
        """Auto-calculate urgency based on days remaining"""
        days = self.days_remaining()
        # Handle case where no deadline is set (returns None)
        if days is None:
            return 'low'  # No deadline = low urgency
        if days < 0:
            return 'high'
        elif days <= 3:
            return 'high'
        elif days <= 7:
            return 'medium'
        else:
            return 'low'
    
    def save(self, *args, **kwargs):
        """Auto-update urgency and estimated hours before saving"""
        self.urgency = self.calculate_urgency()
        # Auto-calculate estimated hours if not provided and deadline exists
        if not self.estimated_hours or self.estimated_hours == 0:
            hours_remaining = self.hours_remaining()
            if hours_remaining is not None:
                self.estimated_hours = hours_remaining
            else:
                # No deadline - set default estimated hours
                self.estimated_hours = 2.0  # Default to 2 hours for assignments without deadline
        super().save(*args, **kwargs)


# Subject Folder Model (for organizing notes)
class SubjectFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_folders')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    def note_count(self):
        """Count notes in this folder"""
        return self.quick_notes.count()


# Quick Note Model
class QuickNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quick_notes')
    subject_folder = models.ForeignKey(SubjectFolder, on_delete=models.CASCADE, related_name='quick_notes', null=True, blank=True)
    subject = models.CharField(max_length=100)  # Keep for backward compatibility
    title = models.CharField(max_length=200, default='Untitled Note')
    content = models.TextField(max_length=2000)  # Increased limit for better notes
    study_duration = models.IntegerField(help_text="Duration in minutes", null=True, blank=True)
    is_pinned = models.BooleanField(default=False)  # Pin feature
    pinned_at = models.DateTimeField(null=True, blank=True)  # Track when pinned for ordering
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-pinned_at', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


# Support Message Model (for user-admin communication)
class SupportMessage(models.Model):
    MESSAGE_TYPES = [
        ('general', 'General'),
        ('time_correction', 'Time Correction Request'),
        ('bug_report', 'Bug Report'),
        ('feedback', 'Feedback'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='general')
    subject = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    # For time correction requests
    study_session = models.ForeignKey(StudySession, on_delete=models.SET_NULL, null=True, blank=True, related_name='correction_requests')
    requested_duration = models.IntegerField(null=True, blank=True, help_text="Requested corrected duration in minutes")
    is_read = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    # For feedback approval (shows on login page)
    is_approved_feedback = models.BooleanField(default=False)
    admin_response = models.TextField(max_length=2000, blank=True, null=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} - {self.subject}"
