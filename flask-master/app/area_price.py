import pandas as pd
from mange import df,redis_cli
from flask import render_template, request, jsonify
from . import api

@api.route('/area_price',methods=['GET'])
def get_area_price():
    '''
    渲染 影响价格因素的页面
    :return: 
    '''

    return render_template('area_price.html')

@api.route('/get_area_price',methods=['GET'])
def set_area_price_data():
    '''
    异步 获取 影响价格因素的页面 所需的散点图
    :return: 
    '''
    cache_data = redis_cli.get('price_splashes')
    if cache_data:
        data_dict = eval(cache_data.decode())
        return jsonify(data_dict)
    else:
        # 单价 相关数据
        unit_dict = df[['jzmj', 'unitPriceValue']].to_dict(orient='records')
        unit_price = []
        for value in unit_dict:
            unit_price.append([value['jzmj'], value['unitPriceValue']])

        # 总价相关数据
        total_dict = df[['jzmj', 'total']].to_dict(orient='records')
        total_price = []
        for value in total_dict:
            total_price.append([value['jzmj'], value['total']])
        data_dict = {"total_price":total_price,"unit_price":unit_price}
        redis_cli.set('price_splashes',str(data_dict))
        return jsonify(data_dict)