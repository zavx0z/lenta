import os

import allure
import pytest
from selenium.webdriver import DesiredCapabilities
from undetected_chromedriver import Chrome, ChromeOptions


@pytest.fixture(scope="session")
def wd():
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={os.getenv('USER_DATA_DIR')}")
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})  # disable Chrome restore option
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    wd = Chrome(options=options, desired_capabilities=capabilities)
    yield wd
    wd.quit()


def report_failure(item):
    if 'wd' not in item.fixturenames:
        allure.dynamic.description("Браузер не работает")
    else:
        # wd.find_element(By.XPATH, "//h1[.='С вашего IP-адреса приходит слишком много запросов.']")
        allure.attach(item.keywords.node.funcargs.get('wd').get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when == "call":
        if report.failed:
            report_failure(item)
