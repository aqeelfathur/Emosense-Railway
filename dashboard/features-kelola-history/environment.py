from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def before_all(context):
    """Setup yang dijalankan sekali sebelum semua test"""
    # Konfigurasi Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment untuk headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    context.browser = webdriver.Chrome(service=service, options=chrome_options)
    context.browser.implicitly_wait(10)
    context.browser.maximize_window()
    
    # Set base URL aplikasi
    context.base_url = "http://127.0.0.1:8000/"  # Sesuaikan dengan URL aplikasi kamu


# def before_scenario(context, scenario):
#     """Setup yang dijalankan sebelum setiap scenario"""
#     # Clear cookies sebelum scenario baru
#     context.browser.delete_all_cookies()


# def after_scenario(context, scenario):
#     """Cleanup setelah setiap scenario"""
#     # Screenshot jika scenario gagal
#     if scenario.status == "failed":
#         screenshot_name = f"screenshot_{scenario.name.replace(' ', '_')}.png"
#         context.browser.save_screenshot(screenshot_name)
#         print(f"Screenshot saved: {screenshot_name}")


def after_all(context):
    """Cleanup yang dijalankan sekali setelah semua test"""
    # Tutup browser
    context.browser.quit()