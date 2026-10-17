import unittest
import requests
import csv
import os
from unittest.mock import Mock,patch
from github_api import get_repo_info
from export import export_to_csv

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
            results=get_repo_info(self.repo)
            print(results)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_404(self):
        response=Mock()
        response.status_code=404
        with patch("github_api.requests.get") as mock_get:
            mock_get.return_value=response
            results=get_repo_info(self.repo)
            print(results)
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

    def test_timeout(self):
        with patch("github_api.requests.get")as mock_get:
            mock_get.side_effect=requests.exceptions.Timeout("请求超时")
            #一执行mock_get也就是requests.get就会抛出一个异常(Timeout)
            #side_effect是mock_get的一个属性:主动抛出一个异常(类似status_code是response的一个属性)
            #"请求超时"相当于github_api中的e
            results=get_repo_info(self.repo)
            print(results)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_ConnectionError(self):
        with patch("github_api.requests.get")as mock_get:
            mock_get.side_effect=requests.exceptions.ConnectionError("连接异常")
            results=get_repo_info(self.repo)
            print(results)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_missing_field(self):
        response=Mock()
        response.status_code=200
        response.json.return_value={"full_name":self.repo}
        with patch("github_api.requests.get")as mock_get:
            mock_get.return_value=response   
            results=get_repo_info(self.repo)
            print(results)
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

if __name__=="__main__":#只有运行test.py才执行下面代码
    unittest.main() 
    #unittest自动寻找并运行当前文件中符合规则的测试方法
    #1.测试类要继承unittest.TestCase
    #2.测试方法名以test开头(test_)