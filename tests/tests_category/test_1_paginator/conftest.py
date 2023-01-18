import os
from pathlib import Path
from urllib.parse import urlunparse, urlencode

import allure
import pandas as pd
import pytest
from parse_schema import Schema

pytest_plugins = [
    "fixtures.wd"
]


def pytest_addoption(parser):
    parser.addoption(
        "--category",
        action="store",
        default='Бакалея',
        help="Категория товаров"
    )
    parser.addoption(
        "--parse_schema",
        action="store",
        default=Path(__file__).parents[1] / 'schema.xml',
        help="Схема страницы"
    )


def pytest_generate_tests(metafunc):
    df = pd.read_parquet(
        path=Path(os.environ.get("STORE_DIR")).resolve() / 'catalog.parquet',
        filters=(
            ('title', '=', metafunc.config.option.category),
        ),
        columns=['href']
    )
    metafunc.parametrize(
        argnames="url",
        argvalues=df.href.to_list(),
        ids=df.index.map(lambda i: str(i).zfill(4)).to_list(),
        scope='class'
    )


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    print(session)
    print(exitstatus)


def setup(item):
    category = item.config.option.category
    allure.dynamic.epic("Каталог")
    allure.dynamic.feature(category)

    if 'test_open' is item.originalname:
        item.instance.category = category


def report_success(item):
    if 'test_query_params_text' in item.originalname:
        page_count = int(item.instance.store.queryParams.iloc[-1].page)
        key_query_param = item.instance.store.queryParams.columns[0]
        parted_link = item.instance.store.partedLinks.head(1).squeeze()

        df = pd.DataFrame(index=range(1, page_count + 1))
        df['scheme'] = parted_link['scheme']
        df['netloc'] = parted_link['netloc']
        df['path'] = parted_link['path']
        df['params'] = parted_link['params']
        df['query'] = df.index.map(lambda x: urlencode({key_query_param: x}))
        df['fragment'] = parted_link['fragment']
        result = pd.DataFrame([urlunparse(tuple(i)[1:]) for i in df.itertuples()], columns=['url'], index=df.index)
        result.to_parquet(Path(os.environ.get("STORE_DIR")).resolve() / 'catalog' / f'{item.config.option.category}.parquet', index=True)



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when == "setup":
        setup(item)
    elif report.when == "call" and report.passed:
        report_success(item)


@pytest.fixture(scope='session')
def schema(request):
    yield Schema(request.config.option.parse_schema)

# make_link = urlunparse(df.head(1).squeeze().values.tolist())
# make_query = lambda d: urlencode(d)
