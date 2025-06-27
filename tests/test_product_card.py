import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.mark.parametrize("product",
                         ['macbook',
                          'iphone',
                          'cameras/nikon-d300'],
                         ids=['macbook', 'iphone', 'camera Nicon'])
def test_search_form(browser, base_url, product):
    browser.get(base_url + f"/en-gb/product/{product}")
    wait = WebDriverWait(browser, 5)
    assert wait.until(EC.element_to_be_clickable((By.ID, "content"))), "нет товара на странице"
    assert browser.find_element(By.ID, "logo"), "не загрузился логотип"
    assert wait.until(EC.element_to_be_clickable((By.ID, "button-cart"))), "нет кнопки добавления товара в корзину"
    assert wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "price-new"),"$")), "не указана цена"
    assert browser.find_element(By.CLASS_NAME, "col-sm"), "нет изображения товара"

