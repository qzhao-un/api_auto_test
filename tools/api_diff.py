import requests
import json
import yaml
import os
from datetime import datetime


def deep_diff(obj1, obj2, path=""):
    """递归对比两个对象，返回差异列表"""
    diffs = []

    if type(obj1) != type(obj2):
        diffs.append(f"{path}: 类型不同 - {type(obj1).__name__} vs {type(obj2).__name__}")
        return diffs

    if isinstance(obj1, dict):
        all_keys = set(obj1.keys()) | set(obj2.keys())
        for key in all_keys:
            current_path = f"{path}.{key}" if path else key
            if key not in obj1:
                diffs.append(f"{current_path}: 仅在第二个响应中存在")
            elif key not in obj2:
                diffs.append(f"{current_path}: 仅在第一个响应中存在")
            else:
                diffs.extend(deep_diff(obj1[key], obj2[key], current_path))
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            diffs.append(f"{path}: 数组长度不同 - {len(obj1)} vs {len(obj2)}")
        for i in range(min(len(obj1), len(obj2))):
            diffs.extend(deep_diff(obj1[i], obj2[i], f"{path}[{i}]"))
    else:
        if obj1 != obj2:
            diffs.append(f"{path}: 值不同 - {obj1} vs {obj2}")

    return diffs


def compare_api(url1, url2, headers=None):
    """对比两个接口的返回"""
    print(f"\n{'='*60}")
    print(f"对比接口:")
    print(f"  环境A: {url1}")
    print(f"  环境B: {url2}")
    print(f"{'='*60}")

    resp1 = requests.get(url1, headers=headers, verify=False, timeout=10)
    resp2 = requests.get(url2, headers=headers, verify=False, timeout=10)

    print(f"\n状态码: A={resp1.status_code}, B={resp2.status_code}")
    if resp1.status_code != resp2.status_code:
        print("⚠️  状态码不一致!")

    try:
        data1 = resp1.json()
        data2 = resp2.json()
    except:
        print("❌ 响应不是JSON格式")
        return []

    diffs = deep_diff(data1, data2)

    if not diffs:
        print("✅ 两个响应完全一致")
    else:
        print(f"❌ 发现 {len(diffs)} 处差异:")
        for i, diff in enumerate(diffs, 1):
            print(f"  {i}. {diff}")

    return diffs


def run_from_yaml(yaml_file, token=None):
    """从YAML配置文件批量对比"""
    with open(yaml_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    all_diffs = {}
    for case in config.get("compare_cases", []):
        name = case["name"]
        url1 = case["url1"]
        url2 = case["url2"]
        diffs = compare_api(url1, url2, headers)
        all_diffs[name] = diffs

    # 生成报告
    report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_file = os.path.join(report_dir, f"diff_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"接口对比报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        for name, diffs in all_diffs.items():
            f.write(f"【{name}】\n")
            if not diffs:
                f.write("  ✅ 完全一致\n\n")
            else:
                f.write(f"  发现 {len(diffs)} 处差异:\n")
                for i, diff in enumerate(diffs, 1):
                    f.write(f"  {i}. {diff}\n")
                f.write("\n")

    print(f"\n\n📄 对比报告已保存: {report_file}")
    return all_diffs


if __name__ == "__main__":
    import os
    token = os.getenv("GITHUB_TOKEN")
    yaml_file = os.path.join(os.path.dirname(__file__), "..", "test_data", "diff_cases.yaml")
    yaml_file = os.path.abspath(yaml_file)
    run_from_yaml(yaml_file, token)