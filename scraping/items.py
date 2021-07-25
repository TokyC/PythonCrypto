import scrapy


# Articles
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    texte = scrapy.Field()
    author = scrapy.Field()
    full_article_ref = scrapy.Field()
    img_src = scrapy.Field()


# Coin market
class CoinMarketItem(scrapy.Item):
    name = scrapy.Field()
    symbol = scrapy.Field()
    price = scrapy.Field()
    percent_change_24h = scrapy.Field()
    type_24 = scrapy.Field()
    percent_change_7d = scrapy.Field()
    type_7 = scrapy.Field()
    market_cap = scrapy.Field()
    volume_24h = scrapy.Field()
