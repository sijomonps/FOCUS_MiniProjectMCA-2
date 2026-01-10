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
        
        while True:
            has_studied = cls.objects.filter(user=user, date=current_date).exists()
            if has_studied:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                # If today has no study, don't count as broken yet
                if current_date == today:
                    current_date -= timedelta(days=1)
                    continue
                break
        
        return streak


# Assignment Model
class Assignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, default='General')
    deadline = models.DateTimeField()
    estimated_hours = models.FloatField(default=0, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='low')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['deadline', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.subject}"
    
    def days_remaining(self):
        """Calculate days remaining until deadline"""
        today = timezone.now().date()
        deadline_date = self.deadline.date() if hasattr(self.deadline, 'date') else self.deadline
        delta = deadline_date - today
        return delta.days
    
    def hours_remaining(self):
        """Calculate hours remaining until deadline"""
        now = timezone.now()
        delta = self.deadline - now
        hours = delta.total_seconds() / 3600
        return max(0, round(hours, 1))
    
    def calculate_urgency(self):
        """Auto-calculate urgency based on days remaining"""
        days = self.days_remaining()
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
        # Auto-calculate estimated hours if not provided
        if not self.estimated_hours or self.estimated_hours == 0:
            self.estimated_hours = self.hours_remaining()
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
