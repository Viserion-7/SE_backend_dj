"""
Quick script to test email sending functionality.
Run this script directly to test email configuration:

python manage.py shell < tasks/tests/test_send_email.py
"""

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from tasks.models import Task, Category, Reminder
from tasks.utils import send_task_reminder, check_and_send_reminders
from datetime import datetime, timedelta
from django.utils import timezone

def test_basic_email():
    """Test basic email functionality"""
    print("Testing basic email sending...")
    try:
        send_mail(
            'Test Email from TaskNinja',
            'This is a test email to verify the email configuration.',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],  # Send to yourself
            fail_silently=False,
        )
        print("✓ Basic email test successful!")
    except Exception as e:
        print(f"✗ Basic email test failed: {str(e)}")

def test_reminder_email():
    """Test reminder email functionality"""
    print("\nTesting reminder email...")
    try:
        # Create test user
        user, created = User.objects.get_or_create(
            username='testuser',
            email=settings.EMAIL_HOST_USER,  # Send to configured email
            defaults={'password': 'testpass123'}
        )
        
        # Create test category
        category, created = Category.objects.get_or_create(
            name='Test Category'
        )
        
        # Create test task
        task = Task.objects.create(
            user=user,
            title='Test Reminder Task',
            description='This is a test task to verify reminder emails',
            due_date=timezone.now() + timedelta(hours=1),
            priority='High',
            category=category
        )
        
        # Create immediate reminder
        reminder = Reminder.objects.create(
            task=task,
            remind_at=timezone.now()
        )
        
        # Send reminder
        success = send_task_reminder(reminder)
        if success:
            print("✓ Reminder email test successful!")
        else:
            print("✗ Reminder email test failed")
            
    except Exception as e:
        print(f"✗ Reminder email test failed: {str(e)}")

if __name__ == '__main__':
    print("Email Configuration:")
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"TLS: {settings.EMAIL_USE_TLS}")
    print(f"From: {settings.EMAIL_HOST_USER}")
    print("\nRunning tests...")
    
    test_basic_email()
    test_reminder_email()
