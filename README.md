# API 自动化测试框架

基于 Python + Pytest + Requests 的接口自动化测试框架，以 GitHub API 为实践对象，涵盖功能测试、数据驱动、持续集成、接口对比等能力。

## 技术栈

| 技术 | 用途 |
|---|---|
| Python 3 | 开发语言 |
| Pytest | 测试框架 |
| Requests | HTTP请求库 |
| PyYAML | 数据驱动配置 |
| pytest-html | HTML测试报告 |
| Allure | 可视化测试报告 |
| pytest-rerunfailures | 失败自动重试 |
| GitHub Actions | CI/CD持续集成 |

## 项目结构
api_auto_test/
├── common/ # 公共模块
│ ├── requests_util.py # 请求封装（鉴权、日志、SSL）
│ └── logger_util.py # 日志工具类
├── test_cases/ # 测试用例
│ ├── test_github_repos.py # 仓库 CRUD 测试
│ └── test_data_driven.py # 数据驱动测试
├── test_data/ # 测试数据
│ ├── repo_data.yaml # 用例数据
│ └── diff_cases.yaml # 接口对比配置
├── tools/ # 工具
│ └── api_diff.py # 接口对比工具
├── reports/ # 测试报告（自动生成）
├── logs/ # 运行日志（自动生成）
├── conftest.py # Pytest 配置与 Fixture
├── pytest.ini # Pytest 配置文件
├── requirements.txt # 依赖清单
└── .github/workflows/ci.yml # CI/CD 流水线

## 核心功能

### 1. 接口自动化测试
- 覆盖 GitHub 仓库的增删改查（CRUD）全流程
- 包含正常场景与异常场景（重复创建、不存在的仓库、未授权等）
- 测试前后自动清理测试数据，保持环境干净

### 2. 数据驱动
- 测试数据与代码分离，通过 YAML 文件管理
- 同一用例多组数据，减少重复代码

### 3. 日志系统
- 所有请求的方法、URL、请求体、响应状态码、响应内容自动记录
- 按日期分割日志文件，同时输出到控制台和文件
- 测试失败时可快速定位问题

### 4. 失败自动重试
- 网络抖动导致的失败自动重试2次，间隔1秒
- 减少误报，提高测试稳定性

### 5. CI/CD 持续集成
- 基于 GitHub Actions，每次提交代码自动运行测试
- 通过 Secret 管理敏感 Token，不硬编码
- 测试报告作为构件归档

### 6. 接口对比工具
- 自研工具，支持对比两个环境/接口的返回差异
- 递归对比 JSON 结构，识别字段缺失、类型不一致、值不同
- YAML 配置批量对比，自动生成差异报告
- 应用场景：上线前回归、新旧环境对比

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt