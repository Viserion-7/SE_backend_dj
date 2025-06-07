import os
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import Task, Reminder

def send_task_reminder(reminder):
    """
    Send an email reminder for a task
    """
    task = reminder.task
    user = task.user
    subject = f"Reminder: {task.title}"
    
    # Format the due date
    due_date = task.due_date.strftime("%B %d, %Y at %I:%M %p")
    
    # Create the email message
    message = f"""
    Hello {user.username},

    This is a reminder for your task: {task.title}
    Due date: {due_date}

    Task details:
    - Priority: {task.priority}
    - Category: {task.category.name if task.category else 'None'}
    - Description: {task.description or 'No description provided'}

    Please make sure to complete this task on time.

    Best regards,
    TaskNinja Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        # Mark reminder as sent
        reminder.sent = True
        reminder.save()
        return True
    except Exception as e:
        print(f"Failed to send email reminder: {str(e)}")
        return False

def check_and_send_reminders():
    """
    Check for due reminders and send them
    """
    # Get all unsent reminders that are due
    current_time = datetime.now()
    due_reminders = Reminder.objects.filter(
        sent=False,
        remind_at__lte=current_time
    ).select_related('task', 'task__user', 'task__category')

    for reminder in due_reminders:
        send_task_reminder(reminder)
