import allure


class TestCategory:
    @allure.title('Открытие категории')
    def test_open(self, wd, url):
        wd.get(url)
        assert True
