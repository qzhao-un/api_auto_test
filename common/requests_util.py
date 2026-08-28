import requests
import allure
from common.logger_util import get_logger


class RequestsUtil:
    def __init__(self, base_url="https://api.github.com", token=None, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = get_logger()
        if token:
            self.session.headers.update({
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            })
        self.session.verify = False

    def request(self, method, url, **kwargs):
        url = self.base_url + url
        self.logger.info(f"请求: {method.upper()} {url}")
        if kwargs.get("json"):
            self.logger.info(f"请求体: {kwargs['json']}")
        with allure.step(f"发送请求: {method.upper()} {url}"):
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            self.logger.info(f"响应状态码: {response.status_code}")
            self.logger.info(f"响应内容: {response.text[:500]}")
            allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
            return response

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)

    def patch(self, url, **kwargs):
        return self.request("PATCH", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)