from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chat/', views.chat_interface, name='chat_interface'),
    path('appointments/', views.book_appointment, name='book_appointment'),
    path('records/', views.medical_records_list, name='medical_records_list'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications_'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('reminders/', views.reminders, name='reminders'),
    path('reminders/toggle/<int:reminder_id>/', views.toggle_reminder, name='toggle_reminder'),
    path('reminders/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('emergency-contacts/', views.emergency_contacts, name='emergency_contacts'),
    path('emergency-contacts/toggle-favorite/<int:contact_id>/', views.toggle_favorite_contact, name='toggle_favorite_contact'),
    path('emergency-contacts/delete/<int:contact_id>/', views.delete_emergency_contact, name='delete_emergency_contact'),
    path('whatsapp/', views.link_whatsapp, name='link_whatsapp'),
    path('check-in/', views.check_in_response, name='check_in_response'),
    path('check-in/start/', views.start_check_in, name='start_check_in'),
    path('check-in-history/', views.check_in_history, name='check_in_history'),
    path('api/analyze/', views.analyze_symptoms, name='analyze_symptoms'),
]
