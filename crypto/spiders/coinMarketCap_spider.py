import scrapy
from ..items import CryptoMarketItem
import numpy as np


class CoinMarketCapSpider(scrapy.Spider) :
    name = 'cryptoMarket'
    start_urls = [
        "https://coinmarketcap.com/"
    ]

    def parse(self, response) :
        crypto = CryptoMarketItem()

        all_crypto = response.css('tr')

        for cryptos in all_crypto :
            name = cryptos.css('.iJjGCS::text').extract()
            symbol = cryptos.css('.coin-item-symbol::text').extract()
            price = cryptos.css('.cLgOOr .cmc-link::text').extract()
            percent_change_24h = cryptos.css('td:nth-child(5) .sc-1v2ivon-0::text').extract()
            percent_24 = cryptos.css('td:nth-child(5) .sc-1v2ivon-0 span::attr(class)').extract()
            percent_change_7d = cryptos.css('td:nth-child(6) .sc-1v2ivon-0::text').extract()
            percent_7 = cryptos.css('td:nth-child(6) .sc-1v2ivon-0 span::attr(class)').extract()
            market_cap = cryptos.css('.ieFnWP::text').extract()
            volume_24 = cryptos.css('.font_weight_500___2Lmmi::text').extract()

            crypto['name'] = name
            crypto['symbol'] = symbol
            crypto['price'] = price
            crypto['percent_change_24h'] = percent_change_24h
            crypto['type_24'] = percent_24
            crypto['percent_change_7d'] = percent_change_7d
            crypto['type_7'] = percent_7
            crypto['market_cap'] = market_cap
            crypto['volume_24h'] = volume_24

            if crypto['name'] :
                yield crypto
