# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv,os
import logging
from pymongo import MongoClient
from LianjiaSpider.spiders.utils import total_price_turn,unit_price_turn,area_unit_remove

# 从配置文件中导入 连接 MongoDB 所需的参数
from LianjiaSpider.settings import HOST,PORT,TEST_DB_NAME,DB_NAME,COLLECTION
class MongodbPipeline(object):
    def open_spider(self, spider):  # 在爬虫开启的时候仅执行一次
        # 连接 MongoDB
        self.client = MongoClient(host=HOST,port=PORT)
        # 选择 测试所用的 数据库和集合
        self.db = self.client[TEST_DB_NAME]
        self.col = self.db[COLLECTION]
        # 选择 真正保存数据的数据库和集合
        # self.db = self.client[DB_NAME]
        # self.col = self.db[COLLECTION]

    def process_item(self, item, spider):
        # 把 item 转成 字典, 因为 在 items.py 文件中进行了 建模 此时 这个参数item 是一个模型对象
        # 在 scrapy 可以 直接把这个 模型对象转成字典的
        item = dict(item)
        # 把数据 插入到 MongoDB 数据库中 使用 更新 若是 这条数据 在数据库中不存在就插入,存在就更新
        self.col.update(item,{'$set':item},upsert=True)
        # self.col.insert(item)
        return item

    def close_spider(self, spider):  # 在爬虫关闭的时候仅执行一次
        # 关闭和 MongoDB 的连接
        self.client.close()

# 创建一个 管道 把数据保存到 CSV 文件中
class  CsvPipeline(object):
    data_header = [
        "小区名称", "所在区域", "街道", "总价(万元)", "单价(元/平米)",
        "房屋户型", "所在楼层", "建筑面积(㎡)", "户型结构",
        "套内面积(㎡)", "建筑类型", "房屋朝向", "建筑结构",
        "装修情况", "梯户比例", "配备电梯", "挂牌时间",
        "交易权属", "上次交易", "房屋用途","关注人数",
        "房屋年限", "产权所属", "抵押信息", "房本备件",
    ]
    def open_spider(self, spider):  # 在爬虫开启的时候仅执行一次
        file = '..\data_file\ershoufang_demo.csv'
        if not os.path.isfile(file):
            with open(file,'w',newline='') as f:

                # 基于上面创建的文件对象 构建 CSV 写入对象
                writer = csv.writer(f)
                #  构建表头
                writer.writerow(self.data_header)
                # 创建一个文件对象
        else:
            self.f = open(file, 'a',newline='')
            self.writer = csv.writer(self.f)
    def process_item(self, item, spider):
        item = dict(item)
        data = []
        print(item)
        for i in range(len(self.data_header)):
            try:
                if i == 2:
                    data.append(item['street'])
                elif i == 3:
                    # 把价格后面的单位去掉
                    total_price = total_price_turn(item['house_info_dict']['总价'])
                    if total_price:
                        data.append(total_price)
                    else:
                        data = []
                        break
                elif i == 4:
                    unit_price = unit_price_turn(item['house_info_dict']['单价'])
                    if unit_price:
                        data.append(unit_price)
                    else:
                        data = []
                        break
                elif i == 7:
                    # 把 面积后面的单位去掉
                    area_unit = area_unit_remove(item['house_info_dict']['建筑面积'])
                    if area_unit:
                        data.append(area_unit)
                elif i == 9:
                    tn_area = area_unit_remove(item['house_info_dict']['套内面积'])
                    if tn_area:
                        data.append(tn_area)
                    else:
                        data = []
                        break
                else:
                    data.append(item['house_info_dict'][self.data_header[i]])
            except Exception as e:
                logging.error('{} save CSV Field error'.format(item['detail_url']))
                data = []
                # 若是 出现错误则 退出循环
                break
        if  data:
            #  若是 data 不为空则 把数据 存到 CSV 文件中
            print(data)
            self.writer.writerow(data)
        return item

    def close_spider(self, spider):  # 在爬虫关闭的时候仅执行一次
       self.f.close()