import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_search_form(browser, base_url):
    browser.get(base_url + "/administration")
    wait = WebDriverWait(browser, 5)
    assert wait.until(EC.title_is("Administration")), "Заголовок таблицы отличается от ожидаемого"
    assert browser.find_element(By.CSS_SELECTOR,"[src='view/image/logo.png']"), "Отсутствует логотип"
    assert browser.find_element(By.NAME, "username"), "Нет поля ввода имени пользователя"
    assert browser.find_element(By.NAME, "password"), "Нет поля ввода пароля"
    assert browser.find_element(By.CLASS_NAME, "text-end"), "Нет кнопки входа"