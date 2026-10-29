#集中管理配置
import os
#os.getenv("REQUEST_TIMEOUT","10") 
#作用:从操作系统的环境变量中寻找REQUEST_TIMEOUT,如果电脑没有设置这个变量就默认返回"10"
DEFULT_TIMEOUT=10
try: 
    REQUEST_TIMEOUT=int(os.getenv("REQUEST_TIMEOUT","10"))
except ValueError:
    REQUEST_TIMEOUT=DEFULT_TIMEOUT
else:
    if REQUEST_TIMEOUT<=0:
        REQUEST_TIMEOUT=DEFULT_TIMEOUT