# 接口自动化测试项目

基于 Python + Pytest + Requests + Allure 搭建的接口自动化测试框架，对 JSONPlaceholder 公开API进行全面测试。

## 技术栈
- Python 3.9+
- Pytest（测试框架，支持参数化、Fixture）
- Requests（HTTP请求库）
- Allure（可视化测试报告）
- PyYAML（配置管理）

## 项目结构
```
api_auto_test/
├── config/              # 配置文件
├── common/              # 公共工具类
├── test_cases/          # 测试用例
├── test_data/           # 测试数据
├── reports/             # 测试报告
├── conftest.py          # Pytest全局Fixture
├── pytest.ini           # Pytest配置
└── requirements.txt     # 依赖清单
```

## 覆盖接口
- GET /users - 获取用户列表
- GET /users/{id} - 获取单个用户
- POST /users - 创建用户
- GET /posts - 获取帖子列表
- GET /posts?userId= - 按条件筛选
- POST /posts - 创建帖子
- GET /comments - 获取评论列表

## 运行方式
```bash
pip install -r requirements.txt
pytest
allure serve reports/allure-results
```
