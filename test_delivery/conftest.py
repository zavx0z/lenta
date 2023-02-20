import pytest

pytest_plugins = [
    "fixtures.wd"
]


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 0:
        print(session)
