import pandas as pd
from mange import df
from flask import render_template, request, jsonify
import jieba.analyse
from datas import get_data
from . import api
# 获取 面积切割后的数据
from utils import split_area


@api.route('/')
def index():
    """
    首页展示
    """
    return render_template('index.html')

@api.route('/data_analysis')
def hello_world():
    """
    折线图/柱状图页面
    """
    return render_template('data_analysis_index.html')

@api.route('/get_date', methods=["POST"])
def overview_app():
    """
    首页 房源数量折线图异步获取数据
    """
    # 统计 areaName 这一列 中各元素出现的次数 即 统计 每个区有多少房屋因为这一列的元素是区名
    data = df['areaName'].value_counts()
    # 统计 装修 占比数据 用于 前端展示饼状图
    pie_data = count_zxqk = df["zxqk"].value_counts()
    pie_key = []
    pie_value = []
    for key, value in pie_data.items():
        pie_key.append(key)
        pie_value.append(value)
    pie_data = {'key': pie_key, 'value': pie_value}
    # # 所在 楼层情况的 占比
    floor = df['szlc'].apply(lambda x:x[:3]).value_counts()
    floor_list = []
    for k,v in floor.items():
        if k != '未知 ':
            floor_list.append({'name':k,'value':v})
    # 返回的数据是 x_data首页 折线图的x轴数据,data是 y轴的数据, pie_data 是对应的 饼状图所需要的数据
    return jsonify({'x_data':list(data.keys()),'data':list(data),'pie_data':pie_data,"floor":floor_list})



@api.route('/contrast')
def contrast():
    """
    二手房箱线图页面
    """
    # 计算数据

    return render_template('contrast.html')

@api.route('/get_contrast', methods=["POST"])
def contrast_data():
    """
    箱线图异步获取数据
    """
    # 获取 前端发送过来的参数
    price = request.get_json().get('price')

    if not price:
        # 若是 area 参数为 空
        return jsonify({"data":0})

    # 各区域二手房单价箱线图 所需要的数据
    # 数据分组、数据运算和聚合
    unitprice_area = df[price].groupby(df["areaName"])
    # 构造返回给前端的数据
    data = []
    for name, value in unitprice_area:
        data.append({"name": name, "value": list(value)})

    return jsonify({'data':data})


@api.route('/housetype',methods=['GET'])
def housetype():
    """
    显示 户型建筑类型图页面
    """
    return render_template('housetype.html')

@api.route('/get_select',methods=["GET"])
def get_select():
    '''
    异步 获取 区的数据
    :return:
    '''
    # 获取 区 的 名称
    area_name = list(df['areaName'].value_counts().keys())

    return jsonify({"area":area_name})

@api.route('/get_housetype', methods=["POST"])
def get_area_housetype():
    '''
    异步 获取 户型和建筑类型所需要的数据
    :return: 
    '''
    # 获取 参数
    area = request.get_json().get('title')
    if not area:
        # 若是 area 参数为 空
        return jsonify({"data":0})
    if area != "郑州":
        area_df = df[df.areaName==area]
    else:
        area_df = df
    # 获取 户型这一列的种类和数目 获取前十类
    count_fwhx = area_df['fwhx'].value_counts()[:7]
    # 后面的 都用 其他来表示
    count_other_fwhx = pd.Series({"其他": area_df['fwhx'].value_counts()[7:].count()})
    count_fwhx = count_fwhx.append(count_other_fwhx)
    # 构造户型占比的返回数据
    house_type_data = []
    for k, v in count_fwhx.items():
        house_type_data.append({"name": k, "value": v})
    # 获取建筑类型
    count_jzlx = area_df["jzlx"].value_counts()
    # 构造建筑类型的返回数据
    architecture_type_data = []
    for k, v in count_jzlx.items():
        if k == '暂无数据':
            # 若是统计的是暂无数据的 将其转换成 位置
            k = '其他'
        architecture_type_data.append({"name": k, "value": v})
    return jsonify({"house_type_data": house_type_data, 'architecture_type_data': architecture_type_data})


@api.route('/realtime')
def real_time():
    """
        二手房面积页面
    """
    return render_template('realtime.html')

@api.route('/get_item', methods=["POST"])
def get_item():
    """
    异步获取 区域二手房单价和建筑面积的 直方图所需要的数据
    """
    # 获取 直方图的数据

    # 对分段后的数据进行每段数据的统计 并且默认从高到低排序。
    jzmj_cut = split_area()
    jzmj_result = jzmj_cut.value_counts()
    # 构造返回的直方图数据
    data_jz = []
    for k,v  in  jzmj_result.items():
        data_jz.append({"name":k,"value":v})

    # 获取 平均 建筑面积
    groups_unitprice_jzmj = df["jzmj"].groupby(df["areaName"])
    mean_jzmj = groups_unitprice_jzmj.mean()
    data_mean_jzmj = []
    for k,v in mean_jzmj.items():
        data_mean_jzmj.append({"name":k,"value":int(v)})


    # 返回 json 数据
    return jsonify({"data_jz":data_jz,'data_mean_jzmj':data_mean_jzmj})





