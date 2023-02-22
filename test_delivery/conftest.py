from pathlib import Path
import pytest

from parse_schema import Schema

pytest_plugins = ["fixtures.boss"]


def pytest_addoption(parser):
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
def schema(request):
    yield Schema(Path(__file__).parent / 'schema.xml')


@pytest.fixture(scope='class')
def tab(request, boss):
    tab = boss.tab(1)
    yield tab


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 0:
        store = session.items[0].instance.store
        print(store)
