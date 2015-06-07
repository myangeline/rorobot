# _*_ coding:utf-8 _*_
"""
Created on 2015-06-07

@author: lujin
"""
from bs4 import BeautifulSoup
import requests


def get_html(url):
    response = requests.get(url)
    content = response.content.decode('utf-8')
    return content


def parser_fenlei(content):
    soup = BeautifulSoup(content)
    categorys = []
    for ul in soup.find_all('ul', class_='kbi'):
        for a in ul.find_all('a'):
            category = dict()
            category['href'] = a.get('href')
            category['name'] = a.contents[0]
            categorys.append(category)
    print(categorys)


def parser_fenlei_detail(content):
    pass


if __name__ == '__main__':
    url = 'http://www.douguo.com/caipu/fenlei'
    content = get_html(url)
    parser_fenlei(content)