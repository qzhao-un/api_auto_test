import allure
import pytest
import time
from common.yaml_util import get_config

@allure.feature("GitHub仓库管理")
class TestGitHubRepos:

    @pytest.fixture(scope="function")
    def test_repo(self, api):
        config = get_config()
        prefix = config.get("test_repo_prefix", "test_auto_")
        repo_name = f"{prefix}{int(time.time())}"
        payload = {"name": repo_name, "description": "自动化测试仓库", "private": False}
        resp = api.post("/user/repos", json=payload)
        assert resp.status_code == 201
        yield repo_name
        username = self._get_username(api)
        api.delete(f"/repos/{username}/{repo_name}")

    def _get_username(self, api):
        resp = api.get("/user")
        return resp.json()["login"]

    @allure.story("鉴权验证")
    @allure.title("GET /user - 验证Token有效性，获取用户信息")
    def test_get_user_info(self, api):
        resp = api.get("/user")
        assert resp.status_code == 200
        data = resp.json()
        assert "login" in data
        assert "id" in data

    @allure.story("创建仓库")
    @allure.title("POST /user/repos - 正常创建新仓库")
    def test_create_repo(self, api):
        repo_name = f"test_create_{int(time.time())}"
        payload = {
            "name": repo_name,
            "description": "接口自动化测试创建的仓库",
            "private": False,
            "auto_init": True
        }
        resp = api.post("/user/repos", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == repo_name
        assert data["description"] == "接口自动化测试创建的仓库"
        username = self._get_username(api)
        del_resp = api.delete(f"/repos/{username}/{repo_name}")
        assert del_resp.status_code == 204

    @allure.story("查询仓库")
    @allure.title("GET /repos/{owner}/{repo} - 查询仓库详情")
    def test_get_repo(self, api, test_repo):
        username = self._get_username(api)
        resp = api.get(f"/repos/{username}/{test_repo}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == test_repo
        assert data["description"] == "自动化测试仓库"
        assert "created_at" in data

    @allure.story("修改仓库")
    @allure.title("PATCH /repos/{owner}/{repo} - 修改仓库描述")
    def test_update_repo(self, api, test_repo):
        username = self._get_username(api)
        payload = {"description": "修改后的描述", "has_issues": False}
        resp = api.patch(f"/repos/{username}/{test_repo}", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["description"] == "修改后的描述"
        assert data["has_issues"] == False

    @allure.story("删除仓库")
    @allure.title("DELETE /repos/{owner}/{repo} - 删除仓库")
    def test_delete_repo(self, api):
        repo_name = f"test_delete_{int(time.time())}"
        payload = {"name": repo_name, "description": "待删除"}
        create_resp = api.post("/user/repos", json=payload)
        assert create_resp.status_code == 201
        username = self._get_username(api)
        del_resp = api.delete(f"/repos/{username}/{repo_name}")
        assert del_resp.status_code == 204
        get_resp = api.get(f"/repos/{username}/{repo_name}")
        assert get_resp.status_code == 404

    @allure.story("异常场景")
    @allure.title("POST /user/repos - 重复创建同名仓库返回422")
    def test_create_duplicate_repo(self, api, test_repo):
        payload = {"name": test_repo, "description": "重复创建"}
        resp = api.post("/user/repos", json=payload)
        assert resp.status_code == 422