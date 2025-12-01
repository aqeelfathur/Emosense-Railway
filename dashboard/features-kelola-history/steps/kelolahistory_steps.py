from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


@given('I am logged in as admin')
def step_login_as_admin(context):
    """Login sebagai admin"""
    driver = context.browser
    base_url = context.base_url
    
    # Navigasi ke halaman login
    driver.get(f"{base_url}/auth/login")
    
    # Isi form login dengan kredensial admin
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    username_input.clear()
    username_input.send_keys("admin1")
    password_input.clear()
    password_input.send_keys("tes12345")
    
    # Submit form
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Tunggu redirect ke dashboard
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )


@given('I am on "{url}"')
@when('I am on "{url}"')
def step_navigate_to_url(context, url):
    """Navigasi ke URL tertentu"""
    driver = context.browser
    base_url = context.base_url
    driver.get(f"{base_url}{url}")
    time.sleep(1)


@given('I go to "{url}"')
@when('I go to "{url}"')
def step_go_to_url(context, url):
    """Navigasi ke URL tertentu"""
    driver = context.browser
    base_url = context.base_url
    driver.get(f"{base_url}{url}")
    time.sleep(1)


@given('I should see "{text}"')
@when('I should see "{text}"')
@then('I should see "{text}"')
def step_should_see_text(context, text):
    """Verifikasi teks muncul di halaman atau dalam alert/confirm"""
    driver = context.browser
    
    # Cek apakah ada JavaScript alert/confirm dengan text tersebut
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        if text.lower() in alert_text.lower():
            return  # Text ditemukan di alert, jangan dismiss alert
    except:
        pass  # Tidak ada alert, lanjut cek di halaman
    
    # Cek text di halaman HTML
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
        )
        assert element.is_displayed(), f"Text '{text}' tidak terlihat di halaman"
    except TimeoutException:
        raise AssertionError(f"Text '{text}' tidak ditemukan di halaman atau alert")


@when('I select "{action}" from row "{row_id}"')
def step_select_action_from_row(context, action, row_id):
    """Pilih aksi (lihat/hapus) dari row tertentu berdasarkan ID"""
    driver = context.browser
    
    try:
        # Cari row berdasarkan ID history (cari td dengan strong tag yang berisi ID)
        row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[.//strong[text()='{row_id}']]"))
        )
        
        # Cari tombol aksi dalam row tersebut
        if action.lower() == "lihat":
            # Tombol Lihat: <a class="btn btn-view">Lihat</a>
            button = row.find_element(By.XPATH, ".//a[contains(@class, 'btn-view') and contains(text(), 'Lihat')]")
        elif action.lower() == "hapus":
            # Tombol Hapus: <a class="btn btn-delete" onclick="return confirm(...)">Hapus</a>
            button = row.find_element(By.XPATH, ".//a[contains(@class, 'btn-delete') and contains(text(), 'Hapus')]")
        else:
            raise ValueError(f"Action '{action}' tidak dikenali")
        
        # Scroll ke elemen jika perlu
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.5)
        
        # Klik tombol
        button.click()
        time.sleep(1)
        
    except TimeoutException:
        raise AssertionError(f"Row dengan ID '{row_id}' tidak ditemukan")
    except Exception as e:
        raise AssertionError(f"Gagal melakukan aksi '{action}' pada row '{row_id}': {str(e)}")


@when('I select "{button_text}"')
def step_select_button(context, button_text):
    """Klik tombol berdasarkan text"""
    driver = context.browser
    
    try:
        # Cari tombol berdasarkan text
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                f"//button[contains(text(), '{button_text}')] | //a[contains(text(), '{button_text}')]"
            ))
        )
        
        # Scroll ke tombol
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.5)
        
        # Klik tombol
        button.click()
        time.sleep(1)
        
    except TimeoutException:
        raise AssertionError(f"Tombol '{button_text}' tidak ditemukan")


@when('I press "{button_text}"')
def step_press_button(context, button_text):
    """Tekan tombol dalam modal/dialog atau JavaScript confirm"""
    driver = context.browser
    
    try:
        # Cek apakah ada JavaScript alert/confirm
        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            
            if button_text.lower() in ["iya", "ya", "ok", "yes"]:
                alert.accept()  # Klik OK/Iya
            else:
                alert.dismiss()  # Klik Cancel/Tidak
            
            time.sleep(1)
            return
        except TimeoutException:
            pass  # Tidak ada alert, lanjut cek modal
        
        # Jika tidak ada alert, cari modal
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal"))
        )
        
        # Cari tombol dalam modal
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                f"//div[contains(@class, 'modal')]//button[contains(text(), '{button_text}')]"
            ))
        )
        
        # Klik tombol
        button.click()
        time.sleep(1)
        
        # Tunggu modal hilang jika tombol adalah "Iya"
        if button_text.lower() in ["iya", "ya", "ok"]:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "modal"))
            )
        
    except TimeoutException:
        raise AssertionError(f"Dialog atau tombol '{button_text}' tidak ditemukan")