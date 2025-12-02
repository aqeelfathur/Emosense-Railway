import os
import sys
import traceback

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    print("🔄 Loading Django application...", flush=True)
    application = get_wsgi_application()
    print("✅ Django application loaded successfully!", flush=True)
except Exception as e:
    print(f"❌ FATAL ERROR loading Django application:", flush=True)
    print(f"Error: {e}", flush=True)
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()
    raise