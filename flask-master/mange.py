#!/usr/bin/python
# coding=utf-8

from flask import Flask
from flask_compress import Compress
# 导入 redis的 扩展
# from redis import StrictRedis
from datas import get_data
# 导入蓝图
from app import api
from redis import StrictRedis
# 连接 MongoDB
from pymongo  import MongoClient
from config import DB,COLLECTION,MONGODB_HOST,MONGODB_PORT
# 创建 flask 实例
app = Flask(__name__)
Compress(app)
# 加载配置文件
app.config.from_object('config')
client = MongoClient(host=MONGODB_HOST,port=MONGODB_PORT)
collection = client[DB][COLLECTION]
# 获取 二手房源数据
df = get_data()
redis_cli = StrictRedis(db=3)
# 注册蓝图
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(threaded=True)