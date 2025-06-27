import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_search_form(browser, base_url):
    browser.get(base_url + '/en-gb?route=account/register')
    wait = WebDriverWait(browser, 5)
    assert wait.until(EC.title_is("Register Account")), "Заголовок неверный или отсуствует"
    assert browser.find_element(By.ID, "search"), "нет панели поиска"
    assert browser.find_element(By.ID, "logo"), "не загрузился логотип"
    assert wait.until(EC.visibility_of(browser.find_element(By.ID, "header-cart"))), "нет кнопки перехода в корзину"
    assert browser.find_element(By.CSS_SELECTOR,"[type='checkbox']"), "Нет переключаетеля"


