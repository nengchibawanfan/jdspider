import scrapy
from jd.items import JdItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    def start_requests(self):
        # https://list.jd.com/list.html?cat=9987,653,655 &page=2&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=6#J_main
        urls = [
            "https://list.jd.com/list.jd.com/list.html?cat=9987,653,655",  # 手机，共152页
            "https://list.jd.com/list.jd.com/list.html?cat=652,828,842",  # 耳机，共214页
            "https://list.jd.com/list.jd.com/list.html?cat=652,828,841",  # 音箱，共234页
            "https://list.jd.com/list.jd.com/list.html?cat=652,12345,12347",  # 手环，共228页
            "https://list.jd.com/list.jd.com/list.html?cat=670,671,672"  # 笔记本，共1021页
        ]

        # yield self.make_requests_from_url("https://list.jd.com/list.html?cat=9987,653,655&page=2&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=6#J_main")
        for url in urls:
            for i in range(1, 2):
                full_url = url + "&page=%d&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=6#J_main" % i
                yield self.make_requests_from_url(full_url)

    def parse(self, response):
        category = {
            "9987,653,655": "手机",
            "652,828,842": "耳机",
            "652,828,841": "音箱",
            "652,12345,12347": "手环",
            "670,671,672": "笔记本",
        }

        for each in response.xpath('//ul[@class="gl-warp clearfix"]/li'):
            item = JdItem()
            cate = response.url[response.url.find('=') + 1: response.url.find('&')].strip(' ')
            item['category'] = category[cate]
            # try:
            # item['name'] = each.xpath('./div/div[@class="p-name p-name-type-2"]/a/@title').extract()[0]
            # 商品名解析
            # scrapy 自带的Xpath解析进行匹配
            # <div class="p-name">，其它商品和部分手机商品
            item['name'] = ' '
            # type 为列表
            tmp = each.xpath('./div/div[@class="p-name"]/a/em/text()')
            if tmp:
                item['name'] = tmp.extract()[0].strip('\n').strip(' ')
            else:
                # <div class="p-name p-name-type3">， 大部分手机商品
                item['name'] = each.xpath('./div/div[@class="p-name p-name-type3"]/a/em/text()').extract()[0].strip(
                    '\n').strip(' ')
            item['price'] = each.xpath('./div/div[@class="p-price"]/strong/i/text()').extract()[0]

            tmp = each.xpath('./div/div[@class="p-commit"]/strong/a/text()')
            if tmp:
                item['remark_count'] = tmp.extract()[0]
            else:
                # 手环、笔记本
                item['remark_count'] = each.xpath('./div/div[@class="p-commit p-commit-n"]/strong/a/text()').extract()[
                    0]

            # 判断是否有其它参数
            tmp = each.xpath('./div/div[@class="p-name p-name-type3"]/span//a')
            if tmp:
                des = []
                for a in tmp:
                    des.append(a.xpath('./b/text()').extract()[0])
                item['descript'] = ';'.join(des)
            else:
                item['descript'] = ' '
            # item['second_hand_url'] = each.xpath('./div/div[@class="p-commit"]/a[@class="spu-link"]/@href').extract()[0]

            # 判断是否是店家
            tmp = each.xpath('./div/div[@class="p-shop"]/span/a/@title')
            item['merchant'] = tmp.extract()[0] if tmp else ' '

            # 判断是否有二手
            tmp = each.xpath('./div/div[@class="p-commit"]/a[@class="spu-link"]/text()')
            item['second_hand'] = '1' if tmp else '0'
            yield item
#             一定要用yield  交给管道处理
