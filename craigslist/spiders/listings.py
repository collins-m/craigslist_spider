# -*- coding: utf-8 -*-
import os
import glob
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from craigslist.items import CraigslistItem


class ListingsSpider(Spider):
    name = 'listings'
    allowed_domains = ['dublin.craigslist.org']
    start_urls = ['http://dublin.craigslist.org/search/hhh']

    def parse(self, response):
        listings = response.xpath(
            '//a[@class="result-title hdrlnk"]/@href').extract()
        for listing in listings:
            yield Request(listing, callback=self.parse_listing)

        # process next page
        next_page_url = response.xpath(
            '//a[@class="button next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_listing(self, response):
        # Some listings do not have a location
        try:
            location = response.xpath(
                '//small/text()').extract_first().strip()[1:-1]
        except:
            location = 'n/a'
        page_url = response.xpath(
            '//link[@rel="canonical"]/@href').extract_first()
        price = response.xpath(
            '//*[@class="price"]/text()').extract_first()
        housing = response.xpath(
            '//*[@class="housing"]/text()').extract_first()
        listing_title = response.xpath(
            '//*[@id="titletextonly"]/text()').extract_first()
        description = '\n'.join([t.strip() for t in response.xpath(
            '//section[@id="postingbody"]/text()').extract() if t.strip()])
        image_urls = response.xpath(
            '//img/@src').extract()


        l = ItemLoader(item=CraigslistItem(), response=response)

        l.add_value('page_url', page_url)
        l.add_value('listing_title', listing_title)
        l.add_value('location', location)
        l.add_value('price', price)
        l.add_value('housing', housing)
        l.add_value('description', description)
        l.add_value('image_urls', image_urls)
        return l.load_item()

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, 'house_listings.csv')
