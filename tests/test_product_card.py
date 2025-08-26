import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from page_objects import ProductCurt

@pytest.mark.only
@pytest.mark.parametrize("product",
                         ['macbook',
                          'iphone',
                          'cameras/nikon-d300'],
                         ids=['macbook', 'iphone', 'camera Nicon'])
def test_search_form(browser, base_url, product):
    product_curt = ProductCurt(browser, base_url, product)
    assert product_curt.content(), "нет товара на странице"
    assert product_curt.add_to_cart(), "нет кнопки добавления товара в корзину"
    assert "$" in product_curt.price_in_curt("$"), "не указана цена"
    assert product_curt.foto(), "нет изображения товара"

