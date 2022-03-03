import scrapy

class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"

    def start_requests(self):
        url= 'http://quotes.toscrape.com/'

        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('span[@class="text"]/text()').get(),
                'author': quote.xpath('span/small/text()').get(),
                'tags': quote.xpath('div[@class="tags"]/a/text()').getall()
            }

        yield from response.follow_all(xpath='//ul[@class="pager"]/li[@class="next"]/a', callback=self.parse)
