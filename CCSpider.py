import scrapy
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess


class CCSpider(scrapy.Spider):
    start_urls = []
    # Find what the user wants to input
    query = input("Wha' you searching for buddy?")
    query.replace(" ","+")

    # We always start on page1, for a nice scrape process.
    url = "https://www.cashconverters.co.uk/search?type=product&phrase=" + query + "&page=1"
    start_urls.append(url)
    name = 'ccspider'
    def parse(self, response):
        for title in response.css('.col-sm-4'):
            image = title.css('.panel a ::attr(style)').get()
            fixed = self.fixImage(image)
            price = self.fixPrice(title.css('.panel>.price-tag ::text').get())

            yield {'ref': title.css('.panel ::attr("data-barcode")').get(),'title': title.css('.panel-body>h5 a ::text').get(), 'price' : price,'image' : fixed, 'href': title.css('.panel a ::attr(href)').get()}

        next_pages = response.css('.pagination>.page a ::attr(href)').getall()
        for next_page in next_pages:
                yield response.follow(next_page, self.parse)

    def fixImage(self, image):
        if image is not None:
         image = image.split("url(")[1].strip(")")
         return image

    def fixPrice(self,price):
        if price is not None:
            return price.strip("\n").strip()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
})

process.crawl(CCSpider)
process.start()