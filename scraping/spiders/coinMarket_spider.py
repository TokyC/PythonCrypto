import scrapy
from scraping.items import CoinMarketItem
import numpy as np


class CoinMarketSpider(scrapy.Spider):
    name = 'cryptoMarket'
    start_urls = [
        "https://coinmarketcap.com/"
    ]

    # On récupère les champs
    def parse(self, response):

        crypto = CoinMarketItem()

        all_crypto = response.css('tr')

        for cryptos in all_crypto:
            name = cryptos.xpath('td[3]/div/a/div/div/p/text()').extract()
            symbol = cryptos.xpath('td[3]/div/a/div/div/div/p/text()').extract()
            price = cryptos.xpath('td[4]/div/a/text()').extract()
            percent_change_24h = cryptos.xpath('td[5]/span/text()').extract()
            percent_24 = cryptos.xpath('td[5]/span/span/@class').extract()
            percent_change_7d = cryptos.xpath('td[6]/span/text()').extract()
            percent_7 = cryptos.xpath('td[6]/span/span/@class').extract()
            market_cap = cryptos.xpath('td[7]/p/span[2]/text()').extract()
            volume_24 = cryptos.xpath('td[8]/div/a/p/text()').extract()

            crypto['name'] = name
            crypto['symbol'] = symbol
            crypto['price'] = price

            crypto['percent_change_24h'] = percent_change_24h
            if crypto['percent_change_24h']:
                crypto['percent_change_24h'] = crypto['percent_change_24h'][0]

            crypto['type_24'] = percent_24
            crypto['percent_change_7d'] = percent_change_7d
            if crypto['percent_change_7d']:
                crypto['percent_change_7d'] = crypto['percent_change_7d'][0]

            crypto['type_7'] = percent_7
            crypto['market_cap'] = market_cap
            crypto['volume_24h'] = volume_24

            if crypto['name']:
                yield crypto
