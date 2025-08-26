from re import search
from venv import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.alert import Alert
import pytest
import logging
from datetime import datetime, date
import inspect

class BasePage():
    PATH = ""
    LOGO = By.ID, "logo"
    TITLE = ""
    def __init__(self, browser, url):
        self.browser = browser
        self.browser.get(url + self.PATH)
        self.logger = browser.logger
        self.wait = WebDriverWait(self.browser, 5)
        self.wait.until(EC.title_is(self.TITLE))

    def find_logo(self):
        logging.info('поиск логотипа')
        return self.browser.find_element(*self.LOGO)

    def selfy_find_element(self, element_selector):
        try:
            element = self.browser.find_element(*element_selector)
            self.browser.logger.debug(f'выполнен поиск элемента {inspect.currentframe().f_back.f_code.co_name}')
            return element
        except:
            self.browser.logger.error(f'элемент {inspect.currentframe().f_back.f_code.co_name} не найденпо {element_selector}')
            self.browser.save_screenshot("screenshorts/page.png") #{time.strftime('%Y%m%d_%H%M%S')}
            raise AssertionError(f'по запросу из {inspect.currentframe().f_back.f_code.co_name} не удалось найти элемент по {element_selector}')

class AdminPage (BasePage):
    PATH = "/administration"
    TITLE = 'Administration'
    USERNAME_FIELD = By.NAME, 'username'
    PASSWORD_FIELD = By.NAME, "password"
    LOGIN_BUTTON = By.CSS_SELECTOR, "#form-login > div.text-end > button"
    LOGO = By.CSS_SELECTOR,"[src='view/image/logo.png']"

    def find_username(self):
        return self.browser.find_element(*self.USERNAME_FIELD)

    def find_password(self):
        return self.browser.find_element(*self.PASSWORD_FIELD)

    def find_login_button(self):
        logging.info('попытка входа')
        return self.browser.find_element(*self.LOGIN_BUTTON)

    def logout_button(self):
        logging.info('поиск кнопки выхода из приложения')
        wait = WebDriverWait(self.browser, 5)
        return wait.until(EC.element_to_be_clickable((By.ID, "nav-logout")))

    def admin_login(self):
        logging.info('вход в приложение')
        self.find_username().send_keys("user")
        self.find_password().send_keys("bitnami")
        self.find_login_button().click()
        return AdminAccount(self.browser)

class AddProductPage(BasePage):
    PRODUCT_NAME = By.CSS_SELECTOR, "#input-name-1"
    META_TEG_TITLE = By.CSS_SELECTOR,'#input-meta-title-1'
    DATA_PAGE = By.CSS_SELECTOR,'#form-product > ul > li:nth-child(2) > a'
    SEO_PAGE = By.CSS_SELECTOR,'#form-product > ul > li:nth-child(11) > a'
    MODEL_FILD = By.CSS_SELECTOR, '#input-model'
    KEYWORD_FILD = By.CSS_SELECTOR, '#input-keyword-0-1'
    SAVE_BUTTON =  By.CSS_SELECTOR, '#content > div.page-header > div > div > button > i'

    def __init__(self, browser):
        self.browser = browser
        self.logger = browser.logger
        self.wait = WebDriverWait(self.browser, 5)

    def add_new_product(self,product_name, tag_title, model, keyword):
        self.browser.logger.info("вызов функции добавления продукта")
        self.selfy_find_element(self.PRODUCT_NAME).send_keys(product_name)
        self.selfy_find_element(self.META_TEG_TITLE).send_keys(tag_title)
        self.selfy_find_element(self.DATA_PAGE).click()
        self.selfy_find_element(self.MODEL_FILD).send_keys(model)
        self.selfy_find_element(self.SEO_PAGE).click()
        self.selfy_find_element(self.KEYWORD_FILD).send_keys(keyword)
        self.browser.logger.debug("обязательные поля заполнены")
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()
        return True

class AdminAccount(BasePage):
    FIlTER_NAME = By.CSS_SELECTOR, '#input-name'
    SEARCH_BUTTON = By.CSS_SELECTOR, '#button-filter'
    FIRST_PRODUCT_DESCRIPTION = By.CSS_SELECTOR, '#form-product > div.table-responsive > table > tbody > tr > td:nth-child(3)'
    ADD_PRODUCT_BUTTON = By.CSS_SELECTOR, "#content > div.page-header > div > div > a"
    PRODUCT_SELECTOR = By.CSS_SELECTOR, '#form-product > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(1) > input'
    REMOVE_BUTTON = By.CSS_SELECTOR, '#content > div.page-header > div > div > button.btn.btn-danger'
    SUCCESS_ALERT = By.CSS_SELECTOR, '#alert'
    BTN_DANGER = By.CSS_SELECTOR, '#content > div.page-header > div > div > button.btn.btn-danger'
    CATALOG_BUTTON = By.CSS_SELECTOR, "#collapse-1"
    PRODUCT_BUTTON = By.CSS_SELECTOR, "#collapse-1 > li:nth-child(2) > a"

    def __init__(self, browser):
        self.browser = browser

    def open_add_products_page(self):
        self.product_page()

        self.browser.find_element(*self.ADD_PRODUCT_BUTTON).click()

        return AddProductPage(self.browser)

    def product_page(self):
        self.browser.logger.info('Открытие страницы продукта')
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.title_is("Dashboard"))
        self.browser.execute_script("arguments[0].setAttribute('class', 'collapse show')",
                                    self.browser.find_element(*self.CATALOG_BUTTON))
        self.browser.find_element(*self.PRODUCT_BUTTON).click()

    def find_product(self, product_name):
        self.browser.logger.info(f'Поиск продука {product_name}')
        self.selfy_find_element(self.PRODUCT_BUTTON).click()
        self.selfy_find_element(self.FIlTER_NAME).send_keys(product_name)
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()
        try:
            wait.until(EC.text_to_be_present_in_element(self.FIRST_PRODUCT_DESCRIPTION, product_name))
            return wait.until(EC.element_to_be_clickable(self.FIRST_PRODUCT_DESCRIPTION)).text
        except:
            raise AssertionError('элемент не найден поиском')


    def remove_product(self):
        self.browser.logger.info('Удаление продукта')
        self.selfy_find_element(self.PRODUCT_SELECTOR).click()
        self.selfy_find_element(self.REMOVE_BUTTON).click()
        wait = WebDriverWait(self.browser, 5)
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        wait.until(EC.presence_of_element_located(self.BTN_DANGER))
        return wait.until(EC.text_to_be_present_in_element(self.SUCCESS_ALERT, "Success"))


class MainPage(BasePage):
    PATH = ""
    TITLE = "Your Store"
    LOGO = By.CSS_SELECTOR, '#logo'
    SEARCH_PANEL = By.ID, "search"
    HEADER_CART_BUTTON = By.ID, "header-cart"
    CURRENCY_CHOICE = By.ID, "form-currency"
    PRODUCTS_SELECTOR_LIST = By.CSS_SELECTOR, "[type='submit']"
    ADD_TO_CART_BUTTON = By.CSS_SELECTOR," [data-bs-original-title='Add to Cart']"
    PRODUCTS_DESCRIPTION_LIST = By.CSS_SELECTOR, "div.description: first-of-type"
    SUCCESS_ALERT = By.CSS_SELECTOR, '#alert'

    def search_panel(self):
        return self.browser.find_element(*self.SEARCH_PANEL)

    def header_cart_button(self):
        self.browser.logger.info("вызвана функция поиска кнопки перехода в корзину")
        return self.browser.find_element(*self.HEADER_CART_BUTTON)

    def currensy_choice(self, currency_symbol):
        self.browser.logger.info('Вызвана функция смены валюты')
        if currency_symbol == "€":
            href_value = "EUR"
        elif currency_symbol == "$":
            href_value = "USD"
        elif currency_symbol == "£":
            href_value = "GBP"
        CURRENCY_LOCATOR = By.CSS_SELECTOR, f"[href = {href_value}]"
        wait = WebDriverWait(self.browser, 5)
        try:
            self.browser.logger.debug('Поиск выпадающего списка')
            wait.until(EC.element_to_be_clickable(self.CURRENCY_CHOICE)).click()
            wait.until(EC.element_to_be_clickable(CURRENCY_LOCATOR)).click()
        except:
            self.browser.logger.error('Не удалось кликнуть на локатор')
            return None
        try:
            wait.until(EC.text_to_be_present_in_element(self.CURRENCY_CHOICE, currency_symbol))
            self.browser.logger.debug('Выполнен поиск выпадающего списка после выбора')
        except:
            self.browser.logger.error('Не удалось проверить текст')
        return self.browser.find_element(*self.CURRENCY_CHOICE)

    def add_product(self):
        self.browser.logger.info('Добавление продукта в корзину')
        try:
            self.wait.until(EC.presence_of_element_located(self.PRODUCTS_SELECTOR_LIST))
        except:
            raise AssertionError("нет списка выбора продукта")
        try:
            self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)).click()
        except:
            raise AssertionError("не удалось кликнуть на кнопку добавления продукта")
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert.accept()
            return wait.until(EC.text_to_be_present_in_element(self.SUCCESS_ALERT, "Success"))
        except:
            raise AssertionError("сообщение об успехе присутствует")


    def get_product_description(self):
        self.browser.logger.info('Получение описания товара')
        return self.browser.find_elements(self.PRODUCTS_DESCRIPTION_LIST)[0].text


class CatalogPage(BasePage):

    PATH = "/en-gb/catalog/desktops"
    TITLE = "Desktops"
    LOGO = By.CSS_SELECTOR, '#logo'
    PRODUCTS_DESCRIPTION = By.CLASS_NAME, "description"
    CARUSEL_SELECTOR = By.ID, "carousel-banner-0"
    DISPLAY_CONTROL =  By.ID, "display-control"
    PRODUCT_LIST = By.ID, "product-list"
    PAGINATION = By.CSS_SELECTOR, "#content:last-child"

    def find_product_category(self, product_category):
        PRODUCT_SELECTOR = By.CSS_SELECTOR, f"[href$='{product_category}']"
        self.browser.logger.info(f"поиск {product_category}")
        return self.browser.find_element(*PRODUCT_SELECTOR)

    def carusel(self):
        return self.selfy_find_element(self.CARUSEL_SELECTOR)

    def display_settings(self):
        return self.selfy_find_element(self.DISPLAY_CONTROL)

    def product_list(self):
        return self.selfy_find_element(self.PRODUCT_LIST)

    def pagination_buttons(self):
        if "Page" in self.selfy_find_element(self.PAGINATION).text:
            return self.selfy_find_element(self.PAGINATION)
        else:
            raise AssertionError("последений элемент контекста - не кнопки пагинации")

    def get_description_text(self):
        self.browser.logger.info('Поиск описания товара')
        return self.selfy_find_element(self.PRODUCTS_DESCRIPTION).text

class ProductCurt():
    CONTENT_PANEL = By.ID, "content"
    ADD_TO_CART_BUTTON = By.ID, "button-cart"
    PRICE_NEW = By.CLASS_NAME, "price-new"
    FIRST_FOTO = By.CSS_SELECTOR, "#content > div.row.mb-3 > div:nth-child(1) > div > a > img"
    def __init__(self, browser, url, product):
        self.product = product
        path = f"/en-gb/product/{self.product}"
        self.browser = browser
        self.browser.get(url + path)
        if product == 'macbook':
            title = "MacBook"
        elif product == 'iphone':
            title = "iPhone"
        elif product == 'cameras/nikon-d300':
            title = "Nikon D300"
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.title_is(title))

    def content(self):
        wait = WebDriverWait(self.browser, 5)
        return wait.until(EC.element_to_be_clickable(self.CONTENT_PANEL))

    def add_to_cart(self):
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)).click()
        return True

    def price_in_curt(self, currency_symbol):
        self.browser.logger.info('вызов функции проверки цены в выбранной валюте')
        wait = WebDriverWait(self.browser, 5)
        try:
            wait.until(EC.text_to_be_present_in_element(self.PRICE_NEW,currency_symbol))
        except:
            self.browser.logger.error('символ валюты не появился в описании цены')
            return None
        return self.browser.find_element(*self.PRICE_NEW).text

    def foto(self):
        wait = WebDriverWait(self.browser, 5)
        try:
            foto_element = self.browser.find_element(*self.FIRST_FOTO)
        except TimeoutError:
            self.browser.save_screenshot(f"screenshorts/{datetime.now().time()}.png")
            return None
        return foto_element

class RegisterAccountPage(BasePage):

    PATH = "/en-gb?route=account/register"
    TITLE = "Register Account"
    TEXT_FILD = By.CSS_SELECTOR, "#search > input"
    SEARCH_BUTTON = By.CSS_SELECTOR, "#search > button"
    PRODUCT_NAME = By.CSS_SELECTOR, "#product-list > div > div > div.content > div > h4 > a"
    LOGIN_PAGE_LINK = By.CSS_SELECTOR,"#content > p > a"
    FIRSTNAME_FILD= By.NAME, "firstname"
    LASTNAME_FILD = By.NAME, "lastname"
    EMAIL_FILD = By.NAME, "email"
    PASSWORD_FILD = By.NAME, "password"
    AGREE_POLICY = By.NAME, "agree"
    OK_BUTTON = By.CSS_SELECTOR, "#form-register > div > button"
    COMMON_SUCCESS = By.ID, "common-success"

    def registration_accont (self, firstname, lastname, email, password ):
        self.browser.logger.info(f"создаем аккаунт для пользователя {firstname} {lastname}")
        try:
            self.browser.find_element(*self.FIRSTNAME_FILD).send_keys(firstname)
            self.browser.find_element(*self.LASTNAME_FILD).send_keys(lastname)
            self.browser.find_element(*self.EMAIL_FILD).send_keys(email)
            self.browser.find_element(*self.PASSWORD_FILD).send_keys(password)
            self.browser.logger.debug("информация добавлена")
            self.browser.find_element(*self.AGREE_POLICY).click()
        except:
            self.browser.logger.error('не удалось ввести информацию о пользователе')
            return None
        wait = WebDriverWait(self.browser, 3)
        wait.until(EC.element_to_be_clickable(self.OK_BUTTON)).click()
        try:
            wait.until(EC.presence_of_element_located(self.COMMON_SUCCESS))
            self.browser.logger.debug('пользователь добавлен')
            return True
        except:
            try:
                error_massage = wait.until(EC.alert_is_present()).text
            except:
                error_massage = "сообщение об ошибке обнаружить не удалось"
            self.browser.logger.error(f'не удалось добавить пользователя: {error_massage}')
            return None

    def search_result (self, text):
        logging.info('поиск продукта с помощью панели поиска')
        self.browser.find_element(*self.TEXT_FILD).send_key(text)
        self.browser.find_element(*self.SEARCH_BUTTON).click()
        logging.debug('данные для поиска введены')
        wait = WebDriverWait(self.browser,5)
        product = wait.until(EC.text_to_be_present_in_element(self.PRODUCT_NAME, text))
        return product.get_attribute("href")

    def login_page_link (self):
        return self.browser.find_element(*self.LOGIN_PAGE_LINK)

class CartPage():
    PATH = "/en-gb?route=checkout/cart"
    PRODUCT_DESCRIPTION = By.CSS_SELECTOR,"#shopping-cart > div > table > tbody > tr > td.text-start.text-wrap > a"
    def __init__(self, browser, url):
       self.browser = browser
       self.browser.get(url + self.PATH)

    def get_product_description(self):
        self.browser.logger.info('получение описания продукта из корзины')
        return self.browser.find_element(*self.PRODUCT_DESCRIPTION).text