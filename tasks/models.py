from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    """
    Represents a category or tag for organizing tasks.
    Example: Work, Personal, Shopping, etc.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Represents a task created by a user.
    """
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Normal', 'Normal'),
        ('Low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Normal')
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name="tasks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Save the task first
        super().save(*args, **kwargs)

        # Default category assignment
        if self.categories.count() == 0:
            personal_category, _ = Category.objects.get_or_create(name="Personal")
            self.categories.add(personal_category)
            
        # Default reminders (30 mins, 2 hrs, 1 day at 8 AM, 3 days at 8 AM)
        reminder_times = [
            self.due_date - timedelta(minutes=30),
            self.due_date - timedelta(hours=2),
            self.due_date.replace(hour=8, minute=0, second=0, microsecond=0) - timedelta(days=1),
            self.due_date.replace(hour=8, minute=0, second=0, microsecond=0) - timedelta(days=3),
        ]

        # Create reminders if they don't already exist
        for remind_at in reminder_times:
            if remind_at > timezone.now():  # Only add future reminders
                Reminder.objects.get_or_create(task=self, remind_at=remind_at)


class SubTask(models.Model):
    """
    Represents a subtask under a main task.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    """
    Represents a reminder for a task.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.remind_at}"