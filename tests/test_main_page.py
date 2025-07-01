import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_search_form(browser, base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.title_is("Your Store"))
    assert browser.find_element(By.ID, "search"), "нет панели поиска"
    assert browser.find_element(By.ID, "logo"), "не загрузился логотип"

def test_no_money_to_start(browser, base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.title_is("Your Store"))
    assert "0.00" in browser.find_element(By.ID, "header-cart").text, "Возможно, конзина не пуста"

def test_head(browser, base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.title_is("Your Store"))
    assert "$" in browser.find_element(By.ID, "form-currency").text, "Неверная валюта по умолчанию"

@pytest.mark.parametrize("href_value, currency_symbol",
                         [("EUR","€"),
                          ("USD","$"),
                          ("GBP","£")],
                         ids=["euro", "dollar", "pound"])
def test_change_currency(browser, base_url, href_value, currency_symbol):
    browser.get(base_url)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.title_is("Your Store"))
    change_currency_button = browser.find_element(By.CSS_SELECTOR, f"[href = '#']")
    change_currency_button.click()
    browser.find_element(By.CSS_SELECTOR, f"[href = {href_value}]").click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, f"[href = '#']"),text_=currency_symbol))
    assert currency_symbol in browser.find_element(By.ID, "header-cart").text, "Валюта не отображается на кнопке корзины"