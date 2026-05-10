"""
WSGI config for healthaid project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthaid.settings')

application = get_wsgi_application()

# Pre-load AI models at startup for faster first request
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model'))
    from main import predict
    from utils.symptom_mapper import map_symptoms
    from utils.llm_engine import generate_medical_response
    print("AI models pre-loaded successfully")
except Exception as e:
    print(f"Warning: Could not pre-load AI models: {e}")
