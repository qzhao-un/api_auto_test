import pytest
from common.requests_util import RequestsUtil

@pytest.fixture(scope="session")
def api():
    req = RequestsUtil()
    yield req
