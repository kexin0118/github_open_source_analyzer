# GitHub open source analyzer

## 项目介绍

根据用户输入的仓库标识,构造API URL,再通过requests.get()请求数据
## 主要功能
- 获取仓库stars数量
- 对多个仓库进行排名
- 处理网络请求异常
- 使用unittest+Mock 对异常及处理,API请求进行自动化测试(10项测试)
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
python main.py
```

## 运行测试
```bash
python test.py
```
## 项目结构

```text
github_open_source_analyzer/
├── github_api.py
├── main.py
├── test.py
├── requirements.txt
├── README.md
└── .gitignore
```