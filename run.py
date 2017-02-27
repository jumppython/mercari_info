# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import requests
import re
import csv
import locale
import time
from xml.etree import ElementTree as et

categorydict = {"636":u"正月",
                "637":u"成人式",
                "638":u"バレンタインデー",
                "639":u"ひな祭り",
                "640":u"子どもの日",
                "641":u"母の日",
                "642":u"父の日",
                "643":u"サマーギフト／お中元",
                "644":u"夏休み",
                "645":u"ハロウィン",
                "646":u"敬老の日",
                "647":u"七五三",
                "648":u"お歳暮",
                "649":u"クリスマス",
                "650":u"冬一般",}

class Info:
    def __init__(self):
        self.info = dict()
    def _set(self,**args):
        self.info = args
    def _get(self):
        return self.info

class UrlBox(Info):
    def set(self,m_url,m_price):
        self._set(url=m_url,price=m_price)

class ItemInfo(Info):
    def save(self,m_id,m_price,m_area,m_text,m_rote):
        self._set(mid=m_id,price=m_price,area=m_area,text=m_text,rote=m_rote)

def ItemPage(page,mid=None):
    if re.search(r'<section class="items-box-container clearfix">',page):
        urls = re.findall(r'<a href="(https://item.mercari.com/jp/.*?/)">',page)
        prices = [''.join(a[0].split(',')) for a in re.findall(r'<div class="items-box-price font-5">.*?(\d{1,3}(,\d{3})*)</div>',page)]
        return urls, prices
    if re.search(r'<section class="item-box-container">',page):
        info = ItemInfo()
        area = re.findall(r'<a href="https://www.mercari.com/jp/area/\d+?/">(.*?)</a>',page)[0].decode('utf-8').encode('shift-jis')
        try:
            text = re.findall(r'<h2 class="item-name">(.*?)</h2>',page)[0].decode('utf-8').encode('shift-jis')
        except:
            text = ""
        rote = re.findall(r'<span>(\d+?)</span>',page)
        price = re.findall(r'<span class="item-price bold">(.*?)</span>',page)[0]
        price = ''.join(price[2:].split(','))
        info.save(m_id=mid,m_area=area,m_price=price,m_text=text,m_rote=rote[0:3])
        return info

def Spider(url,mid=None):
    try:
        page = requests.get(url).content
    except:
        time.sleep(2)
        page = requests.get(url).content
    return ItemPage(page,mid)

def urlCollecter(categoryId,categoryName):
    urlcollection,pricecollection = [],[]
    if not os.path.isdir("./" + categoryId):
        os.mkdir("./" + categoryId)

    #if os.path.exists("./" + categoryName + "/urllist.csv"):
    #    return

    for page in range(1,101):
        categoryUrl = "https://www.mercari.com/jp/category/" + categoryId + "/?page=" + str(page)
        spiderresult = Spider(categoryUrl)
        urlcollection.append(spiderresult[0])
        pricecollection.append(spiderresult[1])
        print(" - ".join([categoryName,str(page)]))
        time.sleep(3)
    print("category " + categoryName + "urls are collected.")
    with open("./" + categoryId + "/urllist.csv","wb") as uf:
        writer = csv.writer(uf)
        for row in urlcollection:
            writer.writerow(row)
    with open("./" + categoryId + "/pricelist.csv","wb") as pf:
        writer = csv.writer(pf)
        for row in pricecollection:
            writer.writerow(row)

def runUrlCollect():
    global categorydict
    for item in categorydict:
        urlCollecter(item,categorydict[item])



if __name__ == '__main__':
    runUrlCollect()
    
