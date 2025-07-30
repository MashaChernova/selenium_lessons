import pytest
from page_objects import RegisterAccountPage
import time

@pytest.mark.reserv
def test_search_form(browser, base_url):
    register_account_page = RegisterAccountPage(browser, base_url)
    assert register_account_page.LOGO(), "Отсутствует логотип"

@pytest.mark.reserv
def test_search_form(browser, base_url):
    register_account_page = RegisterAccountPage(browser, base_url)
    assert register_account_page.login_page_link(), "Нет ссылки на страницу входа для зарегистрированных пользователей"

@pytest.mark.reserv
@pytest.mark.parametrize("firstname, lastname, email, password",
                         [("1", "1", "1@1.a", "1234"),
                          ("000102030405060708090a0b0c0d0e0f", "000102030405060708090A0B0C0D0E0F", "FFFFFFFFFFFFFFFFFFFFFFFFFYFFFFFFFFFFFFYFFFFYFFFFFFYYFFFYFFFFFFFF@1.a", "0010203040506070809")],
                         ids=["user_short_name", "user_log_name"])
def test_search_form(browser, base_url, firstname, lastname, email, password):
    register_account_page = RegisterAccountPage(browser, base_url)
    assert register_account_page.login_page_link(), "Нет ссылки на страницу входа для зарегистрированных пользователей"
    assert register_account_page.registration_accont(firstname, lastname, email, password), "Регистрация не удалась"




