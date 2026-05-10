from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    icon_image = models.ImageField(upload_to='profile_icons/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class MedicalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_histories')
    diagnosis = models.TextField(help_text="Previous medical diagnosis")
    diseases = models.TextField(help_text="List of diseases you have had", blank=True)
    chronic_diseases = models.TextField(help_text="List of chronic conditions", blank=True)
    medications = models.TextField(help_text="Current medications", blank=True)
    allergies = models.TextField(help_text="Known allergies", blank=True)
    surgeries = models.TextField(help_text="Past surgeries", blank=True)
    family_history = models.TextField(help_text="Family medical history", blank=True)
    notes = models.TextField(blank=True, help_text="Additional notes")
    date_recorded = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Medical History - {self.date_recorded.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date_recorded']


class PatientCheckIn(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='check_ins')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    initial_symptoms = models.TextField(help_text="Symptoms that triggered the check-in")
    last_check_in_time = models.DateTimeField(auto_now=True)
    next_check_in_time = models.DateTimeField()
    check_in_count = models.IntegerField(default=0)
    responses = models.TextField(blank=True, help_text="Patient responses to check-ins")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Check-in - {self.status}"

    class Meta:
        ordering = ['-created_at']


class AutoReminder(models.Model):
    REMINDER_TYPE_CHOICES = [
        ('medication', 'Medication'),
        ('appointment', 'Appointment'),
        ('checkup', 'Check-up'),
        ('exercise', 'Exercise'),
        ('water', 'Water Intake'),
        ('other', 'Other'),
    ]
    
    FREQUENCY_CHOICES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES, default='other')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='once')
    reminder_time = models.TimeField()
    reminder_date = models.DateField(null=True, blank=True, help_text="Required for 'once' reminders")
    is_active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    next_send = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.title} - {self.reminder_time}"

    def save(self, *args, **kwargs):
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        if not self.next_send:
            # Calculate next send time based on frequency
            today = timezone.now().date()
            if self.reminder_date:
                next_date = self.reminder_date
            else:
                next_date = today
            
            # Combine date and time
            next_datetime = timezone.make_aware(
                datetime.combine(next_date, self.reminder_time)
            )
            
            # If the time has passed today and it's a recurring reminder, move to next occurrence
            if next_datetime < timezone.now():
                if self.frequency == 'daily':
                    next_datetime += timedelta(days=1)
                elif self.frequency == 'weekly':
                    next_datetime += timedelta(weeks=1)
                elif self.frequency == 'monthly':
                    next_datetime += timedelta(days=30)
            
            self.next_send = next_datetime
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['next_send']


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('appointment', 'Appointment'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
        ('info', 'Information'),
        ('success', 'Success'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.title}"

    class Meta:
        ordering = ['-created_at']


class EmergencyContact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('emergency', 'Emergency'),
        ('hospital', 'Hospital'),
        ('pharmacy', 'Pharmacy'),
        ('family', 'Family'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, help_text="Phone number to dial")
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default='other')
    specialty = models.CharField(max_length=200, blank=True, help_text="Doctor's specialty (for doctors)")
    address = models.TextField(blank=True, help_text="Address or location")
    notes = models.TextField(blank=True, help_text="Additional notes")
    is_favorite = models.BooleanField(default=False, help_text="Mark as favorite for quick access")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        ordering = ['-is_favorite', 'name']
