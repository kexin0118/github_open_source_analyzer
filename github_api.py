import requests
import os
import logging

logger=logging.getLogger(__name__)#name标识当前模块身份
def show_url(repo:str)->str:
    url=f"https://api.github.com/repos/{repo}"
    return url

def get_repo_info(repo:str)->tuple[str|None,int|None]:
    url=show_url(repo)
    logger.info(f"开始请求仓库:{repo}")#记录程序准备请求哪个仓库
    #读取密钥
    token=os.getenv("GITHUB_TOKEN")
    try:
        headers={}
        if token:
           headers["Authorization"]=f"Bearer {token}"
        response=requests.get(url,headers=headers,timeout=10)
        if response.status_code==404:
            logger.warning(f"仓库 {repo} 不存在,HTTP 状态码:404")
            print(f"仓库{repo}不存在")
            return None,None
        if response.status_code==403:
            logger.warning(f"仓库{repo}请求被拒绝, HTTP 状态码:403,可能权限不足或API请求收到限制")
            print("被拒绝请求,可能权限不足或API请求收到限制")
            return None,None
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.exception(f"仓库{repo}请求发生异常")
        print("请求异常",e)
        return None,None
    else:
        try:
            data=response.json()
            if not isinstance(data,dict):
                return None,None
            name=data["full_name"]
            stars=data["stargazers_count"]
            if type(stars) is not int or stars<0:
                return None,None
            if not isinstance(name,str) or not name:
                return None,None
        except KeyError as e:
            print("API返回的数据缺少字段",e)
            return None,None
        else:
            logger.info("仓库 %s 数据获取成功",name)
            print("请求成功")
            return name,stars

#批量获取仓库信息
def get_multiple_repos(repos:list[str])->list[tuple[str,int]]:
    results:list[tuple[str,int]]=[]
    for name in repos:
        result_name,result_stars=get_repo_info(name)
        if result_name is None or result_stars is None:
            continue
        print(result_name,result_stars)
        results.append((result_name,result_stars))
    return results