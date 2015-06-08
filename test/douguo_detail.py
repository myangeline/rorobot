# _*_ coding:utf-8 _*_
from bs4 import BeautifulSoup
import pymongo
import requests

__author__ = 'sunshine'


def get_db():
    conn = pymongo.MongoClient('127.0.0.1')
    return conn['db_douguo']


def get_html(url):
    response = requests.get(url)
    content = response.text
    return content


def parser_detail(content):
    soup = BeautifulSoup(content)
    fullStory = soup.find('div', attrs={'id': 'fullStory'})
    # 描述
    desc = fullStory.contents[0].strip()
    print(desc)
    mtim = soup.find('tr', class_='mtim')
    # print(mtim.contents)
    tds = 0
    print(mtim.find_all('td')[0])
    for td in mtim.find_all('td'):
        print(td.contents[-1].strip())


if __name__ == '__main__':
    url = 'http://www.douguo.com/cookbook/1190382.html'
    content = get_html(url)
    parser_detail(content)