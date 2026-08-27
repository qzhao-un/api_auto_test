import requests
import allure
from common.yaml_util import get_config

class RequestsUtil:
    def __init__(self):
        config = get_config()
        self.base_url = config["base_url"]
        self.timeout = config["timeout"]
        self.session = requests.Session()

    def request(self, method, url, **kwargs):
        url = self.base_url + url
        with allure.step(f"发送请求: {method.upper()} {url}"):
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
            return response

    def get(self, url, **kwargs):
        return self.request("get", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("post", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("put", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("delete", url, **kwargs)
