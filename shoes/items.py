import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    color = scrapy.Field()
    available_colors = scrapy.Field()
    review_count = scrapy.Field()
    reviews_score = scrapy.Field()
