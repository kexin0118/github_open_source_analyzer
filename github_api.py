import requests

def show_url(repo:str)->str:
    url=f"https://api.github.com/repos/{repo}"
    return url

def get_repo_info(repo:str)->tuple[str|None,int|None]:
    url=show_url(repo)
    try:
        response=requests.get(url,timeout=10)
        if response.status_code==404:
            print(f"仓库{repo}不存在")
            return None,None
        if response.status_code==403:
            print("被拒绝请求,可能权限不足或API请求收到限制")
            return None,None
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("请求异常",e)
        return None,None
    else:
        try:
            data=response.json()
            name=data["full_name"]
            stars=data["stargazers_count"]
        except KeyError as e:
            print("API返回的数据缺少字段",e)
            return None,None
        else:
            print("请求成功")
            return name,stars

#批量获取仓库信息
def get_multiple_repos(repos:list[str])->list[tuple[str,int]]:
    results:list[tuple[str,int]]=[]
    for name in repos:
        result=get_repo_info(name)
        if result==(None,None):
            continue
        print(result)
        results.append(result)
    return results