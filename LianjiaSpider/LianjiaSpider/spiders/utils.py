
import collections

# 因为 区下面的 街道 同一个街道有在多个区下面展示的情况, 所以需要去重
def reduplication_street_url(street_list,street):
    # 若是 不在 这个 街道列表中 则返回这个街道 否则返回 None
    if street not in street_list:
        street_list.append(street)
        return street
    return None

# 数据清洗
# 将房屋基本信息的数据和交易信息的数据 去除里面的特殊字符 以及字符串左右两端的空格
def replaceLine(string):
    try:
        return string.strip().replace('\n','').replace('\t','')
    except:
        return ''

# 把总价后面的单位去掉
def total_price_turn(price):
    try:
        price = price.split('万')[0]
    except Exception:
        return ''
    else:
        # 返回的 item 数据中 总价是 xxx万
        return  price

# 把单价后面的单位给去掉
def unit_price_turn(price):
    try:
        price = price.split('元')[0]
    except Exception:
        return ''
    else:
        # 返回的 item 数据中 总价是 xxx万
        return price

# 把 建筑面积和套间面积的单位去掉
def area_unit_remove(area):
    if area == '暂无数据':
        return area
    try:
        area  = area.split("㎡")[0]
    except Exception:
        return ''
    else:
        return area

# 根据 传递的 街道 的总页数 构造 街道的url列表
def convertUrlList(baseUrl, totalPage):
    count = 1
    res = []
    while count <= totalPage:
        # page = '' if count == 1 else ('pg' + str(count) + '/')
        page = 'pg' + str(count) + '/'
        url = baseUrl + page
        res.append(url)
        count += 1
    return res



# 将 基本信息和交易信息的 键和数据关联起来放到字典中
def convertInfoAndNoValueSetDef(k,v):
    obj = {}
    count = 0
    while count < len(k):
        obj[k[count]] = replaceLine(v[count])
        count+=1
    return obj

# 将关联好的基本数据和交易信息 放到一个字典中
def mergeMap(mapArr):
    res = {}
    # 使用 有序字典 存储房屋信息
    # res = collections.OrderedDict()
    for oMap in mapArr:
        for k in oMap:
            res[k] = oMap[k]
    return res
