import allure

@allure.feature("评论模块")
class TestComments:

    @allure.story("获取评论列表")
    @allure.title("GET /comments - 获取评论列表")
    def test_get_comments(self, api):
        resp = api.get("/comments")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 500
        assert "email" in data[0]
        assert "body" in data[0]

    @allure.story("按帖子ID查评论")
    @allure.title("GET /comments?postId=1 - 查询帖子1的评论")
    def test_get_comments_by_post(self, api):
        resp = api.get("/comments?postId=1")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 5
        for comment in data:
            assert comment["postId"] == 1
