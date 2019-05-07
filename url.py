import requests
# 目标url
import time
import pandas as pd
import random
from math import isnan
print('************version 0.1************')
print('************owner:xuejame**********')
print('*****contact:xuejame@gmail.com*****')
print('修复：1、不能插入空格2、如果无法获取库存，则设为空替代无法获取3、加入反爬虫，使用多uer_agent4、去掉了没用的user_agent')
print('成功读取文件！')



all = pd.read_csv('url.csv',encoding='gb2312')
local_time = time.strftime('%D')
list = all['url']
stock = []
USER_AGENT_LIST = \
    [
    'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
    'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
    'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
    'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
    'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
    'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
]
for start_url in list:
    #判断是不是空的url
    if type(start_url)==float and isnan(start_url):
        print('当前行没有url')
        stock.append(None)
        continue
    
    
    # 自定义headers
    user_agent = random.choice(USER_AGENT_LIST)
    headers = {
               "User-Agent": user_agent,
               "X-Requested-With": "XMLHttpRequest"
               }

    try:
        response = requests.get(url=start_url, headers=headers,timeout = 500)
        # print(response.status_code,user_agent)
        start = response.text.find('"stockOnHand":')+14
        for i in range(start,len(response.text)):
            if not response.text[start:i+1].isdigit():
                print(start_url+'的库存为：',int(response.text[start:i]))
                stock.append(int(response.text[start:i]))
                break
    except:
        print('网页 '+start_url+' 无法读取 or  没有库存  or  agent:'+user_agent)
        stock.append(None)
        continue

all['stock_'+local_time]=stock
name = all.columns.values.tolist()
if 'sales_'+local_time not in all:
    all['sales_'+local_time] = all[name[-3]] - all[name[-1]]
else:
    all['sales_' + local_time] = all[name[-4]] - all[name[-2]]

all.to_csv('url.csv',encoding='gb2312',index=None)


#输出
print('操作完成,移步查看url.csv文件')
print('添加网址,只需增加一行名字和url')
print('5分钟后该程序自动关闭...')
time.sleep(300)