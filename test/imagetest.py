import pymongo
import requests

__author__ = 'sunshine'

def get_db():
    conn = pymongo.MongoClient('127.0.0.1')
    return conn['db_douguo']

if __name__ == '__main__':
    # resp = requests.get('http://cp1.douguo.net/upload/caiku/b/c/d/yuan_bcda0919d4fdaa0c56bed17586b810bd.jpg')
    # with open(r'E:\123.jpg', 'wb') as f:
    #     f.write(resp.content)
    db = get_db()
    rs = db['c_caipu_map.c_caipu_map'].find()
    for r in rs:
        link = r['link']
        rr = db.c_caipu_map.find_one({'link': link})
        if not rr:
            doc = {
                'link': link,
                'create_date': r['create_date'],
                'type': r['type'],
                'name': r['name'],
                'status': 0
            }
            db.c_caipu_map.insert(doc)
        else:
            print('菜谱已存在...')

