from django.core.management.base import BaseCommand
from tasks.utils import check_and_send_reminders
from django.utils import timezone

class Command(BaseCommand):
    help = 'Send email reminders for tasks'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS(f'Starting to send reminders at {timezone.now()}')
        )
        
        try:
            check_and_send_reminders()
            self.stdout.write(
                self.style.SUCCESS('Successfully sent reminders')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending reminders: {str(e)}')
            )
