# GitHub open source analyzer

## 项目介绍

本项目是一个基于 Python 和 GitHub REST API 开发的命令行仓库分析工具。

用户可以输入多个 GitHub 仓库名称，程序通过 requests 获取仓库信息，提取仓库名称与 Stars 数量，按照用户指定的最低 Stars 数量进行筛选和排序，并将最终结果导出为 CSV 文件。

项目支持 GitHub Token 认证、网络异常处理、API 数据校验及 unittest + Mock 自动化测试。
## 主要功能
- 获取仓库stars数量
- 对多个仓库进行排名
- 处理网络请求异常
- 使用unittest+Mock 对异常及处理,API请求进行自动化测试(12项测试)
- CSV导出
- token认证

## 安装依赖
```bash
python -m pip install -r requirements.txt
```
## 配置 GitHub Token（可选）

本项目支持通过环境变量读取 GitHub Token，
用于向 GitHub API 发送认证请求。

Windows PowerShell：

```powershell
$env:GITHUB_TOKEN = "你的Token"
```

设置完成后，在同一个终端运行项目。

注意：
- 不要将真实 Token 写入 Python 源代码。
- 不要将真实 Token 提交到 GitHub。
- 未配置 Token 时，仍可查询公开仓库，但会受到更严格的 API 请求频率限制。

## 运行项目
```bash
## 使用示例

输入你想查询的仓库
python/cpython
pallets/flask
0

输入最小stars:
1000

程序将：
1. 查询输入的 GitHub 仓库
2. 获取仓库名称和 Stars 数量
3. 筛选满足最低 Stars 要求的仓库
4. 按 Stars 数量降序排序
5. 将结果保存到 ranking.csv
```

## 运行测试
```bash
python test.py
```
## 项目结构

```text
github_open_source_analyzer/
├── github_api.py       # GitHub API 请求与数据校验
├── ranking.py          # 仓库筛选与排序
├── export.py           # CSV 导出
├── main.py             # 程序入口与用户交互
├── test.py             # 自动化测试
├── requirements.txt    # 项目依赖
├── README.md           # 项目说明
└── .gitignore          # Git 忽略规则
```
## 数据校验与异常处理

为了提高程序的稳定性，项目实现了以下检查：

- 处理网络超时及 HTTP 请求异常。
- 检查 API 返回的 JSON 数据是否为字典。
- 检查必要字段是否存在。
- 检查仓库名称是否为非空字符串。
- 检查 Stars 是否为非负整数，并拒绝布尔值等不合法类型。
- 对无效仓库数据返回 (None, None)，避免错误数据进入后续处理。

## 技术栈

- **Python 3.12**：主要开发语言
- **requests**：发送 GitHub API HTTP 请求
- **JSON**：解析 API 返回的数据
- **CSV**：导出仓库分析结果
- **unittest**：自动化单元测试
- **unittest.mock**：模拟 API 请求和响应
- **Git / GitHub**：版本控制与代码管理