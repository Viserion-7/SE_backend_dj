# Email Reminder System Setup

## Configuration

1. Update your environment variables or create a `.env` file:
```
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Note: For Gmail, you need to use an App Password:
1. Go to your Google Account settings
2. Enable 2-Step Verification if not already enabled
3. Go to Security → App passwords
4. Create a new app password for your application

## Testing the System

1. Create a task with reminders:
   - When you create a task, reminders are automatically set for:
     - 30 minutes before due time
     - 2 hours before due time
     - 1 day before at 8 AM
     - 3 days before at 8 AM

2. Check reminder status:
```bash
# Using API endpoint
curl -X GET http://localhost:8000/api/tasks/reminder_status/

# Or use the admin interface at:
http://localhost:8000/admin/tasks/reminder/
```

3. Manually trigger reminder checks:
```bash
# Using Django management command
python manage.py send_reminders

# Or using API endpoint
curl -X POST http://localhost:8000/api/tasks/check_reminders/
```

## Setting Up Automatic Reminder Checks

Add to your crontab (Unix/Linux):
```bash
# Check every 5 minutes
*/5 * * * * cd /path/to/project && python manage.py send_reminders

# Or check every hour
0 * * * * cd /path/to/project && python manage.py send_reminders
```

For Windows, use Task Scheduler to run:
```batch
python manage.py send_reminders
```

## Email Template

Reminders will include:
- Task title and description
- Due date and time
- Priority level
- Category (if set)
- Task status

## Troubleshooting

1. Check email settings:
```python
from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'Test Message',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

2. Common issues:
   - Gmail blocking "less secure app access" → Use App Password
   - Incorrect email credentials → Check environment variables
   - Network issues → Check firewall settings
   - SMTP connection timeout → Check network connectivity

3. Viewing failed reminders:
   - Check Django error logs
   - Look for unsent reminders in admin interface
   - Check reminder_status API endpoint

## Reminder Rules

1. Reminders are created automatically when:
   - A new task is created
   - A task's due date is updated

2. Reminders are sent only if:
   - The reminder time is in the future
   - The reminder hasn't been sent yet
   - The task isn't marked as completed

3. Reminder times are based on user's timezone (set in settings.py)

4. Failed reminders will be retried on the next check cycle
