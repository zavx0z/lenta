import os
from pathlib import Path

import pandas as pd

pytest_plugins = [
    "fixtures.wd"
]

category_path = Path(os.environ.get("STORE_DIR")).resolve() / "delivery"


def pytest_addoption(parser):
    parser.addoption("--category", action="store", default='Бакалея', help="Категория товаров")


def pytest_generate_tests(metafunc):
    category = metafunc.config.option.category
    df = pd.read_parquet(category_path / f"{category}.parquet", columns=['url'])
    metafunc.parametrize("url", df.url.to_list(), ids=[str(i).zfill(4) for i in df.index.to_list()], scope='class')
