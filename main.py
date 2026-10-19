from ranking import show_ranking,filter_repos
from github_api import get_multiple_repos
from export import export_to_csv

def get_min_stars()->int:
    while True:
        try:
            n=int(input("输入最小stars:"))
            if(n<0):
                print("stars不能是负数!")
                continue
            return n
        except ValueError:
            print("输入错误,请重新输入整数!")

def get_repo()->list[str]:
    repos=[]
    print("输入你想查询的仓库")
    while True:
        repo=input().strip().lower()
        if repo=="0":
            break
        if repo=="":
            print("仓库不能为空!")
            continue
        if repo in repos:
            print("此仓库已输入")
            continue
        if repo.count("/")!=1:
            print("输入格式错误")
            continue
        if " "in repo:
            print("输入格式错误")
            continue
        if repo.split("/")[1]=="" or repo.split("/")[0]=="":
            print("用户名不能为空")
            continue
        repos.append(repo)
    return repos

#results.sort(results,key=get_stars,reverse=True)   直接修改原列表,返回值为None
#results=sorted(results,key=get_stars,reverse=True) 不修改原列表,返回新列表
if __name__=="__main__":
    repos=get_repo()
    min_stars=get_min_stars()
    results=get_multiple_repos(repos)
    filtered=filter_repos(results,min_stars)
    print("repositories总数:",len(results))
    print("大于min_stars的仓库个数:",len(filtered))
    sorted_repo=show_ranking(filtered)#False是从小到大,True是从大到小(可以不写因为被设定为默认值)
    export_to_csv("ranking.csv",sorted_repo)