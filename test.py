import unittest
import requests
from unittest.mock import Mock,patch
from github_api import get_repo_info

#TestGitHubApi自定义测试类,unittest.TestCase父类,self指向自定义测试类
class TestGitHubApi(unittest.TestCase):
    def test_403(self):#self表示当前测试的实例
        response=Mock()
        response.status_code=403
        with patch("github_api.requests.get") as mock_get:
            mock_get.return_value=response
            results=get_repo_info("python/cpython")
            print(results)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_404(self):
        response=Mock()
        response.status_code=404
        with patch("github_api.requests.get") as mock_get:
            mock_get.return_value=response
            results=get_repo_info("python/cpython")
            print(results)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_200(self):
        response=Mock()
            #预先json的内容
        response.json.return_value={
            "full_name":"python/cpython",
            "stargazers_count":100000
        }
        response.status_code=200
        with patch("github_api.requests.get") as mock_get:
            mock_get.return_value=response
            results=get_repo_info("python/cpython")
            print(results)
            self.assertEqual(("python/cpython",100000),results)
            mock_get.assert_called_once()

    def test_timeout(self):
        with patch("github_api.requests.get")as mock_get:
            mock_get.side_effect=requests.exceptions.Timeout("请求超时")
            #一执行mock_get也就是requests.get就会抛出一个异常(Timeout)
            #side_effect是mock_get的一个属性:主动抛出一个异常(类似status_code是response的一个属性)
            #"请求超时"相当于github_api中的e
            results=get_repo_info("python/cpython")
            print(results)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()

    def test_ConnectionError(self):
        with patch("github_api.requests.get")as mock_get:
            mock_get.side_effect=requests.exceptions.ConnectionError("连接异常")
            results=get_repo_info("python/cpython")
            print(results)
            self.assertEqual(results,(None,None))
            mock_get.assert_called_once()
    
if __name__=="__main__":#只有运行test.py才执行下面代码
    unittest.main() 
    #unittest自动寻找并运行当前文件中符合规则的测试方法
    #1.测试类要继承unittest.TestCase
    #2.测试方法名以test开头(test_)