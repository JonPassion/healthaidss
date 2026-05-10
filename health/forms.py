from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile, MedicalHistory, AutoReminder, Notification, EmergencyContact

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'icon_image', 'bio', 'phone', 'date_of_birth', 'address']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your address'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'icon_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            })
        }


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'diseases', 'chronic_diseases', 'medications', 'allergies', 'surgeries', 'family_history', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your previous medical diagnosis'
            }),
            'diseases': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List any diseases you have had'
            }),
            'chronic_diseases': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List any chronic conditions'
            }),
            'medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List current medications'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List known allergies'
            }),
            'surgeries': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List past surgeries'
            }),
            'family_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Family medical history'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes'
            })
        }


class AutoReminderForm(forms.ModelForm):
    class Meta:
        model = AutoReminder
        fields = ['title', 'description', 'reminder_type', 'frequency', 'reminder_time', 'reminder_date', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reminder title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description (optional)'
            }),
            'reminder_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reminder_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'reminder_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone', 'contact_type', 'specialty', 'address', 'notes', 'is_favorite']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number (e.g., +1234567890)'
            }),
            'contact_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'specialty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Doctor's specialty (optional)"
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Address or location (optional)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes (optional)'
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
