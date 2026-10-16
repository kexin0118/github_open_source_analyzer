from github_api import get_repo_info

def get_stars(repo):
    return repo[1]

def show_ranking(results,descending=True):#默认值是True
    results_stars=sorted(results,key=get_stars,reverse=descending)
    for index,content in enumerate(results_stars,start=1):
        name,stars=content
        print(f"第{index}名:{name},Stars:{stars:,}")

#批量获取仓库信息
def get_multiple_repos(repos):
    results=[]
    for name in repos:
        result=get_repo_info(name)
        if result==(None,None):
            continue
        print(result)
        results.append(result)
    return results

def filter_repos(results,min_stars):
    filtered=[]
    for result in results:
        if result[1]>=min_stars:
            filtered.append(result)
    return filtered

def get_min_stars():
    while True:
        try:
            n=int(input("输入最小stars:"))
            if(n<0):
                print("stars不能是负数!")
                continue
            return n
        except ValueError:
            print("输入错误,请重新输入整数!")

def get_repo():
    repos=[]
    print("输入你想查询的仓库")
    while True:
        repo=input().strip().lower()
        if repo=="":
            print("仓库不能为空!")
            continue
        if repo in repos:
            print("此仓库已输入")
            continue
        if repo=="0":
            break
        if repo.count("/")!=1:
            print("输入格式错误")
            continue
        if repo.split("/")[1]=="" or repo.split("/")[0]=="":
            print("用户名不能为空")
            continue
        repos.append(repo)
    return repos

#results.sort(results,key=get_stars,reverse=True)   直接修改原列表,返回值为None
#results=sorten(results,key=get_stars,reverse=True) 不修改原列表,返回新列表
if __name__=="__main__":
    repos=get_repo()
    min_stars=get_min_stars()
    results=get_multiple_repos(repos)
    filtered=filter_repos(results,min_stars)
    show_ranking(filtered)#False是从小到大,True是从大到小(可以不写因为被设定为默认值)
    print("repositories:",len(results))
    print(len(filtered))
    print(results)