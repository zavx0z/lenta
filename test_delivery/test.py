import allure


class TestDelivery:
    @allure.title('Открытие категории')
    def test_open(self, tab, schema):
        buttons = tab.get_element(schema, remote=True)
        delivery_button = buttons.get_element(schema / "Доставка", remote=False)
        background = buttons.style
        assert tab
