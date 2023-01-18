import os
import re


def get_parametrize_id():
    return re.findall(r"\[(.*)\]", os.environ.get('PYTEST_CURRENT_TEST'))[0]
