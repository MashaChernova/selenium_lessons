from operator import truediv

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from tests.page_objects import MainPage, AdminPage, CartPage, CatalogPage, AddProductPage


@pytest.mark.only
def test_login_admin(browser, base_url):
    admin_page = AdminPage(browser,base_url)
    admin_page.admin_login()
    assert admin_page.logout_button(), "Отсутствует кнопка выхода. Вероятно, вход не выполнен"
    admin_page.logout_button().click()
    assert admin_page.find_login_button(), "Отсутствует кнопка входа. Вероятно, выход не выполнен"


@pytest.mark.only1
def test_add_product_in_cart(browser, base_url):
    main_page = MainPage(browser, base_url)
    assert  "0 item" in main_page.header_cart_button().text, "корзина изначально не пуста"
    main_page.add_product()
    product_description = main_page.get_product_description()
    cart_page = CartPage(browser, base_url)
    assert  cart_page.get_product_description() in product_description,  "Товар не добавился или добавился более одного раза"

@pytest.mark.only
def test_change_currency_in_main_page(browser,base_url):
    cyrrent_symbol = "£"
    main_page = MainPage(browser, base_url)
    main_page.currensy_choice(cyrrent_symbol)
    assert cyrrent_symbol in main_page.header_cart_button().text

@pytest.mark.only
def test_change_currency_in_catalog(browser,base_url):
    cyrrent_symbol = "£"
    main_page = MainPage(browser, base_url)
    main_page.currensy_choice(cyrrent_symbol)
    catalog_page = CatalogPage(browser,base_url)
    assert cyrrent_symbol in catalog_page.get_description_text()

@pytest.mark.only
def test_add_new_product(browser, base_url):
    admin_page = AdminPage(browser, base_url)
    account_page = admin_page.admin_login()
    product_page = account_page.open_add_products_page()
    product_name = "comp number 1"
    assert product_page.add_new_product(product_name,"some_tag", "model", "af"), "Нет сообщения об успешном добавлении"

@pytest.mark.only
def test_remove_product(browser, base_url):
    admin_page = AdminPage(browser, base_url)
    account_page = admin_page.admin_login()
    account_page.product_page()
    assert account_page.remove_product(), "нет сообщения об успешном удалении"

