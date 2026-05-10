from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm, UserForm, MedicalHistoryForm, AutoReminderForm, EmergencyContactForm
from .models import UserProfile, MedicalHistory, PatientCheckIn, AutoReminder, Notification, EmergencyContact
from django.utils import timezone
from datetime import timedelta
import json
import sys
import os

# Add the model directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model'))

# Model will be loaded lazily when needed
predict = None
map_symptoms = None
generate_medical_response = None
MODEL_AVAILABLE = None

@login_required
def home(request):
    """Home page - always redirect to login first"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def user_login(request):
    """Login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def user_register(request):
    """Registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    """Dashboard view for authenticated users"""
    from django.db import connection
    
    # Ensure profile exists
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_userprofile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_image VARCHAR(100),
                    icon_image VARCHAR(100),
                    bio VARCHAR(500),
                    phone VARCHAR(20),
                    date_of_birth DATE,
                    address VARCHAR(255),
                    created_at DATETIME,
                    updated_at DATETIME,
                    user_id INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Calculate actual counts with proper error handling
    medical_records_count = 0
    try:
        medical_records_count = MedicalHistory.objects.filter(user=request.user).count()
    except Exception:
        medical_records_count = 0
    
    active_reminders_count = 0
    try:
        active_reminders_count = AutoReminder.objects.filter(user=request.user, is_active=True).count()
    except Exception:
        active_reminders_count = 0
    
    unread_notifications_count = 0
    try:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    except Exception:
        unread_notifications_count = 0
    
    # Messages count (placeholder - can be implemented later)
    messages_count = 0
    
    # Upcoming appointments count (placeholder for future appointment system)
    upcoming_appointments_count = 0
    
    return render(request, 'home.html', {
        'user': request.user,
        'profile': profile,
        'unread_count': unread_notifications_count,
        'medical_records_count': medical_records_count,
        'active_reminders_count': active_reminders_count,
        'messages_count': messages_count,
        'upcoming_appointments_count': upcoming_appointments_count
    })


@login_required
def chat_interface(request):
    """Chat interface placeholder"""
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except Exception:
        profile = None
    return render(request, 'health/home.html', {
        'user': request.user,
        'profile': profile,
        'unread_count': 0
    })


@login_required
def book_appointment(request):
    """Book appointment placeholder"""
    return render(request, 'home.html', {'user': request.user})


@login_required
def medical_records_list(request):
    """Medical records view - same as medical history"""
    from django.db import connection
    
    # Create table if it doesn't exist
    try:
        MedicalHistory.objects.filter(user=request.user).first()
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_medicalhistory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    diagnosis TEXT,
                    diseases TEXT,
                    chronic_diseases TEXT,
                    medications TEXT,
                    allergies TEXT,
                    surgeries TEXT,
                    family_history TEXT,
                    notes TEXT,
                    date_recorded DATETIME,
                    last_updated DATETIME,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
    
    histories = MedicalHistory.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.user = request.user
            medical_history.save()
            messages.success(request, 'Medical record added successfully!')
            return redirect('medical_records_list')
    else:
        form = MedicalHistoryForm()
    
    return render(request, 'medical_records_list.html', {
        'form': form,
        'histories': histories
    })


@login_required
def profile(request):
    """Profile view - display and edit user profile"""
    from django.db import connection
    
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except Exception as e:
        # If table doesn't exist, create it manually
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_userprofile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_image VARCHAR(100),
                    icon_image VARCHAR(100),
                    bio VARCHAR(500),
                    phone VARCHAR(20),
                    date_of_birth DATE,
                    address VARCHAR(255),
                    created_at DATETIME,
                    updated_at DATETIME,
                    user_id INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    })


@login_required
def notifications(request):
    """Notifications view - display user notifications"""
    from django.db import connection
    
    # Create table if it doesn't exist
    try:
        Notification.objects.filter(user=request.user).first()
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_notification (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200),
                    message TEXT,
                    notification_type VARCHAR(20),
                    is_read BOOLEAN,
                    created_at DATETIME,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
    
    notifications_list = Notification.objects.filter(user=request.user)
    unread_count = notifications_list.filter(is_read=False).count()
    
    return render(request, 'notifications.html', {
        'notifications': notifications_list,
        'unread_count': unread_count
    })


def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications_')


def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read!')
    return redirect('notifications_')


def reminders(request):
    """Reminders view - create and manage auto reminders"""
    from django.db import connection
    
    # Create table if it doesn't exist
    try:
        AutoReminder.objects.filter(user=request.user).first()
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_autoreminder (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200),
                    description TEXT,
                    reminder_type VARCHAR(20),
                    frequency VARCHAR(20),
                    reminder_time VARCHAR(20),
                    reminder_date DATE,
                    is_active BOOLEAN,
                    last_sent DATETIME,
                    next_send DATETIME,
                    created_at DATETIME,
                    updated_at DATETIME,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
    
    reminders_list = AutoReminder.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = AutoReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, 'Reminder created successfully!')
            return redirect('reminders')
    else:
        form = AutoReminderForm()
    
    return render(request, 'reminders.html', {
        'form': form,
        'reminders': reminders_list
    })


def toggle_reminder(request, reminder_id):
    """Toggle reminder active status"""
    reminder = AutoReminder.objects.get(id=reminder_id, user=request.user)
    reminder.is_active = not reminder.is_active
    reminder.save()
    status = 'activated' if reminder.is_active else 'deactivated'
    messages.success(request, f'Reminder {status} successfully!')
    return redirect('reminders')


@login_required
def delete_reminder(request, reminder_id):
    """Delete a reminder"""
    reminder = AutoReminder.objects.get(id=reminder_id, user=request.user)
    reminder.delete()
    messages.success(request, 'Reminder deleted successfully!')
    return redirect('reminders')


def emergency_contacts(request):
    """Emergency contacts view - manage doctors and emergency numbers"""
    from django.db import connection
    
    # Create table if it doesn't exist
    try:
        EmergencyContact.objects.filter(user=request.user).first()
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_emergencycontact (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(200),
                    phone VARCHAR(20),
                    contact_type VARCHAR(20),
                    specialty VARCHAR(200),
                    address TEXT,
                    notes TEXT,
                    is_favorite BOOLEAN,
                    created_at DATETIME,
                    updated_at DATETIME,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
    
    contacts_list = EmergencyContact.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Emergency contact added successfully!')
            return redirect('emergency_contacts')
    else:
        form = EmergencyContactForm()
    
    return render(request, 'emergency_contacts.html', {
        'form': form,
        'contacts': contacts_list
    })


def toggle_favorite_contact(request, contact_id):
    """Toggle favorite status of emergency contact"""
    contact = EmergencyContact.objects.get(id=contact_id, user=request.user)
    contact.is_favorite = not contact.is_favorite
    contact.save()
    return redirect('emergency_contacts')


@login_required
def delete_emergency_contact(request, contact_id):
    """Delete an emergency contact"""
    contact = EmergencyContact.objects.get(id=contact_id, user=request.user)
    contact.delete()
    messages.success(request, 'Emergency contact deleted successfully!')
    return redirect('emergency_contacts')


@login_required
def link_whatsapp(request):
    """WhatsApp link placeholder"""
    return render(request, 'home.html', {'user': request.user})


@login_required
def check_in_response(request):
    """Handle patient check-in responses"""
    from django.db import connection
    
    # Create table if it doesn't exist
    try:
        PatientCheckIn.objects.filter(user=request.user).first()
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_patientcheckin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status VARCHAR(20),
                    initial_symptoms TEXT,
                    last_check_in_time DATETIME,
                    next_check_in_time DATETIME,
                    check_in_count INTEGER,
                    responses TEXT,
                    created_at DATETIME,
                    completed_at DATETIME,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
    
    active_check_in = PatientCheckIn.objects.filter(user=request.user, status='active').first()
    
    if request.method == 'POST':
        response = request.POST.get('response', '').lower()
        
        if active_check_in:
            # Update responses
            if active_check_in.responses:
                active_check_in.responses += f"\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}]: {response}"
            else:
                active_check_in.responses = f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}]: {response}"
            
            # Check if patient says they're okay
            if 'ok' in response or 'better' in response or 'fine' in response or 'good' in response:
                active_check_in.status = 'completed'
                active_check_in.completed_at = timezone.now()
                messages.success(request, 'Great to hear you\'re feeling better! Check-ins have been stopped.')
            else:
                # Schedule next check-in in 12 hours
                active_check_in.next_check_in_time = timezone.now() + timedelta(hours=12)
                active_check_in.check_in_count += 1
                active_check_in.last_check_in_time = timezone.now()
                messages.info(request, 'We\'ll check in with you again in 12 hours.')
            
            active_check_in.save()
        else:
            messages.error(request, 'No active check-in found.')
        
        return redirect('check_in_response')
    
    return render(request, 'check_in.html', {
        'active_check_in': active_check_in
    })


def check_in_history(request):
    """Display patient check-in history"""
    from django.db import connection
    
    # Create table if it doesn't exist
    try:
        PatientCheckIn.objects.filter(user=request.user).first()
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_patientcheckin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status VARCHAR(20),
                    initial_symptoms TEXT,
                    last_check_in_time DATETIME,
                    next_check_in_time DATETIME,
                    check_in_count INTEGER,
                    responses TEXT,
                    created_at DATETIME,
                    completed_at DATETIME,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
    
    check_ins = PatientCheckIn.objects.filter(user=request.user)
    
    return render(request, 'check_in_history.html', {
        'check_ins': check_ins
    })

@csrf_exempt
@require_http_methods(["POST"])
def analyze_symptoms(request):
    """API endpoint to analyze symptoms and return predictions"""
    global predict, map_symptoms, generate_medical_response, MODEL_AVAILABLE
    
    # Lazy load the model only when button is clicked
    if MODEL_AVAILABLE is None:
        try:
            from main import predict as _predict
            from utils.symptom_mapper import map_symptoms as _map_symptoms
            from utils.llm_engine import generate_medical_response as _generate_medical_response
            predict = _predict
            map_symptoms = _map_symptoms
            generate_medical_response = _generate_medical_response
            MODEL_AVAILABLE = True
        except Exception as e:
            MODEL_AVAILABLE = False
            import traceback
            return JsonResponse({
                'error': f'AI model load failed: {str(e)}',
                'traceback': traceback.format_exc()
            }, status=500)
    
    if not MODEL_AVAILABLE:
        return JsonResponse({
            'error': 'AI model is not available'
        }, status=500)
    
    try:
        data = json.loads(request.body)
        user_text = data.get('symptoms', '')
        
        if not user_text:
            return JsonResponse({
                'error': 'No symptoms provided'
            }, status=400)
        
        # Map symptoms using the model's symptom mapper
        mapped_symptoms = map_symptoms(user_text)
        
        if not mapped_symptoms:
            return JsonResponse({
                'error': 'No recognizable symptoms detected',
                'suggestion': 'Please describe your symptoms more clearly'
            }, status=400)
        
        # Get predictions from the model
        predictions = predict(mapped_symptoms)
        
        # Fetch user's medical history from database
        medical_history_context = ""
        try:
            if request.user.is_authenticated:
                histories = MedicalHistory.objects.filter(user=request.user).order_by('-date_recorded')
                if histories.exists():
                    latest_history = histories.first()
                    medical_history_context = f"""
User's Medical History:
- Diagnosis: {latest_history.diagnosis or 'Not recorded'}
- Diseases: {latest_history.diseases or 'Not recorded'}
- Chronic Diseases: {latest_history.chronic_diseases or 'Not recorded'}
- Current Medications: {latest_history.medications or 'Not recorded'}
- Allergies: {latest_history.allergies or 'Not recorded'}
- Surgeries: {latest_history.surgeries or 'Not recorded'}
- Family History: {latest_history.family_history or 'Not recorded'}
"""
        except Exception as e:
            medical_history_context = "No medical history available"
        
        # Generate AI response with medical history context
        try:
            ai_response = generate_medical_response(user_text, predictions, medical_history_context)
        except Exception as e:
            ai_response = f"⚠️ LLM Error: {str(e)}"
        
        # Auto-start check-in if user is authenticated
        if request.user.is_authenticated:
            try:
                # Check if there's already an active check-in
                active_check_in = PatientCheckIn.objects.filter(user=request.user, status='active').first()
                if not active_check_in:
                    # Create new check-in
                    check_in = PatientCheckIn.objects.create(
                        user=request.user,
                        status='active',
                        initial_symptoms=user_text,
                        next_check_in_time=timezone.now() + timedelta(hours=12),
                        check_in_count=0
                    )
            except Exception:
                pass  # Don't fail the analysis if check-in creation fails
        
        return JsonResponse({
            'success': True,
            'mapped_symptoms': mapped_symptoms,
            'predictions': [
                {'disease': disease, 'confidence': confidence}
                for disease, confidence in predictions
            ],
            'ai_response': ai_response,
            'medical_history_used': bool(medical_history_context and medical_history_context != "No medical history available"),
            'check_in_started': True
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Processing error: {str(e)}'
        }, status=500)


def start_check_in(request):
    """Start a new check-in process"""
    from django.db import connection
    
    # Create table if it doesn't exist
    try:
        PatientCheckIn.objects.filter(user=request.user).first()
    except Exception:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_patientcheckin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status VARCHAR(20),
                    initial_symptoms TEXT,
                    last_check_in_time DATETIME,
                    next_check_in_time DATETIME,
                    check_in_count INTEGER,
                    responses TEXT,
                    created_at DATETIME,
                    completed_at DATETIME,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id)
                )
            ''')
    
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '')
        
        # Check if there's already an active check-in
        active_check_in = PatientCheckIn.objects.filter(user=request.user, status='active').first()
        if active_check_in:
            messages.info(request, 'You already have an active check-in.')
            return redirect('check_in_response')
        
        # Create new check-in
        check_in = PatientCheckIn.objects.create(
            user=request.user,
            status='active',
            initial_symptoms=symptoms,
            next_check_in_time=timezone.now() + timedelta(hours=12),
            check_in_count=0
        )
        
        messages.success(request, 'Check-in started! We\'ll check in with you in 12 hours.')
        return redirect('check_in_response')
    
    return render(request, 'start_check_in.html')
