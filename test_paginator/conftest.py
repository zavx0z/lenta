from pathlib import Path
from urllib.parse import urlunparse, urlencode
import allure
import pandas as pd
import pytest
from parse_schema import Schema

pytest_plugins = ["fixtures.wd"]


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default='',
        help="Адрес страницы"
    )
    parser.addoption(
        "--schema",
        action="store",
        default='schema.xml',
        help="Схема страницы"
    )
    parser.addoption(
        "--result",
        action="store",
        default='result.parquet',
        help="Файл результата"
    )


@pytest.fixture(scope='class')
def url(request):
    yield request.config.option.url


@pytest.fixture(scope='class')
def schema(request):
    yield Schema(request.config.option.schema)


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    # if exitstatus == 0:
    store = session.items[0].instance.store

    page_count = int(store.queryParams.iloc[-1].page)
    key_query_param = store.queryParams.columns[0]
    parted_link = store.partedLinks.head(1).squeeze()

    df = pd.DataFrame(index=range(1, page_count + 1))
    df['scheme'] = parted_link['scheme']
    df['netloc'] = parted_link['netloc']
    df['path'] = parted_link['path']
    df['params'] = parted_link['params']
    df['query'] = df.index.map(lambda x: urlencode({key_query_param: x}))
    df['fragment'] = parted_link['fragment']

    result = pd.DataFrame([urlunparse(tuple(i)[1:]) for i in df.itertuples()], columns=['url'], index=df.index)
    result.to_parquet(Path(session.config.option.result), index=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when == "setup":
        allure.dynamic.feature(item.config.option.url)
    # elif report.when == "call" and report.passed:
