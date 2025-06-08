from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    category = models.ForeignKey(Category, related_name="tasks", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def create_default_reminders(self):
        """Create default reminders for the task"""
        reminder_times = [
            timedelta(minutes=30),          # 30 minutes before
            timedelta(hours=2),             # 2 hours before
            timedelta(days=1),              # 1 day before
            timedelta(days=3),              # 3 days before
        ]

        for time_delta in reminder_times:
            remind_at = self.due_date - time_delta
            if remind_at > timezone.now():
                Reminder.objects.create(
                    task=self,
                    remind_at=remind_at
                )

class SubTask(models.Model):
    """
    Represents a subtask or step within a main task.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255)
    minutes = models.IntegerField(default=30)  # Duration in minutes
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.task.title})"

    class Meta:
        ordering = ['created_at']

class Reminder(models.Model):
    """
    Represents a reminder for a task.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.remind_at}"

# Signals
@receiver(post_save, sender=Task)
def create_reminders(sender, instance, created, **kwargs):
    """Create reminders when a task is created"""
    if created:
        instance.create_default_reminders()

@receiver(post_save, sender=Task)
def sync_subtask_completion(sender, instance, **kwargs):
    """Complete all subtasks when main task is completed"""
    if instance.is_completed:
        instance.subtasks.all().update(is_completed=True)
