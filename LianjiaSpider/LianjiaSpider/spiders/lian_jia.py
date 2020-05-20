# -*- coding: utf-8 -*-
import json
import copy
import logging
import scrapy
# 导入 定义的 处理数据相关的 方法
from LianjiaSpider.spiders.utils import reduplication_street_url,convertUrlList,convertInfoAndNoValueSetDef,mergeMap
# 导入 管道
from LianjiaSpider.items import LianjiaspiderItem

# 爬虫 模块
class LianJiaSpider(scrapy.Spider):
    name = 'lian_jia'
    allowed_domains = ['lianjia.com']
    # 修改起始的url地址
    start_urls = ['https://zz.lianjia.com/ershoufang/']

    base_url = 'https://zz.lianjia.com'
    # 设置一个列表用于去除重复的 街道
    street_list = []

    # 使用 起始url 发送请求后 的回调函数(解析方法)     获取 区的url
    def parse(self, response):

        # 使用 xpath 语法 获取 城市下面的 区的url
        area_urls = response.xpath('//div[@data-role="ershoufang"]/div/a/@href')

        for area_url in area_urls:
        # for area_url in area_urls[:2]:
            # 把 获得的区地址的 selector对象列表 使用for循环 通过 extract() 方法 转成字符串
            area = area_url.extract()
            area_url = self.base_url + area
            # 把 获得 url 构造成 请求对象 返回给 引擎 然后 让框架通过引擎再次发送请求
            item = {'city':'郑州','area_url':area_url}
            yield scrapy.Request(area_url,callback=self.street_parser,meta={'items':copy.deepcopy(item)})

    # 解析 下载器 返回的响应 获取 街道的url
    def street_parser(self,response):
        # 获取 区 对应 url 请求后的响应的 meta参数中的 items 是一个字典
        items = response.meta['items']

        # print('区的url: ', items['are
        # a_url'])
        # 获取 这个区 页面下的 街道的 url
        streets  =  response.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href')
        # 获取 这个区 页面下的 街道的 名字
        street_names = response.xpath('//div[@data-role="ershoufang"]/div[2]/a/text()')

        for street,street_name in zip(streets,street_names):
        # for street,street_name in zip(streets[:2],street_names[:2]):
            street = reduplication_street_url(self.street_list,street.extract())
            if street is not None:
                street_name = street_name.extract()
                street_url = self.base_url +street
                print('==>街道的url: ' + street_url)
                # 向 items 的 添加街道名字和街道的url
                items['street'] = street_name
                items['street_url'] = street_url
                # print('street_parser的items====',items)
                # 向引擎返回 街道的 url
                yield scrapy.Request(street_url,callback=self.total_page_parse,meta={'items':copy.deepcopy(items)})

    #  解析街道的url 对应的totalPage 即 总页数
    def total_page_parse(self,response):
        # 获得 meta 中的 items 参数
        items = response.meta['items']

        street_url = items['street_url']
        # print('==>街道的url: ' + street_url)

        # 使用 xpath 语法 解析 获得总的页数 使用 extract_first() 返回列表(选择器转成的字符串)中第一个字符串,若是为空列表则返回为None
        total_pages = response.xpath('//*[@id="content"]/div[1]/div[8]/div[2]/div/@page-data').extract_first()
       # 若是 获得的 total_pages 若是不为空 则获得总页数
        if total_pages is not None:
            # 因为总页数 是一个 json 字符串 将json字符串转成Python字典
            total_pages = json.loads(total_pages)
            # 获取总页数
            total_page = total_pages.get('totalPage')
            # 构造 这个街道 对应页数的所有的url
            street_url_list = convertUrlList(street_url,total_page)
            # 使用 for 循环 发送给引擎 报好页数的url 调用 解析函数 解析出 每个页面对应的 每个房屋的url
            for url in street_url_list:
            # for url in street_url_list[:2]:
                # 将包含详细页码的街道的url放到 items 中
                items['street_page_url'] = url
                # print('total_page的items====',items)
                # print(url)
                # 因为 每个 街道 第一页的url 和 street_parser解析方法返回的请求对象是同一个 所以
                # 在构造包含 页码的请求对象的时候, 第一页的请求对象 会被重复检查的filter个屏蔽了 若是不想被屏蔽设为true
                # yield scrapy.Request(url=url,callback=self.detail_url,meta={'items':copy.deepcopy(items)},dont_filter=True)
                yield scrapy.Request(url=url,callback=self.detail_url,meta={'items':copy.deepcopy(items)})

    # 解析包含页码的url 获取 每个 页面的 详情房屋的url
    def detail_url(self,response):
        items = response.meta.get('items')
        print('detail中的url: ',items['street_page_url'])
        # print('detail_url的items',items)
        # 使用xpath语法 解析 每个页面详情房屋的 url
        detail_urls = response.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[1]/a/@href')
        print(len(detail_urls))
        for detail in detail_urls:
            detail_url = detail.extract()
            # 把 房屋的url放到 items 中
            items['detail_url'] = detail_url
            print('每页房屋的url===》 ' + detail_url)
            # 返回请求对象 给 引擎 解析 房屋信息
            yield scrapy.Request(url=detail_url,callback=self.house_parse,meta={'items':copy.deepcopy(items)})

    # 解析 房屋 获取房屋中的信息
    def house_parse(self,response):
        items = response.meta.get('items')
        data = [
            "id", "小区名称", "所在区域", "总价", "单价",
            "房屋户型", "所在楼层", "建筑面积", "户型结构",
            "套内面积", "建筑类型", "房屋朝向", "建筑结构",
            "装修情况", "梯户比例", "配备电梯", "产权年限",
            "挂牌时间", "交易权属", "上次交易", "房屋用途",
            "房屋年限", "产权所属", "抵押信息", "房本备件",
        ]

        # 获取 小区名称
        plot_name = response.xpath('//div[@class="communityName"]/a[1]/text()').extract_first()

        # 获取 小区的所在区域
        plot_area = response.xpath('//span[@class="info"]/a[1]/text()').extract_first()
        try:
            # 获取 总价这 和总结个的单位这两个字符串 然后拼接长总价格
            total_price_data = response.xpath('//span[@class="total"]/text()').extract_first()
            if not total_price_data:
                total_price_data = response.xpath('/html/body/div[5]/div[2]/div[3]/span[1]/text()').extract_first()
            if not total_price_data:
                total_price_data = response.xpath('//div[@class="price "]/span[@class="total"]/text()').extract_first()
            total_price_unit = response.xpath('//span[@class="unit"]/span/text()').extract_first()
            if not total_price_unit:
                total_price_unit = response.xpath('/html/body/div[5]/div[2]/div[3]/span[2]/span/text()').extract_first()
            if not total_price_unit:
                total_price_unit = response.xpath('//div[@class="price "]/span[@class="unit"]/span/text()').extract_first()
            total_price = total_price_data + total_price_unit
        except Exception as e:
            total_price = ''
            logging.error('{} total_price error'.format(items['detail_url']))

        try:
            # 获取 单价数 和 单位这两个字符串 合并成 单价
            unit_price_data = response.xpath('//span[@class="unitPriceValue"]/text()').extract_first()
            unit_price_unit = response.xpath('//span[@class="unitPriceValue"]/i/text()').extract_first()
            unit_price = unit_price_data + unit_price_unit
        except:
            unit_price = ''
            logging.error('{} unit_price error'.format(items['detail_url']))

        # 获取 关注人数
        attention_nums = response.xpath('//span[@id="favCount"]/text()').extract_first()

        # 把 单价 总价 小区名称 所在区域 构造成字典
        plot_info = convertInfoAndNoValueSetDef(["小区名称", "所在区域", "总价", "单价",'关注人数'],
                                                [plot_name,plot_area,total_price,unit_price,attention_nums])

        # 获取 页面基本属性中的内容
        base_info_key = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span/text()').extract()
        base_info_data = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/text()').extract()

        # 把 页面基本属性的 键 和 数据 放到字典中
        base_info = convertInfoAndNoValueSetDef(base_info_key,base_info_data)

        # 获取 交易属性
        deal_info_key = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[1]/text()').extract()
        deal_info_data = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[2]/text()').extract()
        # 把 交易属性的 键 和 数据 放到字典中
        deal_info = convertInfoAndNoValueSetDef(deal_info_key,deal_info_data)

        # 把小区名字,价格等 和 基本属性 以及 交易属性 放到一起
        house_info_dict = mergeMap([plot_info,base_info,deal_info])
        # print('小区的信息:',house_info_dict)

        # 向 数据队列 item 中写入数据
        lijian_item = LianjiaspiderItem()
        lijian_item['city'] = items['city']
        lijian_item['street'] = items['street']
        lijian_item['street_page_url'] = items['street_page_url']
        lijian_item['detail_url'] = items['detail_url']
        lijian_item['house_info_dict'] = house_info_dict
        # print(lijian_item)
        yield lijian_item








