from flask import Blueprint


# 创建蓝图
api = Blueprint('api',__name__)

# 把使用蓝图对象的文件，导入到创建蓝图对象的下面  防止循环导包
from . import analyze,price_element,area_price,show_data,hot_analyze