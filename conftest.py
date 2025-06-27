from email.policy import default

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
#from urllib3 import request



def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests", default="chrome")
    parser.addoption("--drivers", help="Driver storage", default=r"C:\Users\Mariya\Downloads\drivers")
    parser.addoption("--headless", action="store_true", help="Browser run headless")
    parser.addoption(
        "--base_url", help="Base application url", default="192.168.0.231:8181"
    )
@pytest.fixture(scope="session")
def base_url(request):
    return "http://" + request.config.getoption("--base_url")

@pytest.fixture()
def browser(request):
    driver = None
    browser_name = request.config.getoption("--browser")
    drivers_storage = request.config.getoption("--drivers")
    headless = request.config.getoption("--headless")
    if browser_name in ["ch", "chrome"]:
        options = ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser_name in ["ff","fox","firefox"]:
        options=FFOptions()
        if headless:
            options.add_argument("headless")
        driver = webdriver.Firefox(options=options)
    elif browser_name in ["ya","yandex"]:
        options = ChromiumOptions()
        if headless:
            options.add_argument("headless=new")
        options.binary_location = r"c:\Users\Mariya\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
        driver = webdriver.Chrome(options=options, service=ChromiumService(
            executable_path=fr"{drivers_storage}\yandexdriver.exe"))
    yield driver
    driver.quit()