import scrapy
from demo.items import QsbkItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList


class Meiwen(scrapy.Spider):
    name = "qsbk_spider"
    allowed_domains = ['qiushibaike.com']  #允许爬虫的范围
    start_urls = ['https://www.qiushibaike.com/text/page/1/']  #最开始的请求的url地址
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        resp = response.xpath("//div[@id='content-left']/div")
        for resp in resp:
            auto = resp.xpath(".//h2/text()").get().strip()
            wen = resp.xpath(".//div[@class='content']//text()").getall()
            wen = " ".join(wen).strip()
            # print(auto)
            item = QsbkItem(auto=auto,wen=wen)
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li/[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url,callback=self.parse)





