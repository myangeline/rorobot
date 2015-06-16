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


def parser_fenlei_detail(offset, cate, db):
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
            # print(len(content))
            if len(content) == 0:
                print('没有更多了...')
                return False
            else:
                soup = BeautifulSoup(content)
                for div in soup.find_all('div', class_='course'):
                    h3 = div.find('h3')
                    link = h3.a.get('href')
                    result = db.c_caipu_map.find_one({'link': link})
                    if not result:
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
                        db.c_caipu_map.insert(doc)
                    else:
                        print('菜谱已存在...')
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
    # db.c_caipu_map.update({'_id': result['_id']}, {"$set": {'status': 0, 'type': '家常菜'}})
    while True:
        try:
            results = db.c_category.find()
            for result in results:
                hasMore = True
                page = result['page']
                if page == 0:
                    parser_fenlei_detail(0, result['name'], db)
                    parser_fenlei_detail(12, result['name'], db)
                    db.c_category.update({'_id': result['_id']}, {'$set': {'page': 0}})
                    page += 1

                while hasMore:
                    print('解析 ' + result['name'] + ' 第' + str(page) + '页...')
                    hasMore = parser_fenlei_detail(30 + 30 * page, result['name'], db)
                    print(hasMore)
                    if not hasMore:
                        break
                    page += 1
                    db.c_category.update({'_id': result['_id']}, {'$set': {'page': page}})
                    print('第' + str(page - 1) + '页的 ' + result['name'] + ' 解析结束...')
                    print('sleeping...10seconds...')
                    time.sleep(10)
                print('解析下一个类别...')
        except Exception as e:
            print(e)
