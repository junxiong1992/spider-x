from scrapy import Spider, Request

from xiuren.items import XiurenItem


class XiurenspiderSpider(Spider):
    name = 'xiurenspider'
    allowed_domains = ['xiurenb.com','xiurenb.net']
    start_url = 'http://www.xiurenb.com/XiuRen/'

    def start_requests(self):
        for index in range(3):
            if index == 0:
                index_url = self.start_url + 'index'+ '.html'
            else:
                index_url = self.start_url + 'index' + str(index) + '.html'
            # print(f'正在访问第{index}页')
            yield Request(index_url, callback=self.parse_index)

    def parse_index(self, response):
        for item in response.css('div.home-filter > div > div > ul > li'):
            detail_href = item.css('a::attr(href)').extract_first()
            title = item.css('a::attr(title)').extract_first()
            detail_url = response.urljoin(detail_href)

            # print('获取作者页:', title, detail_url)

            yield Request(detail_url, callback=self.parse_detail_author, meta={
                'title': title, 'to_url': detail_url
            })

    def parse_detail_author(self, response):
        title = response.meta.get('title')
        to_url = response.meta.get('to_url')

        to_url_0 = to_url.rsplit(".", 1)[0]

        pages = response.css('body > div.main > div > div > div:nth-child(5) > div > div > a').extract()
        pages = len(pages) - 2
        # print('该作者图片页共有', pages, '页')

        for index in range(0, pages):

            if index == 0:
                detail_url = to_url
                # print('访问作者图片第有', '0 页:', detail_url)
            else:
                detail_url = to_url_0 + '_' + str(index) + '.html'
                # print('访问作者图片第', index, '页:', detail_url)
            yield Request(detail_url, callback=self.parse_detail, meta={
                'title': title, 'to_url': detail_url
            })

    # def parse_detail_author_page(self, response):
    #     title = response.meta.get('title')
    #     to_url = response.meta.get('to_url')
    #
    #     for item in response.css('div.gtps.fl > ul > li'):
    #         detail_href = item.css('a::attr(href)').extract_first()
    #         detail_url = response.urljoin(detail_href)
    #
    #         print('获取高清图片页:', title, detail_url)
    #
    #         yield Request(detail_url, callback=self.parse_detail, meta={
    #             'title': title, 'to_url': detail_url
    #         })

    def parse_detail(self, response):
        title = response.meta.get('title')
        to_url = response.meta.get('to_url')

        base_name = to_url.rsplit("/", 1)[1].split(".", 1)[0]
        tag = 0

        for item in response.css('p[align="center"] > img'):
            tag = tag + 1
            group = item.css('::attr(title)').extract_first()
            url = item.css('::attr(src)').extract_first()
            url = response.urljoin(url)
            name = f'{base_name}_{tag}.jpg'
            print(url)
            # print('获取高清图地址:', url)

            item = XiurenItem({
                'group': group,
                'url': url,
                'name': name
            })
            yield item
