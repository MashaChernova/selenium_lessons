import pytest
from page_objects import AdminPage


@pytest.mark.reserv
def test_search_form(browser, base_url):
    admin_page = AdminPage(browser, base_url)
    assert admin_page.find_logo(), "Отсутствует логотип"
    assert admin_page.find_username(), "Нет поля ввода имени пользователя"
    assert admin_page.find_password(), "Нет поля ввода пароля"
    assert admin_page.find_login_button(), "Нет кнопки входа"