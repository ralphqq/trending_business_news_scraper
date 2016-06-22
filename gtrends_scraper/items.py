# -*- coding: utf-8 -*-

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class GtrendsScraperItem(Item):
    title = Field()
    publisher = Field()
    since_published = Field()
    time_scraped = Field()
    story = Field()
    link = Field()


class GtrendsItemLoader(ItemLoader):
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()
    
    time_scraped_in = MapCompose(
        lambda x: unicode(x).strip()
    )
