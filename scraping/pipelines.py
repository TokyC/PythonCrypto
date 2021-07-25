import pymongo

# Adresse de la base de données
DATABASE_ADDRESS = "mongodb+srv://Hakim:PythonProject2021@cluster0.hdu6d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


class ScrapingPipeline:

    def __init__(self):

        # Connection à la DB
        self.conn = pymongo.MongoClient(
            DATABASE_ADDRESS
        )

    def process_item(self, article, spider):

        if spider.name == 'cryptoArticles':
            db = self.conn["articles_db"]
            self.collection = db['articles']
            self.collection.insert(dict(article))
            return article

        elif spider.name == 'cryptoMarket':
            db = self.conn["articles_db"]
            self.collection = db["coinMarket"]
            self.collection.insert(dict(article))
            return article
