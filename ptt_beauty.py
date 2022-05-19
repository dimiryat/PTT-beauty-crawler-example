# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:31:13 2022

@author: DennisLin
"""

from bs4 import BeautifulSoup
import re
import os
import urllib.request
from ptt_gossiping import *
import time
import requests

def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id="main-content").find_all('a')
    img_urls = []
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls

def save(img_urls, title):
    if img_urls:
        try:
            dname = title.strip()
            os.makedirs(dname)
            for img_url in img_urls:
                if img_url.split("//")[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                fname = img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
        except Exception as e:
            print(e)
            
if __name__=="__main__":
    current_page = get_web_page(PTT_URL + '/bbs/Beauty/index.html')
    if current_page:
        articles = []
        date = time.strftime("%m/%d").lstrip('0')
        current_articles, prev_url = get_articles(current_page, date)
        while current_articles:
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, date)
            
        for article in articles:
            print('Processing', article)
            page = get_web_page(PTT_URL + article['href'])
            if page:
                img_urls = parse(page)
                save(img_urls, article['title'])
                article['num_image'] = len(img_urls)
                
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, sort_keys=True, ensure_ascii=False)