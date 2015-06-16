# _*_ coding:utf-8 _*_
from bs4 import BeautifulSoup
import pymongo
import requests
import time

__author__ = 'sunshine'


def get_db():
    conn = pymongo.MongoClient('127.0.0.1')
    return conn['db_douguo']


def get_html(url):
    response = requests.get(url)
    content = response.text
    return content


def load_image(path, url):
    resp = requests.get(url, timeout=10)
    with open(path, 'wb') as f:
        f.write(resp.content)


def parser_detail(url, content, date, tag, collection):
    soup = BeautifulSoup(content)
    title = soup.find(id='page_cm_id').text
    face = soup.find('div', class_='bmayi mbm').a.get('href')
    load_image('G:\\images\\' + face.split('/')[-1], face)
    fullStory = soup.find(id='fullStory')
    desc = ''
    try:
        if fullStory:
            # 描述
            desc = fullStory.contents[0].strip()
        else:
            desc = soup.find('div', class_='xtip').string.strip()
    except Exception as e:
        print(e)
    table = soup.find('table', class_='retamr')
    tr = table.find_all('tr', class_='mtim')
    difficulty = ''
    time = ''
    ingredient = []
    seasoning = []
    try:
        tr0 = tr[0].find_all('td')
        td0 = tr[0].find('td', class_='lirre')
        hasTime = True
        if td0:
            if td0.span.string == '时间：':
                hasTime = False
                time = td0.contents[-1].strip()
            else:
                difficulty = td0.contents[-1].strip()
        if hasTime:
            time = tr0[1].contents[-1].strip()
        tr1 = tr[1].find_next_siblings()
    except:
        tr1 = tr[0].find_next_siblings()
    print(difficulty)
    isFuliao = False
    for tr in tr1:
        for td in tr.find_all('td'):
            if td.span:
                if isFuliao:
                    right = td.find('span', class_='right').string
                    if right:
                        seasoning.append(td.span.string + '(' + right + ')')
                    else:
                        seasoning.append(td.span.string)
                else:
                    right = td.find('span', class_='right').string
                    if right:
                        ingredient.append(td.span.string + '(' + right + ')')
                    else:
                        ingredient.append(td.span.string)
            else:
                isFuliao = True
                break

    materials = dict()
    materials['ingredient'] = ingredient
    materials['seasoning'] = seasoning
    print(materials)
    div = soup.find('div', class_='step')
    steps = []
    for d in div.find_all('div', class_='stepcont'):
        step = dict()
        if d.a:
            u = d.a.get('href')
            link = u.split('/')[-1]
            load_image('G:\\images\\' + link, u)
        else:
            link = ''
        step['desc'] = d.p.text
        step['link'] = link
        steps.append(step)

    tags = []
    for t in soup.find_all('a', class_='btnta'):
        tags.append(t.string)
    tags.append(tag)
    print(tags)

    tip = soup.find('div', class_='xtieshi')
    tips = ""
    if tip:
        tips = tip.p.text

    doc = {
        'url': url,
        'title': title,
        'face': face.split('/')[-1],
        'desc': desc,
        'difficulty': difficulty,
        'time': time,
        'materials': materials,
        'tags': tags,
        'tips': tips,
        'steps': steps,
        'create_date': date
    }
    print(doc)
    print('解析结束...')
    collection.insert(doc)
    print('数据库操作成功...')


if __name__ == '__main__':
    db = get_db()
    # url = 'http://www.douguo.com/cookbook/1174691.html'
    # parser_detail(url, get_html(url), '2015-10-14', '家常菜', db.c_caipu)
    results = db.c_caipu_map.find({'status': 0}).limit(30)
    print(results.count())
    while results.count() > 0:
        for result in results:
            try:
                url = result['link']
                r = db.c_caipu.find_one({'url': url})
                if not r:
                    print('开始解析菜谱...' + url)
                    print('菜谱名称:' + result['name'])
                    content = get_html(url)
                    date = result['create_date']
                    try:
                        parser_detail(url, content, date, result['type'], db.c_caipu)
                        db.c_caipu_map.update({'_id': result['_id']}, {'$set': {'status': 1}})
                        print('菜谱状态更新成功...')
                    except Exception as e:
                        print(e)
                        db.c_caipu_map.update({'_id': result['_id']}, {'$set': {'status': 2}})
                        with open(r'G:\images\error.txt', 'a+') as f:
                            f.write(url + '\n')
                        print('菜谱解析出错了...')
                    print('菜谱解析结束...')
                    print('=============================================================')
                    print('睡眠10秒...')
                    time.sleep(5)
                else:
                    tags = r['tags']
                    t = result['type']
                    if t not in tags:
                        tags.append(t)
                        db.c_caipu.update({'url': url}, {'$set': {'tags': tags}})
                        print('菜谱标签更新')
                    db.c_caipu_map.update({'_id': result['_id']}, {'$set': {'status': 3}})
                    print('待解析的菜谱已存在...')
            except Exception as e:
                print(e)
        results = db.c_caipu_map.find({'status': 0}).limit(30)