import csv

def export_to_csv(filename,repos):
    #f是打开的文件对象,告诉python将数据写到哪里
    with open(filename,"w",newline="",encoding="utf-8-sig")as f:
        writer=csv.writer(f)
        writer.writerow(["Rank","repository","stars"])
        for index,repo in enumerate(repos,start=1):
            name,stars=repo
            writer.writerow([index,name,stars])

if __name__=="__main__":
    repos=[
        ("python/cpython",77898),
        ("pallets/flask",71000)
    ]
    export_to_csv("ranking.csv",repos)