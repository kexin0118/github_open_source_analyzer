# GitHub open source analyzer

## 项目介绍

根据用户输入的仓库标识,构造API URL,再通过requests.get()请求数据
## 主要功能
- 获取仓库stars数量
- 对多个仓库进行排名
- 处理网络请求异常
- 使用unittest对API请求和异常进行自动化测试

## 安装依赖
'''bash
python -m pip install -r requirements.txt
'''

## 运行项目
'''bash
python main.py
'''

## 运行测试
'''bash
python test.py
'''