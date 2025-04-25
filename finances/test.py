import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting.settings')
django.setup()

print("Django configured successfully!")