import allure
import pandas as pd
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qsl

from utils.allure.html import allure_html_img_base64_string, allure_html_list
from utils.allure.pandas import allure_html_table
from utils.allure.selenium import allure_html_img_full_page


class TestCategoryPagination:
    store = pd.Series({
        "links": list,
        "partedLinks": pd.DataFrame,
        "diffColumns": list,
        "queryParams": pd.DataFrame,
        "diffQueryKeys": list,
    })

    @allure.title('Страница категории')
    def test_open(self, wd, url):
        wd.get(url)
        allure_html_img_full_page(wd)
        assert self.category in wd.title

    @allure.title("Пагинация")
    def test_pagination_element(self, wd, url, schema):
        pagination_el = wd.find_element(By.XPATH, schema)
        allure_html_img_base64_string(pagination_el.screenshot_as_base64, 'пагинация')
        assert len(pagination_el.text.split('\n')) > 1

    @allure.title("Ссылки пагинации")
    def test_links(self, wd, url, schema):
        link_elements = wd.find_elements(By.XPATH, schema / "список" / "страница" / "ссылка")
        links = [link.get_attribute('href') for link in link_elements]
        allure_html_list(links)
        self.store.links = links
        assert len(links) > 1

    @allure.title("Валидность ссылок")
    def test_links_validate(self, wd, url):
        parted_links = pd.DataFrame([urlparse(link)._asdict() for link in self.store.links])
        allure_html_table(parted_links)
        self.store.partedLinks = parted_links
        assert parted_links.isna

    @allure.title('Различие ссылок')
    def test_links_diff_one_part(self, wd, url, schema):
        diff_columns = [column for column in self.store.partedLinks.columns if not all(self.store.partedLinks.duplicated(subset=[column], keep=False))]
        allure_html_list(diff_columns)
        self.store.diffColumns = diff_columns
        assert len(diff_columns) == 1

    @allure.title("Различие ссылок в параметрах запроса")
    def test_link_diff_query_param(self, wd, url):
        column = self.store.diffColumns[0]
        allure.dynamic.description_html(f"Изменяемая часть в url: {column}")
        assert column == 'query'

    @allure.title("Параметры запроса")
    def test_query_param(self, wd, url):
        query_param = pd.DataFrame([dict(parse_qsl(q, encoding='utf-8')) for q in self.store.partedLinks['query'].to_list()])
        allure_html_table(query_param)
        self.store.queryParams = query_param

    @allure.title("Различие в параметрах запроса в одном ключе")
    def test_query_params_one_key(self, wd, url):
        diff_query_keys = self.store.queryParams.columns.to_list()
        allure_html_list(diff_query_keys)
        self.store.diffQueryKeys = diff_query_keys
        assert len(diff_query_keys) == 1

    @allure.title("Параметры запроса соответствуют тексту пагинации")
    def test_query_params_text(self, wd, url, schema):
        query_params = self.store.queryParams[self.store.diffQueryKeys[0]].values.tolist()
        paginate_text_elements = wd.find_elements(By.XPATH, schema / "список" / "страница" / "номер")
        paginate_texts = [i.text for i in paginate_text_elements]
        allure_html_table(pd.DataFrame(list(zip(query_params, paginate_texts)), columns=['Параметры запроса', 'Текст пагинации']))
        assert paginate_texts == query_params
