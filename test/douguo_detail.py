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
    table = soup.find('table', class_='retamr')
    tr = table.find_all('tr', class_='mtim')
    size = len(tr)
    tr0 = tr[0].find_all('td')
    difficulty = tr0[0].contents[-1].strip()
    time = tr0[1].contents[-1].strip()
    print(difficulty)
    print(time)

    tr1 = tr[1].find_next_sibling()
    print(tr1)
    # for tr in soup.find_all('tr', class_='mtim'):
    #     tds = mtim.find_all('td')
    #     difficulty = tds[0].contents[-1].strip()
    #     time = tds[1].contents[-1].strip()
    #     print(difficulty)
    #     print(time)


if __name__ == '__main__':
    url = 'http://www.douguo.com/cookbook/1190382.html'
    content = get_html(url)
    parser_detail(content)