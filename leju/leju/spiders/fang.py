# -*- coding: utf-8 -*-
import re

import scrapy
from leju.settings import *
from leju.items import AgentItem

class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['esf.leju.com']
    # start_urls = ['http://esf.leju.com/']

    def start_requests(self):
        """
        从每个城市的第一页开始
        :return:
        """

        city_names = ["baoding"]
        base_url = "https://{}.esf.leju.com/house/"
        for city in city_names:
            url = base_url.format(city)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_link, meta={"city": city})

    def parse_link(self, response):
        """
        解析当前页的detail链接， yield
        获取下一页链接 yield
        :param response:
        :return:
        """

        scheme = "https:"

        detail_links = response.xpath("//h3[@class='house-title']/a/@href").extract()
        for detail_link in detail_links:
            url = scheme + detail_link
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_detail, meta={"city": response.meta["city"]})

        next_url = response.xpath("//div[@class='page']/a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=scheme+next_url, dont_filter=True, callback=self.parse_link, meta={"city": response.meta["city"]})

    def parse_detail(self, response):
        """
        解析详情页 获取姓名和电话
        yield item
        :param response:
        :return:
        """

        ori = response.request.url
        pattern = re.compile(r"^https://(.+?)\.")
        res = re.match(pattern, ori).group(1)
        if res != "m":

            name = response.xpath("//dd[@class='pr']/a/text()").get()
            res = response.xpath("//div[@class='h-tel']//text()").extract()
            tel = res[1]

            item = AgentItem()
            item["name"] = name
            item["tel"] = tel
            item["source"] = "leju"
            item["area"] = response.meta["city"]
            yield item
