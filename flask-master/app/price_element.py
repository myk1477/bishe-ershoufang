import re
import time
import random
import operator
import pandas as pd
import jieba.analyse
from mange import df
from flask import render_template, request, jsonify

from utils import split_area,response_data

from . import api
# 影响房屋的价格 的因素

@api.route('/price_element',methods=['GET'])
def get_price_element():
    '''
    展示出 影响房屋的价格 的因素的页面
    :return: 
    '''

    return render_template('price_element.html')

@api.route('/get_element',methods=['GET'])
def set_price_element():
    '''
    异步获取 影响房屋的价格 的数据
    :return: 
    '''
    # 户型对价格的影响
    # 户型数量前十的
    fwhx_10 = df['fwhx'].value_counts()[:8].keys()

    # 构造返回数据
    data_fwhx = []
    for fwhx in fwhx_10:
        df1 = df[df['fwhx'] == fwhx]['unitPriceValue'].mean()
        data_fwhx.append({"name": fwhx, "value": int(df1)})
    data_fwhx = sorted(data_fwhx, key=operator.itemgetter('name'))
    names = []
    data = []
    for data_dict in data_fwhx:
        names.append(data_dict['name'])
        data.append(data_dict['value'])
    return jsonify({"names":names,"data":data})

@api.route('/get_element',methods=['POST'])
def select_element():
    # 获取 参数
    element = request.get_json().get('element')
    if not element:
        return jsonify({"data":0})
    if element == 'jzmj':
        jzmj_cut = split_area()
        # 对数据按照 分段后的 建筑面积进行分组,并且对每一个分组的unitPriceValue求出其平均值
        area_price = df.groupby(jzmj_cut).agg({"unitPriceValue": "mean"})
        # 构造放回的数据
        data = response_data(area_price['unitPriceValue'])
    elif element == 'szlc':
        # 获取 不同楼层的平均房价
        floor_price = df.groupby(df[element].apply(lambda x: x[:3])).agg({"unitPriceValue": "mean"})
        data = response_data(floor_price['unitPriceValue'])

    elif element == 'zxqk':
        fitment_price = df.groupby(df[element]).agg({"unitPriceValue": "mean"})
        data = response_data(fitment_price["unitPriceValue"])
    else:
        area_price = df.groupby(df[element]).agg({"unitPriceValue": "mean"})
        data = response_data(area_price["unitPriceValue"])
    return jsonify(data)

