import scrapy
from ..items import ScrapBricolageItem


class VeloSpider(scrapy.Spider):
    name = 'Velo'
    start_urls = [
        'https://mr-bricolage.bg/bg/Instrumenti/Avto-i-veloaksesoari/Veloaksesoari/c/006008012'
    ]

    def parse(self, response):

        item_url = response.css('div.title a::attr(href)')
        for href in item_url:
            yield response.follow(href, self.product_parse)

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def product_parse(self, response):
        items = ScrapBricolageItem()

        name = response.css('li.active::text').extract()[0]
        price = response.css('p.price::text').extract()[0]
        img_xpath = f'//img[@alt="{name}"]/@src'
        img = response.xpath(img_xpath).extract_first()

        price = price.split()[0]
        price = price.replace(",", ".")

        char_dict = {}
        char_table = response.css('table.table')
        if char_table:
            rows = response.xpath("//table[@class='table']/tbody/tr")
            for row in rows:
                data = row.css('td::text').extract()
                data[1] = ''.join(data[1].split())
                char_dict[data[0]] = data[1]

        items['name'] = name
        items['price'] = price
        items['img'] = img
        items['characteristics'] = char_dict if char_dict else "None"

        yield items
