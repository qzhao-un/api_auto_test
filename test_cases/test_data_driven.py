import allure
import pytest
import time
from common.yaml_util import get_test_data

@allure.feature("数据驱动测试")
class TestDataDriven:

    def _get_username(self, api):
        resp = api.get("/user")
        return resp.json()["login"]

    @allure.story("数据驱动-创建仓库")
    @allure.title("{case_name}")
    @pytest.mark.parametrize("case", get_test_data("create_repo_cases"), ids=lambda x: x["case_name"])
    def test_create_repo_data_driven(self, api, case):
        repo_name = f"{case['name']}_{int(time.time())}"
        payload = {
            "name": repo_name,
            "description": case["description"],
            "private": case["private"]
        }
        resp = api.post("/user/repos", json=payload)
        assert resp.status_code == case["expected_status"]
        data = resp.json()
        assert data["name"] == repo_name
        assert data["private"] == case["private"]
        username = self._get_username(api)
        api.delete(f"/repos/{username}/{repo_name}")

    @allure.story("数据驱动-查询仓库")
    @allure.title("{case_name}")
    @pytest.mark.parametrize("case", get_test_data("get_repo_cases"), ids=lambda x: x["case_name"])
    def test_get_repo_data_driven(self, api, case):
        username = self._get_username(api)
        resp = api.get(f"/repos/{username}/{case['repo_name']}")
        assert resp.status_code == case["expected_status"]