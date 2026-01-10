"""
Script to add sample study session data for testing charts
Run: python manage.py shell < scripts/add_sample_data.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyflow.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import StudySession
from datetime import datetime, timedelta
import random

# Get the first user (or create one)
try:
    user = User.objects.first()
    if not user:
        print("No users found. Please create a user first.")
        sys.exit(1)
    
    print(f"Adding sample data for user: {user.username}")
    
    # Delete existing sessions to start fresh (optional)
    # StudySession.objects.filter(user=user).delete()
    
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'English']
    
    # Add data for last 30 days
    today = datetime.now().date()
    for i in range(30):
        date = today - timedelta(days=i)
        # Add 1-3 sessions per day
        num_sessions = random.randint(1, 3)
        for _ in range(num_sessions):
            subject = random.choice(subjects)
            duration = random.randint(15, 120)  # 15 to 120 minutes
            
            StudySession.objects.create(
                user=user,
                subject=subject,
                duration=duration,
                date=date
            )
    
    print(f"✅ Successfully added {StudySession.objects.filter(user=user).count()} study sessions")
    print("Charts should now display data!")
    
    # Show summary
    total_minutes = sum(s.duration for s in StudySession.objects.filter(user=user))
    print(f"Total study time: {total_minutes // 60} hours {total_minutes % 60} minutes")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
