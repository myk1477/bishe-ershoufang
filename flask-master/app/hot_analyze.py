import pandas as pd
# 导入 MongoDB 实例和 加载CSV文件后的实例
from mange import df
from flask import render_template, request, jsonify
from utils import house_info
from datas import get_data
from . import api
import operator

@api.route('/hot',methods=['GET'])
def get_hot():
    area_name = list(df['areaName'].value_counts().keys())
    context = house_info()
    context['area'] = area_name
    return render_template('hot_analyze.html',**context)

@api.route('/get_attentions',methods=['POST'])
def get_house_nums():
    # 获取 参数
    area = request.get_json().get('areaName')
    if not area:
        context = house_info()
        return render_template('analyse/ajax_receive.html',**context)
    data_attentions = df[df.areaName == area]
    groups_gzrs = data_attentions["gzrs"].groupby(data_attentions["communityName"])
    count_gzrs = groups_gzrs.sum()
    # 对 count_gzrs 进行排序 按照 值  获取前五个
    # sort_values（）与 sort_index（）分别按照值、索引进行排序
    # ascending参数默认为True，对values升序排序；
    datas = count_gzrs.sort_values(ascending=False)[:5]

    attentions = []
    for k,v  in  datas.items():
        attentions.append({ 'counts': str(v) + '人','plot': k})
    print(attentions)
    context = {
        'attentions':attentions
    }
    return render_template('analyse/ajax_receive.html',**context)

@api.route('/get_ciyun',methods=['GET'])
def get_ciyun():
    '''
    异步获取生成词云图所需要的数据
    :return: 
    '''
    # 按照户型分组 统计热度
    groups_fwhx = df["gzrs"].groupby(df["fwhx"])
    count_fwhx = groups_fwhx.sum().sort_values(ascending=False)[:30]
    data = []
    for k, v in count_fwhx.items():
        if v != 0:
            data.append({'name': k, 'value': v})
    # 热门分析的初始值 即 郑州市 关注度高的 五个 城区
    groups_gzrs = df["gzrs"].groupby(df["areaName"])
    count_gzrs = groups_gzrs.sum()
    datas = count_gzrs.sort_values(ascending=False)[:5]
    price_mean = []
    area_mean = []
    for k in datas.keys():
        price_mean.append(int(df[df['areaName'] == k]['unitPriceValue'].mean()))
        area_mean.append(int(df[df['areaName'] == k]['jzmj'].mean()))
    print(data)
    return jsonify({'ciyun_data':data,'x_data': list(datas.keys()),
                    'price_mean': price_mean, 'area_mean': area_mean})


@api.route('/get_hot_histogram',methods=['POST'])
def get_hot_histogram():
    '''
    异步获取 热门分析中的柱状图所需要的数据
    :return: 
    '''
    area = request.get_json().get('areaName')
    if not area:
        # 若是 没有区域的名字 则获取 人气最高的几个区
        # 按照区域名字对关注热度字段进行分组
        groups_gzrs = df["gzrs"].groupby(df["areaName"])
        count_gzrs = groups_gzrs.sum()
        # 找出关注度最高的前五个区
        datas = count_gzrs.sort_values(ascending=False)[:5]
        price_mean = []
        area_mean = []
        # 构造返回的数据
        for k in datas.keys():
            price_mean.append(int(df[df['areaName'] == k]['unitPriceValue'].mean()))
            area_mean.append(int(df[df['areaName'] == k]['jzmj'].mean()))
        return jsonify({'x_data': list(datas.keys()), 'price_mean': price_mean, 'area_mean': area_mean})
    else:
        # 首选从数据中筛选出符合前端所传递的区县
        data_attentions = df[df.areaName == area]
        # 对筛选后的数据按照小区的名字对关注热度字段进行分组
        groups_gzrs = data_attentions["gzrs"].groupby(data_attentions["communityName"])
        count_gzrs = groups_gzrs.sum()
        datas = count_gzrs.sort_values(ascending=False)[:5]
        price_mean = []
        area_mean = []
        for k in datas.keys():
            price_mean.append(int(df[df['communityName'] == k]['unitPriceValue'].mean()))
            area_mean.append(int(df[df['communityName'] == k]['jzmj'].mean()))
        print(price_mean)
        return jsonify({'x_data': list(datas.keys()), 'price_mean': price_mean, 'area_mean': area_mean})
    # 对 count_gzrs 进行排序 按照 值  获取前五个
    # sort_values（）与 sort_index（）分别按照值、索引进行排序
    # ascending参数默认为True，对values升序排序；


