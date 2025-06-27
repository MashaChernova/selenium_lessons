import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_search_form(browser, base_url):
    browser.get(base_url + "/en-gb/catalog/desktops")
    wait = WebDriverWait(browser, 5)
    assert wait.until(EC.title_is("Desktops")), "страница не загрузилась"
    assert browser.find_element(By.CSS_SELECTOR, "[href$='tablet']"), "Отсутствует товар категории tablet"
    assert browser.find_element(By.ID, "carousel-banner-0"), "нет баннера брендов"
    assert browser.find_element(By.ID, "display-control"), "нет панели настройки отображения"
    assert browser.find_element(By.ID, "product-list"), "нет списка товаров"
    assert browser.find_element(By.CLASS_NAME, "pagination"), "нет кнопок пагинации"