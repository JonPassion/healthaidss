from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from health.models import AutoReminder
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Send auto reminders that are due'

    def handle(self, *args, **options):
        now = timezone.now()
        reminders = AutoReminder.objects.filter(
            is_active=True,
            next_send__lte=now
        )

        sent_count = 0
        for reminder in reminders:
            # Here you would implement the actual sending logic
            # For example: send email, SMS, push notification, etc.
            # For now, we'll just mark it as sent and update the next send time
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Sending reminder: {reminder.title} to {reminder.user.username}'
                )
            )
            
            # Update last_sent time
            reminder.last_sent = now
            
            # Calculate next send time based on frequency
            if reminder.frequency == 'once':
                reminder.is_active = False
            elif reminder.frequency == 'daily':
                reminder.next_send = now + timedelta(days=1)
            elif reminder.frequency == 'weekly':
                reminder.next_send = now + timedelta(weeks=1)
            elif reminder.frequency == 'monthly':
                reminder.next_send = now + timedelta(days=30)
            
            reminder.save()
            sent_count += 1

        if sent_count == 0:
            self.stdout.write(self.style.WARNING('No reminders to send.'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully sent {sent_count} reminder(s).')
            )
