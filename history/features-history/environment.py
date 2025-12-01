import os
import django
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# --- SESUAIKAN: ganti dengan settings modul project mu ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # <- ganti your_project.settings
django.setup()

def before_all(context):
    # setup webdriver (Chrome)
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.browser = webdriver.Chrome(service=service, options=options)

    # base url untuk selenium; asumsi kamu menjalankan `python manage.py runserver` di port 8000
    context.base_url = 'http://127.0.0.1:8000/'

def after_all(context):
    try:
        context.browser.quit()
    except Exception:
        pass
