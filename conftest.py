import pytest
import os
from common.requests_util import RequestsUtil

@pytest.fixture(scope="session")
def api():
    token = os.getenv("GITHUB_TOKEN")
    req = RequestsUtil(token=token)
    yield req