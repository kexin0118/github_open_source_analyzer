import unittest
import requests
import csv
import os
import importlib
import config
from unittest.mock import Mock,patch
from github_api import get_repo_info,show_url
from export import export_to_csv
from github_api import get_multiple_repos

#TestGitHubApi自定义测试类(子类),unittest.TestCase父类
#self代表当前正在执行测试的对象
class TestGitHubApi(unittest.TestCase):
    def setUp(self):
        self.repo="python/cpython"
        
    def test_403(self):#self表示当前测试的实例
        response=Mock()
        response.status_code=403
        with patch("github_api.requests.get") as mock_get:
            mock_get.return_value=response
            with self.assertLogs("github_api",level="WARNING")as cm:
                results=get_repo_info(self.repo)

            self.assertIn("可能权限不足或API请求收到限制",cm.output[0])
            self.assertIsNone(cm.records[0].exc_info)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_404(self):
        response=Mock()
        response.status_code=404
        with patch("github_api.requests.get") as mock_get:
            mock_get.return_value=response
            with self.assertLogs("github_api",level="WARNING")as cm:
                results=get_repo_info(self.repo)
            self.assertIn("不存在",cm.output[0])
            self.assertIsNone(cm.records[0].exc_info)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_200(self):
        response=Mock()
            #预先json的内容
        response.json.return_value={
            "full_name":self.repo,
            "stargazers_count":100000
        }
        response.status_code=200
        with patch("github_api.requests.get") as mock_get:
            mock_get.return_value=response
            results=get_repo_info(self.repo)
            print(results)
            self.assertEqual((self.repo,100000),results)
            mock_get.assert_called_once()

    @patch("github_api.requests.get")
    def test_invalid_json_structure(self,mock_get):
        datas=["invalid",100,None,[]]
        response=Mock()
        mock_get.return_value=response
        response.status_code=200
        for data in datas:
            response.json.return_value=data
            with self.assertLogs("github_api",level="WARNING")as cm:
                result=get_repo_info(self.repo)

            self.assertIn(f"仓库{self.repo}数据模式错误",cm.output[0])
            self.assertEqual(result,(None,None))

    def test_timeout(self):
        with patch("github_api.requests.get")as mock_get:
            mock_get.side_effect=requests.exceptions.Timeout("请求超时")
            with self.assertLogs("github_api",level="ERROR")as cm:
                results=get_repo_info(self.repo)

            self.assertIn("请求发生异常",cm.output[0])
            self.assertIsNotNone(cm.records[0].exc_info)
            if cm.records[0].exc_info is not None:
                self.assertIs(cm.records[0].exc_info[0],requests.exceptions.Timeout)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_ConnectionError(self):
        with patch("github_api.requests.get")as mock_get:
            mock_get.side_effect=requests.exceptions.ConnectionError("连接异常")
            with self.assertLogs("github_api",level="ERROR")as cm:
                results=get_repo_info(self.repo)

            self.assertIn("请求发生异常",cm.output[0])
            self.assertIsNotNone(cm.records[0].exc_info)
            if cm.records[0].exc_info is not None:
                self.assertIs(cm.records[0].exc_info[0],requests.exceptions.ConnectionError)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_missing_field(self):
        cases=[
            ({"full_name":self.repo},"stargazers_count"),
            ({"stargazers_count":100},"full_name")
        ]
        for data,missing_field in cases:
            response=Mock()
            response.status_code=200
            response.json.return_value=data
            with patch("github_api.requests.get")as mock_get:
                mock_get.return_value=response
                with self.assertLogs("github_api",level="WARNING")as cm:
                    results=get_repo_info(self.repo)   
                print(results)
                self.assertIn(f"缺少字段 '{missing_field}'",cm.output[0])
                self.assertEqual(results,(None,None))
                mock_get.assert_called_once()

    def test_export_csv(self):
        repos=[
            ("A",500),
            ("B",600)
        ]
        export_to_csv("test_ranking.csv",repos)
        with open("test_ranking.csv","r",encoding="utf-8-sig",newline="")as f:
            reader=csv.reader(f)#创建一个csv读取器
            rows=list(reader)#把读取到的没一会转换成列表,方便检查
            self.assertEqual(rows[0],["Rank","repository","stars"])
            self.assertEqual(rows[1],["1","A","500"])
            self.assertEqual(rows[2],["2","B","600"])
        self.addClassCleanup(os.remove,"test_ranking.csv")

#当批量获取仓库中的无效仓库时,程序能跳过它,并继续处理后面的有效仓库
    def test_multiple_repos_skip_invalid(self):
        with patch("github_api.get_repo_info") as mock_get:
            mock_get.side_effect=[
                ("python/cpython",77898),
                (None,None),
                ("pallets/flask",71000)
            ]
            repos=["python/cpython","invalid/repo","pallets/flask"]
            results=get_multiple_repos(repos)
            self.assertEqual(results,[("python/cpython",77898),("pallets/flask",71000)])

    def test_token_header(self):
        #with内部会读取到fake_token
        with patch.dict("os.environ",{"GITHUB_TOKEN":"fake_token"}):#把环境变量GITHUB_TOKEN修改为faketoken
            with patch("github_api.requests.get")as mock_get:
                mock_get.return_value.status_code=404
                get_repo_info(self.repo)
                mock_get.assert_called_once_with(
                    show_url(self.repo),
                    headers={"Authorization":"Bearer fake_token"},
                    timeout=10
                )

    def test_without_token(self):
        with patch.dict("os.environ",{"GITHUB_TOKEN":""}):
            with patch("github_api.requests.get")as mock_get:
                mock_get.return_value.status_code=404
                get_repo_info(self.repo)
                mock_get.assert_called_once_with(
                    show_url(self.repo),
                    headers={},
                    timeout=10
                )

    @patch("github_api.requests.get")
    def test_invalid_stars_name(self,mock_get):
        invalid_values=[
            ("python/cpython","100"),
            ("python/cpython",True),
            ("python/cpython",-10),
            ("python/cpython",None),
            ("python/cpython",100.5),
            (None,100),
            ("",100),
            (123,100)
        ]
        
        for name,stars in invalid_values:
            response=Mock()
            mock_get.return_value=response
            response.status_code=200
            response.json.return_value={
                "full_name":name,
                "stargazers_count":stars
            }
            with self.assertLogs("github_api",level="WARNING")as cm:
                result=get_repo_info(self.repo)
            if type(stars) is not int or stars<0:
                self.assertIn(f"{stars}不合法",cm.output[0])
            elif not isinstance(name,str) or not name:
                self.assertIn(f"{name}不合法",cm.output[0])
            self.assertEqual((None,None),result)

    def test_success_logging(self):
        response=Mock()
        response.status_code=200
        response.json.return_value={
            "full_name":"python/cpython",
            "stargazers_count":1000
        }
        with patch("github_api.requests.get")as mock_get:
            mock_get.return_value=response
            with self.assertLogs("github_api",level="INFO")as mc:
                result=get_repo_info(self.repo)

            self.assertEqual(mc.records[0].levelname,"INFO")
            self.assertTrue(any("数据获取成功"in log for log in mc.output))
            self.assertTrue(all(record.levelname=="INFO"for record in mc.records))
            self.assertEqual(result,("python/cpython",1000))
            mock_get.assert_called_once()

    def test_request_timeout_from_env(self):
        with patch.dict(os.environ,{"REQUEST_TIMEOUT":"20"}):
            self.addCleanup(importlib.reload,config)#测试结束后才执行,并不是当下立即执行
            importlib.reload(config)
            self.assertEqual(config.REQUEST_TIMEOUT,20)

    #验证配置有没有真正传给requests.get()
    @patch("github_api.requests.get")
    def test_api_uses_config_timeout(self,mock_get):
        with patch.dict(os.environ,{"REQUEST_TIMEOUT":"20"},clear=True):#临时清除原有的环境变量,再放入我们指定的环境变量
            self.addCleanup(importlib.reload,config)
            importlib.reload(config)
            mock_get.return_value.status_code=200
            mock_get.return_value.json.return_value={
                "full_name":"python/cpython",
                "stargazers_count":1000
            }
            result=get_repo_info(self.repo)
            self.assertEqual(result,("python/cpython",1000))
            mock_get.assert_called_once_with(
                show_url(self.repo),
                headers={},
                timeout=20
            )

    def test_invalid_request_timeout(self):
        tests=["-10","0","7.8","abc"]
        self.addCleanup(importlib.reload,config)
        for test in tests:
            with self.subTest(value=test):#给循环中的每组测试数据建立一个独立的子测试
                with patch.dict(os.environ,{"REQUEST_TIMEOUT":test}):
                    importlib.reload(config)
                    self.assertEqual(config.DEFULT_TIMEOUT,config.REQUEST_TIMEOUT)

        
if __name__=="__main__":#只有运行test.py才执行下面代码
    unittest.main() 
    #unittest自动寻找并运行当前文件中符合规则的测试方法
    #1.测试类要继承unittest.TestCase
    #2.测试方法名以test开头(test_)