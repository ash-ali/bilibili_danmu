# -*- coding: utf-8 -*-
import scrapy
import json
from bilibili_danmu.items import BilibiliDanmuItem
import re
class DanmuSpider(scrapy.Spider):
    name = 'danmu'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://api.bilibili.com/x/player/pagelist?bvid=BV1Q7411Y7YM&jsonp=jsonp/']

    '''获取cid'''
    def parse(self, response):
        cid = json.loads(response.text)['data'][0]['cid']
        url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+str(cid)
        yield scrapy.Request(url,callback=self.parse_danmu)
        #pass

    '''获取弹幕'''
    def parse_danmu(self,response):
        #存储弹幕的item对象
        item = BilibiliDanmuItem()

        data = response.text
        print(data)
        data_compile = re.compile('<d.*?>(.*?)</d>')
        #弹幕列表
        info_list = data_compile.findall(data)
        for info in info_list:
            item['info'] = info
            yield item
        #pass
if __name__ == '__main__':
    from scrapy import cmdline
    args = "scrapy crawl danmu".split()
    cmdline.execute(args)