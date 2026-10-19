def get_stars(repo:tuple[str,int])->int:
    return repo[1]

def show_ranking(results:list[tuple[str,int]],descending:bool=True)->list[tuple[str,int]]:#默认值是True
    results_stars=sorted(results,key=get_stars,reverse=descending)
    for index,content in enumerate(results_stars,start=1):
        name,stars=content
        print(f"第{index}名:{name},Stars:{stars:,}")
    return results_stars

#筛选仓库
def filter_repos(results:list[tuple[str,int]],min_stars:int)->list[tuple[str,int]]:
    filtered:list[tuple[str,int]]=[]
    for result in results:
        if result[1]>=min_stars:
            filtered.append(result)
    return filtered
