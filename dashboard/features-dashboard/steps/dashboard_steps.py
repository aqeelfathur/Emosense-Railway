from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@given("browser terbuka")
def step_impl(context):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  

    context.browser = webdriver.Chrome(options=options)
    context.browser.maximize_window()
    context.wait = WebDriverWait(context.browser, 10)


@given('I go to "{url}"')
def step_impl(context, url):
    context.browser.get(url)


@given("admin sudah login")
def step_impl(context):
    """Login admin jika belum login"""
    current_url = context.browser.current_url
    
    # Cek apakah sudah di dashboard (sudah login)
    if "/dashboard" in current_url:
        try:
            # Cek apakah ada elemen yang hanya muncul saat sudah login
            context.browser.find_element(By.XPATH, "//*[contains(text(), 'Selamat Datang')]")
            print("✅ Sudah login, skip proses login")
            return  # Sudah login, skip
        except:
            pass  # Belum login, lanjut ke proses login
    
    # Jika belum login, redirect ke halaman login
    if "/login" not in current_url:
        context.browser.get("http://127.0.0.1:8000/auth/login")
    
    print("🔐 Melakukan login...")
    
    # Tunggu form login muncul
    username_field = context.wait.until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Isi username & password
    username_field.clear()
    username_field.send_keys("admin1")
    
    password_field = context.browser.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys("tes12345")
    
    # Klik tombol login
    login_button = context.browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Tunggu redirect ke dashboard
    context.wait.until(EC.url_contains("/dashboard"))
    
    # Tunggu sampai dashboard tampil
    context.wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Selamat Datang')]"))
    )
    
    print("✅ Login berhasil!")


@then('I should see "{text}"')
def step_impl(context, text):
    """Verifikasi text muncul di halaman"""
    try:
        element = context.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{text}')]")
            )
        )
        assert element.is_displayed(), f"Text '{text}' tidak terlihat di halaman"
        print(f"✓ Found: {text}")
    except TimeoutException:
        raise AssertionError(f"Text '{text}' tidak ditemukan di halaman")