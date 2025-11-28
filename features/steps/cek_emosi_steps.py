from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

@given('I am on "cek_emosi"')
def step_impl(context):
    context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    context.driver.get("http://127.0.0.1:8000/")  # pastikan server Django berjalan
    time.sleep(2)

@then('I should see "Analisis emosi dari komentar YouTube menggunakan AI"')
def step_impl(context):
    assert "Analisis emosi dari komentar YouTube menggunakan AI" in context.driver.page_source

@when('I fill in "{field_name}" with "{value}"')
def step_impl(context, field_name, value):
    elem = context.driver.find_element(By.NAME, field_name)
    elem.clear()
    elem.send_keys(value)
    time.sleep(1)

@then('the "{field_name}" field should contain "{expected_value}"')
def step_impl(context, field_name, expected_value):
    elem = context.driver.find_element(By.NAME, field_name)
    assert elem.get_attribute("value") == expected_value

@when('I press "Analisis Komentar"')
def step_impl(context):
    button = WebDriverWait(context.driver, 10).until(
    EC.element_to_be_clickable((By.ID, "analyzeYoutubeBtn"))
    )
    button.click()
    time.sleep(10)

@then('I should see "Hasil Analisis"')
def step_impl(context):
    assert "Hasil Analisis" in context.driver.page_source

@then('I should see "{text}" in the "{element_id}" element')
def step_impl(context, text, element_id):
    elem = context.driver.find_element(By.ID, element_id)
    assert text in elem.text

@then('the response should contain "Detail Skor Semua Emosi"')
def step_impl(context):
    assert "Detail Skor Semua Emosi" in context.driver.page_source

@then('I should see "Daftar Komentar & Emosi"')
def step_impl(context):
    section = WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.ID, "commentsSection"))
    )
    context.driver.execute_script("arguments[0].scrollIntoView(true);", section)
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "commentsSection"),
            "Daftar Komentar & Emosi"
        )
    )
    assert "Daftar Komentar & Emosi" in section.text
