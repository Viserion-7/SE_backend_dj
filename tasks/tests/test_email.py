import os
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from ..models import Task, Reminder, Category
from ..utils import send_task_reminder, check_and_send_reminders

class EmailReminderTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test category
        self.category = Category.objects.create(name='Test Category')
        
        # Create a task due tomorrow at 9 AM
        tomorrow = timezone.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            due_date=tomorrow,
            priority='High',
            category=self.category
        )
        
        # Create a reminder
        self.reminder = Reminder.objects.create(
            task=self.task,
            remind_at=timezone.now() + timedelta(minutes=5)
        )

    def test_send_single_reminder(self):
        """Test sending a single reminder"""
        success = send_task_reminder(self.reminder)
        self.assertTrue(success)
        self.assertEqual(len(mail.outbox), 1)
        
        # Check email content
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Reminder: {self.task.title}")
        self.assertIn(self.task.title, email.body)
        self.assertIn(self.user.username, email.body)
        self.assertIn(self.task.priority, email.body)
        self.assertIn(self.category.name, email.body)

    def test_check_and_send_reminders(self):
        """Test the reminder check and send function"""
        # Create multiple reminders
        Reminder.objects.create(
            task=self.task,
            remind_at=timezone.now() - timedelta(minutes=5)  # Past reminder
        )
        Reminder.objects.create(
            task=self.task,
            remind_at=timezone.now() + timedelta(hours=1)  # Future reminder
        )
        
        # Run the check
        check_and_send_reminders()
        
        # Should only send the past reminder
        self.assertEqual(len(mail.outbox), 1)
        
        # Check if the reminder was marked as sent
        past_reminder = Reminder.objects.get(remind_at__lt=timezone.now())
        self.assertTrue(past_reminder.sent)

    def test_reminder_creation_on_task_save(self):
        """Test that reminders are automatically created when a task is saved"""
        # Count initial reminders
        initial_count = Reminder.objects.count()
        
        # Create a new task
        new_task = Task.objects.create(
            user=self.user,
            title='Another Test Task',
            description='Another Test Description',
            due_date=timezone.now() + timedelta(days=2),
            priority='Normal'
        )
        
        # Should create 4 reminders (30min, 2h, 1d, 3d before)
        self.assertEqual(Reminder.objects.count(), initial_count + 4)
        
        # Check reminder times
        reminders = Reminder.objects.filter(task=new_task)
        self.assertTrue(any(r.remind_at == new_task.due_date - timedelta(minutes=30) for r in reminders))
        self.assertTrue(any(r.remind_at == new_task.due_date - timedelta(hours=2) for r in reminders))

if __name__ == '__main__':
    # Quick manual test
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'tasks.tests.test_email'])
