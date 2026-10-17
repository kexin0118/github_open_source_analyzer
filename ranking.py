def get_stars(repo):
    return repo[1]

def show_ranking(results,descending=True):#默认值是True
    results_stars=sorted(results,key=get_stars,reverse=descending)
    for index,content in enumerate(results_stars,start=1):
        name,stars=content
        print(f"第{index}名:{name},Stars:{stars:,}")
    return results_stars

#筛选仓库
def filter_repos(results,min_stars):
    filtered=[]
    for result in results:
        if result[1]>=min_stars:
            filtered.append(result)
    return filtered
