import allure
from time import sleep

from utils.html import allure_html_img_full_page


class TestDelivery:
    @allure.title('Открытие категории')
    def test_open(self, boss):
        boss.get("https://lenta.com/catalog/bakaleya/")
        count = 0
        while count < 5:
            count += 1
            sleep(1)
            if boss.title: break
        allure_html_img_full_page(boss)
        assert boss.title
