# _*_ coding:utf-8 _*_
"""
Created on 2015-05-22

@author: lujin
"""
import pymongo
from config.mongodbconf import MONGODB_NAME, MONGODB_HOST, MONGODB_PORT


def get_db(db=MONGODB_NAME):
    conn = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
    return conn[db]

