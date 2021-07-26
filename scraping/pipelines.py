import pymongo

# Adresse de la base de données
DATABASE_ADDRESS = "mongodb+srv://Toky:PythonProject@cluster0.squca.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

class ScrapingPipeline :

    def __init__(self) :

        # Connection à la DB
        self.conn = pymongo.MongoClient(
            DATABASE_ADDRESS
        )

    def process_item(self, article, spider) :
        if spider.name == 'cryptoArticles' :
            db = self.conn["articles"]
            self.collection = db['Cryptonaute']
            self.collection.insert(dict(article))
            return article

        elif spider.name == 'cryptoMarket':
            db = self.conn["articles"]
            self.collection = db["coinMarket"]
            self.collection.insert(dict(article))
            return article

        elif spider.name == 'GoogleArticles':
            db = self.conn["articles"]
            self.collection = db["GoogleNews"]
            self.collection.insert(dict(article))
            return article
