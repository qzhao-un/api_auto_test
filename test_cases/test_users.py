import allure

@allure.feature("用户模块")
class TestUsers:

    @allure.story("获取用户列表")
    @allure.title("GET /users - 正常获取用户列表")
    def test_get_users(self, api):
        resp = api.get("/users")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "id" in data[0]
        assert "name" in data[0]
        assert "email" in data[0]

    @allure.story("获取单个用户")
    @allure.title("GET /users/1 - 获取ID为1的用户详情")
    def test_get_user_by_id(self, api):
        resp = api.get("/users/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["name"] == "Leanne Graham"
        assert "@" in data["email"]

    @allure.story("获取单个用户-异常")
    @allure.title("GET /users/0 - 不存在的用户ID返回404")
    def test_get_user_not_found(self, api):
        resp = api.get("/users/0")
        assert resp.status_code == 404

    @allure.story("创建用户")
    @allure.title("POST /users - 正常创建新用户")
    def test_create_user(self, api):
        payload = {
            "name": "赵群",
            "username": "zhaoqun",
            "email": "zhaoqun@test.com",
            "phone": "18183561094"
        }
        resp = api.post("/users", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == payload["name"]
        assert data["email"] == payload["email"]
        assert "id" in data
