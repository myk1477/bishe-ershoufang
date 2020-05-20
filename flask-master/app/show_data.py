import pandas as pd
# 导入 MongoDB 实例和 加载CSV文件后的实例
from mange import df,collection
from flask import render_template, request, jsonify

from datas import get_data
from . import api

@api.route('/show_data',methods=['GET'])
def get_map():

    return render_template('show_data.html')

# 下来框 三级联动
# 获取区的信息
@api.route('/get_district',methods=["GET"])
def get_district():
    '''
    异步 获取 区的数据
    :return:
    '''
    # 获取 区 的 名称
    area_name = list(df['areaName'].value_counts().keys())

    return jsonify({"area":area_name})

@api.route('/get_district/areas',methods=["POST"])
def get_areas():
    '''
    根据前端所传内容 获取 街道获取小区内容
    :return: 
    '''
    # 获取 参数
    data_json = request.get_json()
    areaName = data_json.get('areaName')
    street = data_json.get('street')

    if not  areaName:
        return jsonify({"area":''})
    elif not street:
        return jsonify({"area":''})
    # 根据 参数获取获取 相应的 行
    if street and street != '0':
        # 删选出指定的值对应的行 当时多个条件的时候使用的连接符
        data = df[(df['areaName']==areaName)&(df['street']==street)]
        area_name = list(data['communityName'].value_counts().keys())
    else:
        data = df[df['areaName'] == areaName]
        area_name = list(data['street'].value_counts().keys())

    # 返回响应
    return jsonify({"area":area_name})

@api.route('/home/getHomeInfo',methods=['GET'])
def getHomeInfo():
    '''
    获取表格所需的数据
    :return: 
    '''
    #  获取请求参数
    data = request.args
    pageSize = int(data.get('pageSize'))
    page = int(data.get('page'))
    select_district = data.get('select_district')
    select_street = data.get('select_street')
    select_plot = data.get('select_plot')
    sort = data.get('sort')
    skip = pageSize * (page - 1)
    try:
        if select_street or select_district or select_plot:
            # select_street if select_street else {"$regex":".*"} 表达式的含义为 若是 select_street 存在 则返回 select_street 不存在则返回else后面的内容
            # 若是有查询条件全不为空
            res = collection.find({'street':select_street if select_street else {"$regex":".*"},
                                       'house_info_dict.所在区域':select_district if select_district else {"$regex":".*"},
                                                                                 'house_info_dict.小区名称':select_plot if select_plot else {"$regex":".*"}})

            total = res.count()
            if sort != '_id':
                sort = 'house_info_dict.' + sort
            res = res.skip(skip).limit(pageSize).sort(sort)
        else:
            # 若是 查询条件全部为空
            res = collection.find()
            # 求出总数据量
            total = res.count()
            if sort != '_id':
                sort = 'house_info_dict.'+ sort
            res = res.skip(skip).limit(pageSize).sort(sort)
    except Exception as e:
        res = ''
        return jsonify(res)

    # 构造响应数据  total 为 总数据量 page 为 一页数据
    page = []
    for data  in  res:
        page.append({'detail_url':data.get('detail_url'),'street':data.get('street'),
                     'communityName':data['house_info_dict'].get('小区名称'),'areaName':data['house_info_dict'].get('所在区域'),
                     'unitPriceValue':data['house_info_dict'].get('单价'),'total':data['house_info_dict'].get('总价'),
                     'jzmj':data['house_info_dict'].get('建筑面积'),'fwhx':data['house_info_dict'].get('房屋户型'),'szlc':data['house_info_dict'].get('所在楼层'),
                     'fwcx':data['house_info_dict'].get('房屋朝向'),'zxqk':data['house_info_dict'].get('装修情况'),'thbl':data['house_info_dict'].get('梯户比例')})

    return jsonify({'total':total,'rows':page})

