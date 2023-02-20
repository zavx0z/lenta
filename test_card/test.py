import allure
from time import sleep

from utils.html import allure_html_img_full_page


class TestCard:
    @allure.title('Открытие категории')
    def test_open(self, boss, url):
        boss.get(url)
        count = 0
        while count < 5:
            count += 1
            sleep(1)
            if boss.title: break
        allure_html_img_full_page(boss)
        assert boss.title

    def test_card_links(self, boss, url, schema):
        pass
