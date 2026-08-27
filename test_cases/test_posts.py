import allure
import pytest

@allure.feature("帖子模块")
class TestPosts:

    @allure.story("获取帖子列表")
    @allure.title("GET /posts - 获取帖子列表并校验字段完整性")
    def test_get_posts(self, api):
        resp = api.get("/posts")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 100
        for post in data[:5]:
            assert "userId" in post
            assert "id" in post
            assert "title" in post
            assert "body" in post

    @allure.story("参数化查询")
    @allure.title("GET /posts?userId={user_id} - 按用户ID筛选帖子")
    @pytest.mark.parametrize("user_id, expected_count", [(1, 10), (2, 10), (3, 10)])
    def test_get_posts_by_user(self, api, user_id, expected_count):
        resp = api.get(f"/posts?userId={user_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == expected_count
        for post in data:
            assert post["userId"] == user_id

    @allure.story("创建帖子")
    @allure.title("POST /posts - 创建新帖子")
    def test_create_post(self, api):
        payload = {"title": "测试标题", "body": "测试内容", "userId": 1}
        resp = api.post("/posts", json=payload)
        assert resp.status_code == 201
        assert resp.json()["title"] == "测试标题"
