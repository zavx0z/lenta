from logging_config import configure_logger
from dotenv import load_dotenv
import os
from time import sleep
import re
import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from datetime import datetime

from selenium_ext import scroll_to_center, highlight

load_dotenv()
logger = configure_logger('lenta')
options = ChromeOptions()
options.add_argument(f"--user-data-dir={os.getenv('USER_DATA_DIR')}")
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})  # disable Chrome restore option
wd = Chrome(options=options)

pattern = re.compile(r'-(\d+)%')


def update_promo():
    wd.get("https://lenta.com/crazy/")
    logger.info("Промо-акции")
    sleep(1)
    df = pd.DataFrame([
        card.get_attribute('href')
        for card in wd.find_elements(By.XPATH, "//a[@class='crazy-promo-list__promo-card']")
    ], columns=['href']).drop_duplicates()
    for row in df.itertuples():
        wd.get(row.href)
        # ЗАГОЛОВОК
        title = wd.find_element(By.XPATH, f"//h1[@class='crazy-promo__title']").text
        logger.info(f">>>> Скидка на: {title}")
        df.loc[df.index == row.Index, 'title'] = title
        # ДАТА
        date_text = wd.find_element(By.XPATH, f"//div[@class='crazy-promo__date-main']").text
        if '-' in date_text:
            start_date_text, end_date_text = date_text.split(' - ')
            start_date = datetime.strptime(start_date_text, '%d.%m').replace(year=datetime.now().year)
            end_date = datetime.strptime(end_date_text, '%d.%m').replace(year=datetime.now().year)
            logger.info(f'Дата: {start_date.strftime("%d.%m.%Y")}-{end_date.strftime("%d.%m.%Y")}')
        else:
            start_date = end_date = datetime.strptime(date_text, '%d.%m').replace(year=datetime.now().year)
            logger.info(f'Дата: {start_date.strftime("%d.%m.%Y")}')
        df.loc[df.index == row.Index, 'start'] = start_date
        df.loc[df.index == row.Index, 'end'] = end_date
        # СКИДКИ
        try:  # общая скидка
            percent_text = wd.find_element(By.XPATH, "//div[@class='crazy-promo__discount-label']").text
            percent = int(re.findall(pattern, percent_text)[0])
            df.loc[df.index == row.Index, 'percent'] = percent
            logger.info(f'Скидка: {percent}%')
        except NoSuchElementException:  # скидка на товар от определенного кол-ва
            condition_text, percent_text = wd.find_element(By.XPATH, "//div[@class='discount-label discount-label--with-condition crazy-promo__discount-label']").text.split('\n')
            df.loc[df.index == row.Index, 'condition'] = condition_text
            percent = int(re.findall(pattern, percent_text)[0])
            df.loc[df.index == row.Index, 'percent_with_condition'] = percent
            logger.info(f'Скидка: {percent}% при покупке {condition_text}')
            try:  # скидка на один товар
                percent_text = wd.find_element(By.XPATH, "//div[@class='discount-label discount-label--with-any-text crazy-promo__discount-label']").text
                percent = int(re.findall(pattern, percent_text)[0])
                df.loc[df.index == row.Index, 'percent'] = percent
                logger.info(f'Скидка: {percent}%')
            except NoSuchElementException:
                pass
        df.loc[df.index == row.Index, 'img'] = wd.find_element(By.XPATH, f"//img[@class='crazy-promo__image']").get_attribute('src')  # изображение
        df.loc[df.index == row.Index, 'text'] = wd.find_element(By.XPATH, f"//p[@class='crazy-promo__description-paragraph']").text  # описание
    df.to_parquet('promo.parquet')


def update_catalog():
    wd.get("https://lenta.com/catalog/?utm_source=lweb&utm_medium=banner&utm_campaign=up")
    df = pd.DataFrame(columns=['title', 'href'])
    logger.info(f"Доставка: Каталог")
    sleep(1)
    for card in wd.find_elements(By.XPATH, "//a[@class='group-card']"):
        idx = len(df) + 1
        df.loc[idx, 'title'] = card.text
        df.loc[idx, 'href'] = card.get_attribute('href')
        df.loc[idx, 'img'] = card.find_element(By.XPATH, '//img').get_attribute('src')
        logger.info(f"Категория: {card.text}")
    df.to_parquet('catalog.parquet')


def update_category(cat, visual):
    category = pd.read_parquet('store/catalog.parquet', filters=(('title', '=', cat),)).squeeze()
    wd.get(category.href)
    logger.info(f"Категория каталога: {category.title}")
    df = pd.DataFrame(columns=[
        'title',
        'href',
        'img',
        'price',
        'promo_percent',
        'promo_price',
        'rating',
        'comments_count',
        'volume',
        'manufacturer',
        'delivery',
        'text'
    ])

    def is_promo(card):
        try:
            card.find_element(By.XPATH, ".//div[contains(@class, 'discount-label-small')]")
            logger.info("Товар по акции")
            return True
        except NoSuchElementException:
            return False

    get_rub = lambda el: el.find_element(By.XPATH, ".//span[@class='price-label__integer']").text.replace(' ', '')
    get_kop = lambda el: el.find_element(By.XPATH, ".//small[@class='price-label__fraction']").text

    def parse(card, idx):
        title = card.find_element(By.XPATH, ".//div[@class='sku-card-small-header__title']").text
        df.loc[idx, 'title'] = title
        logger.info(f">>>> {title}")
        df.loc[idx, 'href'] = card.find_element(By.XPATH, 'a').get_attribute('href')
        df.loc[idx, 'img'] = card.find_element(By.XPATH, './/img').get_attribute('src')
        # Стоимость
        price_common = card.find_element(By.XPATH, ".//div[contains(text(), 'Обычная цена')]/..")
        rub = get_rub(price_common)
        kop = get_kop(price_common)
        cost = float(f"{rub}.{kop}")
        df.loc[idx, 'price'] = cost
        logger.info(f"Цена: {rub} рублей {kop} копеек")
        if is_promo(card):
            percent_text = card.find_element(By.XPATH, ".//div[@class='discount-label-small discount-label-small--sku-card sku-card-small__discount-label']").text
            percent = re.findall(pattern, percent_text)[0]
            df.loc[idx, 'promo_percent'] = percent
            logger.info(f"Скидка: {percent}%")
            price_promo = card.find_element(By.XPATH, ".//div[contains(text(), 'Цена по акции')]/..")
            rub = get_rub(price_promo)
            kop = get_kop(price_promo)
            cost = float(f"{rub}.{kop}")
            df.loc[idx, 'promo_price'] = cost
            logger.info(f"Цена по акции: {rub} рублей {kop} копеек")
        rating = float(card.find_element(By.XPATH, ".//span[@class='sku-card-small-header__rating-text']").text)
        df.loc[idx, 'rating'] = rating
        logger.info(f"Рейтинг: {rating}")
        comments = float(card.find_element(By.XPATH, ".//span[@class='sku-card-small-header__comments-text']").text)
        df.loc[idx, 'comments_count'] = comments
        logger.info(f"Кол-во комментариев: {int(comments)}")
        try:
            sub_title = card.find_element(By.XPATH, ".//*[@class='sku-card-small-header__sub-title']").text
            if ',' in sub_title:
                manufacturer, volume = sub_title.split(', ')
                logger.info(f"Страна производитель: {manufacturer}")
                df.loc[idx, 'manufacturer'] = manufacturer
            else:
                volume = sub_title
            df.loc[idx, 'volume'] = volume
            logger.info(f"Объем: {volume}")
        except NoSuchElementException:
            pass

        df.loc[idx, 'text'] = card.text
        try:
            card.find_element(By.XPATH, ".//span[contains(text(), 'Зарезервировать')]")
            df.loc[idx, 'delivery'] = 0
            logger.info("Доставка: отсутствует")
        except NoSuchElementException:
            df.loc[idx, 'delivery'] = 1
            logger.info("Доставка: имеется")

    def is_other_shops(card):
        try:
            card.find_element(By.XPATH, """.//div[@class='sku-card-small__not-available-notice' and contains(text(), 'Товар доступен в других магазинах "Лента"')]""")
            return True
        except NoSuchElementException:
            return False

    def is_retail_store(card):
        try:
            card.find_element(By.XPATH, ".//div[contains(text(), 'Доступен в розничных магазинах ЛЕНТА')]")
            return True
        except NoSuchElementException:
            return False

    while True:
        sleep(2)
        pagination = wd.find_element(By.XPATH, "//ul[@class='pagination']")
        selected = pagination.find_element(By.XPATH, "li[@class='pagination__item selected']").text
        all_items = pagination.find_elements(By.XPATH, "li[contains(@class, 'pagination__item')]")[-1].text
        logger.info(f"\n=====>>> СТРАНИЦА: {selected} из {all_items}")
        for card in wd.find_elements(By.XPATH, "//div[@class='sku-card-small-container']"):
            if visual:
                scroll_to_center(card)
                highlight(card, .1)
            if not is_other_shops(card) and not is_retail_store(card):
                idx = len(df) + 1
                parse(card, idx)
            else:
                title = card.find_element(By.XPATH, ".//div[@class='sku-card-small-header__title']").text
                logger.info(f"Отсутствует в нашем магазине: {title}")
        if int(selected) == int(all_items):
            break
        else:
            wd.find_element(By.XPATH, "//ul[@class='pagination']//li[@class='next']").click()

    df.to_parquet(f'{category.title}.parquet')


if __name__ == '__main__':
    update_category('Бакалея', visual=True)
