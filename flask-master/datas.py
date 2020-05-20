#!/usr/bin/env python
#coding=utf-8
import pandas as pd

# 获取 二手房源的 数据
def get_data():
    # 自定义 数据的行列索引（行索引使用pd默认的，列索引使用自定义的）
    names = [
        "communityName", "areaName", "street", "total", "unitPriceValue",
        "fwhx", "szlc", "jzmj", "hxjg", "tnmj",
        "jzlx", "fwcx", "jzjg", "zxqk", "thbl",
        "pbdt", "gpsj", "jyqs", "scjy","fwyt",
        'gzrs',"fwnx", "cqss", "dyxx", "fbbj",
    ]
    # 自定义需要处理的缺失值标记列表
    miss_value = ["null", "暂无数据"]
    filename = '../data_file/ershoufang3.csv'
    # 读取文件
    df = pd.read_csv(filename, skiprows=[0], names=names, na_values=miss_value, encoding="gbk")
    # 把 面价大于1000的给去掉
    df = df[df['jzmj']<1000]
    return df
