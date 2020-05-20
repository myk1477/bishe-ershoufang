import pandas as pd
from mange import df

#  对房屋面积进行切割 返回切割后的数据
def split_area():

    # 构造切割的范围和 显示的标签
    area_level = [0, 50, 100, 150, 200, 250, 300, 500]
    label_level = ['小于50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350']

    # 使用 cut 对数据 进行分段分组 对 数据的 jzmj 字段 按照 area_level 进行分段
    # 参数 labels 是 对分段后的每个区间打上标签
    jzmj_cut = pd.cut(df["jzmj"], area_level, labels=label_level)

    return jzmj_cut

# 对于 price_element.py 中 构造 返回数据
def response_data(datas):
    # names 为 前端option的x轴所需要的数据 data 为 series 中所需要的数据
    names = []
    data = []
    for name,value in datas.items():
        if name != '未知 ':
            names.append(name)
            data.append(int(value))
    return {"names":names,"data":data}


# 对于 热门分析中的郑州房源大致展示
def house_info():
    # 房源的平均总价
    total_mean = int(df['total'].mean())
    # 房源的平均单价
    unitPriceValue_mean = int(df['unitPriceValue'].mean())
    # 房源你的平均建筑面积
    jzmj_mean = int(df['jzmj'].mean())
    # 房屋总数
    nums = df['total'].count()
    context = {
        'attentions': [
            {
                'counts': str(nums) + '套',
                'plot': '获取的房源总数'
            },
            {
                'counts': str(unitPriceValue_mean) + '元/平米',
                'plot': '获取的房源平均单价'
            },
            {
                'counts': str(total_mean) + '万元',
                'plot': '获取的房源平均总价'
            },
            {
                'counts': str(jzmj_mean) + '㎡',
                'plot': '获取的房源平均建筑面积'
            }
        ]}
    return context