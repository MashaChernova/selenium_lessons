from operator import truediv

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.mark.only
def test_login_admin(browser,base_url):
    browser.get(base_url + "/administration")
    wait = WebDriverWait(browser, 5)
    browser.find_element(By.NAME,"username").send_keys("user")
    browser.find_element(By.NAME, "password").send_keys("bitnami")
    browser.find_element(By.CSS_SELECTOR, "[type='submit']").click()
    assert wait.until(EC.element_to_be_clickable((By.ID, "nav-logout"))), "Отсутствует кнопка выхода. Вероятно, вход не выполнен"
    browser.find_element(By.ID, "nav-logout").click()
    assert wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='submit']"))), "Отсутствует кнопка входа. Вероятно, выход не выполнен"

@pytest.mark.only1
def test_add_product(browser,base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 15)
    wait.until(EC.title_is("Your Store"))
    assert  "0 item" in browser.find_elements(By.CSS_SELECTOR, "[type='button']")[1].text, "корзина изначально не пуста"
    browser.find_elements(By.CSS_SELECTOR,"[type='submit']")[0].click()
    product_description = browser.find_elements(By.CLASS_NAME,"description")[0].text
    browser.get(base_url + "/en-gb?route=checkout/cart")
    assert browser.find_element(By.CSS_SELECTOR,"#shopping-cart > div > table > tbody > tr > td.text-start.text-wrap > a").text in product_description, "Товар не добавился или добавился более одного раза"


@pytest.mark.only2
def test_change_currency_in_main_page(browser,base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 15)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#form-currency > div > a > i"))).click()
    browser.find_element(By.CSS_SELECTOR,"#form-currency > div > ul > li:nth-child(1)").click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#form-currency > div"),"€ Currency"))
    assert "€" in browser.find_element(By.CLASS_NAME,"description").text

@pytest.mark.only3
def test_change_currency_in_catalog(browser,base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 15)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#form-currency > div > a > i"))).click()
    browser.find_element(By.CSS_SELECTOR, "#form-currency > div > ul > li:nth-child(1)").click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#form-currency > div"), "€ Currency"))
    browser.get(base_url + "/catalog/desktops")
    assert "€" in browser.find_element(By.CLASS_NAME,"description").text