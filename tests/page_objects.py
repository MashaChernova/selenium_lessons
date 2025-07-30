from re import search

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.alert import Alert
import pytest

class BasePage():
    PATH = ""
    LOGO = By.ID, "logo"
    TITLE = ""
    def __init__(self, browser, url):
        self.browser = browser
        self.browser.get(url + self.PATH)
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.title_is(self.TITLE))

    def find_logo(self):
        return self.browser.find_element(*self.LOGO)

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
        return self.browser.find_element(*self.LOGIN_BUTTON)

    def logout_button(self):
        wait = WebDriverWait(self.browser, 5)
        return wait.until(EC.element_to_be_clickable((By.ID, "nav-logout")))

    def admin_login(self):
        self.find_username().send_keys("user")
        self.find_password().send_keys("bitnami")
        self.find_login_button().click()
        return AdminAccount(self.browser)




class AddProductPage():
    PRODUCT_NAME = By.CSS_SELECTOR, "#input-name-1"
    META_TEG_TITLE = By.CSS_SELECTOR,'#input-meta-title-1'
    DATA_PAGE = By.CSS_SELECTOR,'#form-product > ul > li:nth-child(2) > a'
    SEO_PAGE = By.CSS_SELECTOR,'#form-product > ul > li:nth-child(11) > a'
    MODEL_FILD = By.CSS_SELECTOR, '#input-model'
    KEYWORD_FILD = By.CSS_SELECTOR, '#input-keyword-0-1'
    SAVE_BUTTON =  By.CSS_SELECTOR, '#content > div.page-header > div > div > button > i'


    def __init__(self, browser):
        self.browser = browser

    def add_new_product(self,product_name, tag_title, model, keyword ):
        self.browser.find_element(*self.PRODUCT_NAME).send_keys(product_name)
        self.browser.find_element(*self.META_TEG_TITLE).send_keys(tag_title)
        self.browser.find_element(*self.DATA_PAGE).click()
        self.browser.find_element(*self.MODEL_FILD).send_keys(model)
        self.browser.find_element(*self.SEO_PAGE).click()
        self.browser.find_element(*self.KEYWORD_FILD).send_keys(keyword)
        self.browser.find_element(*self.SAVE_BUTTON).click()
        return True






class AdminAccount():
    FIlTER_NAME = By.CSS_SELECTOR, '#input-name'
    SEARCH_BUTTON = By.CSS_SELECTOR, '#button-filter'
    FIRST_PRODUCT_DESCRIPTION = By.CSS_SELECTOR, '#form-product > div.table-responsive > table > tbody > tr > td:nth-child(3)'

    def __init__(self, browser):
        self.browser = browser

    def open_add_products_page(self):

        add_product_button = By.CSS_SELECTOR, "#content > div.page-header > div > div > a"

        self.product_page()

        self.browser.find_element(*add_product_button).click()

        return AddProductPage(self.browser)

    def product_page(self):
        catalog_button = By.CSS_SELECTOR, "#collapse-1"

        product_button = By.CSS_SELECTOR, "#collapse-1 > li:nth-child(2) > a"

        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.title_is("Dashboard"))

        self.browser.execute_script("arguments[0].setAttribute('class', 'collapse show')",
                                    self.browser.find_element(*catalog_button))

        self.browser.find_element(*product_button).click()

    def find_product(self, product_name):
        product_button = By.CSS_SELECTOR, "#collapse-1 > li:nth-child(2) > a"
        self.browser.find_element(*product_button).click()
        self.browser.find_element(*self.FIlTER_NAME).send_keys(product_name)
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        self.browser.find_element(*self.SEARCH_BUTTON).click()
        return self.browser.find_element(*self.FIRST_PRODUCT_DESCRIPTION).text

    def remove_product(self):
        product_selector = By.CSS_SELECTOR, '#form-product > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(1) > input'
        remove_button = By.CSS_SELECTOR, '#content > div.page-header > div > div > button.btn.btn-danger'
        success_alert = By.CSS_SELECTOR, '#alert'
        self.browser.find_element(*product_selector).click()
        self.browser.find_element(*remove_button).click()
        wait = WebDriverWait(self.browser, 5)
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        self.browser.find_element(By.CSS_SELECTOR, '#content > div.page-header > div > div > button.btn.btn-danger')
        return self.browser.find_element(*success_alert)


class MainPage(BasePage):
    PATH = ""
    TITLE = "Your Store"
    LOGO = By.CSS_SELECTOR, '#logo'
    SEARCH_PANEL = By.ID, "search"
    HEADER_CART_BUTTON = By.ID, "header-cart"
    CURRENCY_CHOICE = By.ID, "form-currency"

    def search_panel(self):
        return self.browser.find_element(*self.SEARCH_PANEL)

    def header_cart_button(self):
        return self.browser.find_element(*self.HEADER_CART_BUTTON)

    def currensy_choice(self):
        return self.browser.find_element(*self.CURRENCY_CHOICE)

    def currensy_choice(self, currency_symbol):
        if currency_symbol == "€":
            href_value = "EUR"
        elif currency_symbol == "$":
            href_value = "USD"
        elif currency_symbol == "£":
            href_value = "GBP"
        locator = By.CSS_SELECTOR, f"[href = {href_value}]"
        self.browser.find_element(*self.CURRENCY_CHOICE).click()
        self.browser.find_element(*locator).click()
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.text_to_be_present_in_element((self.CURRENCY_CHOICE),text_=currency_symbol))
        return self.browser.find_element(*self.CURRENCY_CHOICE)

    def add_product(self):
        self.browser.find_elements(By.CSS_SELECTOR, "[type='submit']")[0].click()
        return 0

    def get_product_description(self):
        return self.browser.find_elements(By.CLASS_NAME, "description")[0].text


class CatalogPage(BasePage):

    PATH = "/en-gb/catalog/desktops"
    TITLE = "Desktops"
    LOGO = By.CSS_SELECTOR, '#logo'

    def find_product_category(self, product_category):
        PRODUCT_SELECTOR = By.CSS_SELECTOR, f"[href$='{product_category}']"
        return self.browser.find_element(*PRODUCT_SELECTOR)

    def carusel(self):
        SELECTOR = By.ID, "carousel-banner-0"
        return self.browser.find_element(*SELECTOR)

    def display_settings(self):
        SELECTOR = By.ID, "display-control"
        return self.browser.find_element(*SELECTOR)

    def product_list(self):
        SELECTOR = By.ID, "product-list"
        return self.browser.find_element(*SELECTOR)

    def pagination_buttons(self):
        SELECTOR = By.CLASS_NAME, "pagination"
        return self.browser.find_element(*SELECTOR)

    def get_description_text(self):
        return self.browser.find_element(By.CLASS_NAME, "description").text

class ProductCurt():
    CONTENT_PANEL = By.ID, "content"
    ADD_TO_CART_BUTTON = By.ID, "button-cart"

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
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "price-new"),currency_symbol))
        return self.browser.find_element(By.CLASS_NAME, "price-new").text

    def foto(self):
        wait = WebDriverWait(self.browser, 5)
        return self.browser.find_element(By.CSS_SELECTOR, "#content > div.row.mb-3 > div:nth-child(1) > div > a > img")

class RegisterAccountPage(BasePage):

    PATH = "/en-gb?route=account/register"
    TITLE = "Register Account"

    def registration_accont (self, firstname, lastname, email, password ):

        firstname_fild = By.NAME, "firstname"
        lastname_fild = By.NAME, "lastname"
        email_fild = By.NAME, "email"
        password_fild = By.NAME, "password"
        agree_polycy = By.NAME, "agree"
        ok_button = By.CSS_SELECTOR, "#form-register > div > button"

        self.browser.find_element(*firstname_fild).send_keys(firstname)
        self.browser.find_element(*lastname_fild).send_keys(lastname)
        self.browser.find_element(*email_fild).send_keys(email)
        self.browser.find_element(*password_fild).send_keys(password)
        self.browser.find_element(*agree_polycy).click()
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.element_to_be_clickable(ok_button)).click()
        return self.browser.find_element(By.CSS_SELECTOR,"#content > div > a")

    def search_result (self, text):
        text_field = By.CSS_SELECTOR, "#search > input"
        search_button = By.CSS_SELECTOR, "#search > button"
        self.browser.find_element(*text_field).send_key(text)
        self.browser.find_element(*search_button).click()
        wait = WebDriverWait(self.browser,5)
        product = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#product-list > div > div > div.content > div > h4 > a"), text))
        return product.get_attribute("href")

    def login_page_link (self):
        return self.browser.find_element(By.CSS_SELECTOR,"#content > p > a")

class CartPage():
    PATH = "/en-gb?route=checkout/cart"

    def __init__(self, browser, url):
       self.browser = browser
       self.browser.get(url + self.PATH)

    def get_product_description(self):
        return self.browser.find_element(By.CSS_SELECTOR,"#shopping-cart > div > table > tbody > tr > td.text-start.text-wrap > a").text






