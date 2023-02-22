import os

import pytest
from chrome_boss import ChromeBoss


@pytest.fixture(scope="session")
def boss():
    chrome_host = os.environ.get('CHROME_HOST', 'localhost')
    chrome_port = os.environ.get('CHROME_PORT', 4444)
    boss = ChromeBoss(host=chrome_host, port=chrome_port)
    yield boss
    boss.destroy()


# def report_failure(item):
#     if 'wd' not in item.fixturenames:
#         allure.dynamic.description("Браузер не работает")
#     else:
#         wd.find_element(By.XPATH, "//h1[.='С вашего IP-адреса приходит слишком много запросов.']")
# allure.attach(item.keywords.node.funcargs.get('wd').get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    # if report.when == "call":
    # if report.failed:
    #     report_failure(item)
