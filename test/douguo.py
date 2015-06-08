# _*_ coding:utf-8 _*_
"""
Created on 2015-06-07

@author: lujin
"""
from bs4 import BeautifulSoup
import requests
import pymongo
import time


def get_db():
    conn = pymongo.MongoClient('127.0.0.1')
    return conn['db_douguo']


def get_html(url):
    response = requests.get(url)
    content = response.content.decode('utf-8')
    return content


def parser_fenlei(content):
    soup = BeautifulSoup(content)
    types = soup.find_all('h2')
    db = get_db()
    i = 0
    for ul in soup.find_all('ul', class_='kbi'):
        tp = types[i].contents[0]
        i += 1
        for a in ul.find_all('a'):
            doc = {
                'href': a.get('href'),
                'name': a.contents[0],
                'type': tp,
                'page': 0
            }
            db.c_category.insert(doc)


def parser_fenlei_detail(offset, cate, collection):
    url = 'http://www.douguo.com/uajax/getMoreCaipu'
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    data = {'offset': offset, 'cate': cate}
    try:
        resp = requests.post('http://www.douguo.com/uajax/getMoreCaipu', data=data, headers=headers)
    except:
        return False
    if resp.status_code == 200:
        try:
            content = resp.content.decode('utf-8')
            # print(content)
            if content is None:
                return False
            else:
                soup = BeautifulSoup(content)
                for div in soup.find_all('div', class_='course'):
                    h3 = div.find('h3')
                    link = h3.a.get('href')
                    name = h3.a.contents
                    print(link)
                    print(name[0])
                    p = div.find('p', class_='fcc')
                    print(p.contents[-1])
                    doc = {
                        'link': link,
                        'name': name[0],
                        'create_date': p.contents[-1],
                        'status': 0,
                        'type': cate
                    }
                    collection.insert(doc)
                    print('=================================================')
        except:
            return False
    else:
        return False

    return True


if __name__ == '__main__':
    # 获取菜谱类别
    # url = 'http://www.douguo.com/caipu/fenlei'
    # content = get_html(url)
    # parser_fenlei(content)

    # 解析类别
    db = get_db()
    # results = db.c_caipu_map.find()
    # for result in results:
    #     db.c_caipu_map.update({'_id': result['_id']}, {"$set": {'status': 0, 'type': '家常菜'}})
    results = db.c_category.find()
    for result in results:
        hasMore = True
        page = result['page']
        if page == 0:
            parser_fenlei_detail(0, result['name'], db.c_caipu_map)
            parser_fenlei_detail(12, result['name'], db.c_caipu_map)
            db.c_category.update({'_id': result['_id']}, {'$set': {'page': 0}})
            page += 1

        while hasMore:
            print('解析第' + str(page) + '页...')
            hasMore = parser_fenlei_detail(30 + 30 * page, result['name'], db.c_caipu_map)
            page += 1
            db.c_category.update({'_id': result['_id']}, {'$set': {'page': page}})
            print('解析结束...')
            print('sleep...')
            time.sleep(10)
