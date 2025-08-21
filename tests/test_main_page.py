import pytest
from page_objects import MainPage

@pytest.mark.reserv
def test_search_form(browser, base_url):
    main_page = MainPage(browser, base_url)
    assert main_page.find_logo(), "Нет логотипа"
    assert main_page.search_panel(), "Нет панели поиска"

@pytest.mark.reserv
def test_no_money_to_start(browser, base_url):
    main_page = MainPage(browser, base_url)
    assert main_page.find_logo()
    assert "0.00" in main_page.header_cart_button().text, "Возможно, конзина не пуста"

@pytest.mark.reserv
def test_head(browser, base_url):
    currency_symbol = "$"
    main_page = MainPage(browser, base_url)
    assert currency_symbol in main_page.currensy_choice(currency_symbol).text, "Неверная валюта по умолчанию"

@pytest.mark.reserv
@pytest.mark.parametrize("currency_symbol",
                         ["€",
                          "$",
                          "£"],
                         ids=["euro", "dollar", "pound"])
def test_change_currency(browser, base_url, currency_symbol):
    main_page = MainPage(browser, base_url)
    main_page.currensy_choice(currency_symbol)
    assert currency_symbol in main_page.header_cart_button().text, "Валюта не отображается на кнопке корзины"