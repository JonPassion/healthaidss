import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthaid.settings')
django.setup()

from django.core.management import call_command

print("Running makemigrations...")
call_command('makemigrations', 'health')

print("\nRunning migrate...")
call_command('migrate')

print("\nDone!")
