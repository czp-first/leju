# -*- coding: utf-8 -*-
import re

import scrapy
from leju_agent.items import Agent


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['leju.com']

    def start_requests(self):
        city_names = ["byne"]
        base_url = "https://{}.esf.leju.com/agent/"
        for city in city_names:
            url = base_url.format(city)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_agent, meta={"city": city})

    def parse_agent(self, response):

        ori = response.request.url
        pattern = re.compile(r"^https://(.+?)\.")
        res = re.match(pattern, ori).group(1)
        if res != "m":

            next_url = response.xpath("//a[@class='next']/@href").get()
            if next_url:
                url = "https:"+next_url
                yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_agent, meta={"city": response.meta["city"]})

            divs = response.xpath("//div[contains(@class, 'agent-mod clearfix')]")
            if divs:
                for div in divs:
                    item = Agent()
                    item["area"] = response.meta["city"]
                    item["source"] = "leju"
                    item["name"] = div.xpath(".//a[@class='fs18 name']/text()").get()
                    item["tel"] = div.xpath(".//div[@class='fl']/span/text()").get()
                    yield item
            else:
                divs = response.xpath("//div[@class='tit clearfix']")
                for div in divs:
                    item = Agent()
                    item["area"] = response.meta["city"]
                    item["source"] = "leju"
                    item["name"] = div.xpath(".//h4[@class='fs18 fl']/a/@title").get()
                    item["tel"] = div.xpath(".//h4[@class='fs18 fl']/a/span/text()").get()
                    yield item
