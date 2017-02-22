#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time

url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'
urls = ['https://cn.tripadvisor.com/Attractions-g60763-Activities-oa{}-New_York_City_New_York.html'.format(str(s)) for s in range(00, 1080, 30)]

def get_attractions(url, data=None):
    web_data = requests.get(url)
    #web_data
    time.sleep(2)
    soup = BeautifulSoup(web_data.text, features='lxml')
    titles = soup.select('div.property_title > a[target="_blank"]')
    imgs = soup.select('img[width="160"]')
    cates = soup.select('div.p13n_reasoning_v2')  
    for title, img, cate in zip(titles, imgs, cates):
        data = {
                'title': title.get_text(),
                'img': img.get('srt'),
                'cate': list(cate.stripped_strings),
        }
        #print(data['cate'][0])

for each_url in urls:
    get_attractions(each_url)


print "hello world"
    

