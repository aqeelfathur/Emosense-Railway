from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.contrib.auth import get_user_model
from emotion.models import CekEmosi
from django.utils import timezone

User = get_user_model()

# -----------------------------------------------------
# DATA SETUP
# -----------------------------------------------------

@given('there is a test user "{username}" with password "{password}"')
def step_impl(context, username, password):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        try:
            user.role = "user"
        except:
            pass
        user.save()
    context.test_user = user
    context.test_password = password


@given('there is a sample analysis with id "{id_cek}" for user "{username}"')
def step_impl(context, id_cek, username):
    user = User.objects.get(username=username)
    obj, created = CekEmosi.objects.get_or_create(
        id_cek=id_cek,
        defaults={
            "user": user,
            "hasil_deteksi": "Senang",
            "detail_hasil": '{"Senang": 80, "Sedih": 5, "Marah": 5, "Takut": 5, "Netral": 5}',
            "confidence_score": 95.0,
            "tanggal": timezone.now(),
            "link_yt": "",
            "jumlah_comment": 0,
            "input_text": "Contoh teks analisis"
        }
    )
    context.sample_analysis = obj

# -----------------------------------------------------
# PAGE NAVIGATION + LOGIN
# -----------------------------------------------------

@given('I am on "{page_name}"')
def step_impl(context, page_name):
    mapping = {
        "halaman_history": "/history/riwayat/",
        "login": "/auth/login/",
    }

    url = mapping.get(page_name)
    if not url:
        raise AssertionError(f"Unknown page '{page_name}'")

    # 1️⃣ LOGIN DULU
    context.browser.get(context.base_url + mapping["login"])
    time.sleep(2)

    try:
        context.browser.find_element(By.NAME, "username").send_keys(context.test_user.username)
        context.browser.find_element(By.NAME, "password").send_keys(context.test_password)
        context.browser.find_element(By.NAME, "password").send_keys(Keys.ENTER)
        time.sleep(2)
    except:
        pass

    # 2️⃣ MASUK KE HALAMAN HISTORY
    context.browser.get(context.base_url + url)
    time.sleep(2)

# -----------------------------------------------------
# ASSERTIONS & INTERACTIONS
# -----------------------------------------------------

@then('I should see "{text}"')
def step_impl(context, text):
    body = context.browser.find_element(By.TAG_NAME, "body")
    if text not in body.text:
        raise AssertionError(
            f'Expected "{text}" but NOT FOUND.\nPage text:\n{body.text[:500]}'
        )


@when('I select "{item}" from "{list_name}"')
def step_impl(context, item, list_name):

    # Klik history card berdasarkan ID analisis
    card_xpath = f"//strong[contains(text(), '{context.sample_analysis.id_cek}')]/ancestor::div[@class='history-item']"
    card = context.browser.find_element(By.XPATH, card_xpath)
    context.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
    time.sleep(1)
    card.click()

    # Tunggu modal muncul
    WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
    )


@then('I should see the detail modal')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
    )
    modal = context.browser.find_element(By.CLASS_NAME, "modal-content")
    assert modal.is_displayed(), "Modal detail tidak muncul!"
    context.browser.execute_script("arguments[0].scrollIntoView({block: 'end'});", modal)
    time.sleep(3)

@when('I reload the page')
def step_impl(context):
    context.browser.refresh()
