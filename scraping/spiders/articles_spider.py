import scrapy
from scraping.items import ArticleItem


# Création du spider pour le bitcoin
class ArticlesSpider(scrapy.Spider):
    name = 'cryptoArticles'
    start_urls = [
        'https://cryptonaute.fr/news/bitcoin/',
        'https://cryptonaute.fr/news/ethereum/',
        'https://cryptonaute.fr/news/xrp/',
        'https://cryptonaute.fr/news/blockchain/'
    ]

    # On récupère les champs
    def parse(self, response, **kwargs):

        article = ArticleItem()

        all_div_articles = response.css('div.list-item')

        for articles in all_div_articles:
            title = articles.css('h3.typescale-2 a::text').extract()
            texte = articles.css('div.excerpt::text').extract()
            author = articles.css('a.entry-author__name::text').extract()
            full_article_ref = articles.css('h3.typescale-2 a::attr(href)').extract()

            article['title'] = title
            article['texte'] = texte
            article['author'] = author
            article['full_article_ref'] = full_article_ref

            if article['title']:
                yield article
