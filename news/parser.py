from datetime import datetime
from urllib.parse import urlparse
from django.core.files.base import ContentFile
import requests
from bs4 import BeautifulSoup
from .models import *

HOST = 'https://kgd.ru'
URL = 'https://kgd.ru/news'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
           'accept': '*/*'
           }
def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req

def get_img(item):
    link = HOST + item.find('div', class_='catItemTitle').find('a').get_attribute_list(key='href')[0]
    html = get_html(link)
    soup = BeautifulSoup(html.text, 'html.commands')
    item = soup.find('div', class_='itemImageBlock')
    if item == None:
        return 'None'
    else:
        return HOST + item.find('img').get_attribute_list(key='src')[0]

def get_text_(item):
    link = HOST + item.find('div', class_='catItemTitle').find('a').get_attribute_list(key='href')[0]
    html = get_html(link)
    soup = BeautifulSoup(html.text, 'html.commands')
    item = soup.find('div', class_='itemFullText js-mediator-article').get_text(strip=True)
    return item

def get_slug(item):
    link = HOST + item.find('div', class_='catItemTitle').find('a').get_attribute_list(key='href')[0]
    return urlparse(link).path.split('/')[-1]

def get_date_time(item):
    i = item.find('span', class_='catItemDateCreated').get_text(strip=True).split(' ')
    date = i[0].split('.')
    date.reverse()
    time = i[-1].split(':')
    res = date+time
    data_ = datetime(int(res[0]), int(res[1]), int(res[2]), int(res[3]), int(res[4]), 0, 0)
    print(data_)
    return data_

def get_content(html):
    soup = BeautifulSoup(html, 'html.commands')
    items = soup.find_all('div', class_='itemContainer itemContainerLast')
    data = []
    t = 0
    for i in items:
        if t>3:
            break
        data.append({
            'title': i.find('div', class_='catItemTitle').get_text(strip=True),
            'text': get_text_(i),
            'img': get_img(i),
            'slug': get_slug(i),
            'datetime': get_date_time(i)
        })
        t+=1
    return data

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        data = get_content(html.text)
        for i in range(len(data)):
            img_name = urlparse(data[i]['img']).path.split('/')[-1]
            p = requests.get(data[i]['img'])
            print(data[i]['datetime'])
            new_post = NewPost(pub_date=data[i]['datetime'])
            new_post.title = data[i]['title']
            new_post.slug = data[i]['slug']
            new_post.text = data[i]['text']
            new_post.img.save(img_name, ContentFile(p.content), save=True)
            new_post.cat_id = 7
            new_post.save()
            print('OK')
    else:
        print('status code is not 200')

parse()