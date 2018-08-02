from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from random import sample
import jieba
from wordcloud import WordCloud
import wordcloud
# 设置中文字体
matplotlib.rcParams['font.family']='SimHei'
matplotlib.rcParams['font.size']=20

def show(request):
    cate = request.GET.get('cate')
    if cate:
        cate = int(cate)
        start_price = int(request.GET.get('start_price'))
        end_price = int(request.GET.get('end_price')) if request.GET.get('end_price') else 50000
        start_sale = int(request.GET.get('start_sale'))
        end_sale = int(request.GET.get('end_sale')) if request.GET.get('end_sale') else 2000000
        cate_data = loadData()
        cate_name = ["phone", "headset", "speakers", "bracelet", "computer"]
        Cate = cate_data[cate_name[cate]]
        word(Cate)
        sale_price_scatter(Cate, start_price, end_price, start_sale, end_sale)
        res = {
            "word": "/media/word.jpg",
            "scatter": "/media/scatter.jpg",
            "price": "/media/pie/%s_price.png" % cate_name[cate],
            "sale": "/media/pie/%s_sale.png" % cate_name[cate],
            "cate": cate,
            "start_price": start_price,
            "end_price": end_price,
            "start_sale": start_sale,
            "end_sale": end_sale,
        }
        return render(request, 'show.html', res)
    else:
        return render(request, 'show.html')
        
    

def loadData():
    skiprows=[360, 7698, 10313, 11196, 15529, 15790, 25505, 25727, 27839]
    def convert_fun(name):
        convert = {
            '': '',
            '暂无报价': 0,
        }
        if name in convert:
            return convert[name]
        else:
            return name
        
    convert_dict = dict(zip(range(1,7), [convert_fun]*7), )

    data = pd.read_csv('30000.csv', skiprows=skiprows, converters=convert_dict) 
    data.price = data.price.astype(np.float)
    data['sale'] = 0
    # 销售量转换
    def trans_sale(remark):
        remark = str(remark).strip(' ')
        # 去掉 +
        remark = remark.replace('+', '')
        
        if '万' in remark:     
            remark = float(remark[:-1]) * 10000        # 有万,剩10000倍
        else:
            remark = float(remark)                     # 没有万,直接转换
        return remark
    data.sale = data['remark_count'].map(trans_sale)

    # 分离五类商品
    cate_data = {}
    cate_data["phone"] = data[data.category=='手机']
    cate_data["headset"] = data[data.category=='耳机']
    cate_data["speakers"] = data[data.category=='音箱']
    cate_data["bracelet"] = data[data.category=='手环']
    cate_data["computer"] = data[data.category=='笔记本']

    return cate_data


def word(cate):
    title_s = ''
    for name in cate.name:
        title_s += ' '.join(jieba.cut(name))
    
    pic = plt.imread("media/computer.png")
    wc = WordCloud(
        background_color="white", 
        mask=pic,
        max_font_size=150, 
        max_words = 200,
        stopwords = wordcloud.STOPWORDS | {"手机", "耳机", "音箱", "手环", "笔记本", "电脑", "笔记本电脑"},
        font_path = "C:\Windows\Fonts\simkai.ttf",
        random_state = 30,
        scale = 2.5,
    )
    wc.generate_from_text(title_s)
    
    plt.figure(figsize=(5,4), dpi=80)
    plt.title("词云")
    plt.imshow(wc)
    plt.axis("off")
    wc.to_file("media/word.jpg")
    plt.close()


# 绘制 销售量-价格 散点图
def sale_price_scatter(cate, start_price=0, end_price=50000, start_sale=0, end_sale=2000000):
    cate = cate[cate.price>start_price][cate.price<end_price][cate.sale>start_sale][cate.sale<end_sale]
    plt.figure(figsize=(10,8), dpi=80)
    plt.scatter(cate.price, cate.sale, marker='.')
    plt.title("销售-价格散点图")
    plt.xlabel("价格")
    plt.ylabel("销售量")
    plt.savefig("media/scatter.jpg")
    plt.close()