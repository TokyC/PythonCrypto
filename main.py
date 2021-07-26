import os
import pymongo

# Adresse de la base de données (Droits administrateur uniquement pour la base de données 'articles_db')
DATABASE_ADDRESS = "mongodb+srv://Admin:PythonProject@cluster0.squca.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


# Connection à MongoDb
def get_client():
    return pymongo.MongoClient(DATABASE_ADDRESS)

if __name__ == '__main__':

    print('Connexion à MongoDB ...')
    client = get_client()
    print('Succès')

    print('Nettoyage de la base de données (MongoDB) ...')
    client.drop_database('articles')
    print('Succès')

    print('Scraping des articles en cours, patientez ...')
    os.system("scrapy runspider scraping/spiders/articles_spider.py --logfile=scraping.log")
    print('Succès')

    print('Scraping des articles google en cours, patientez ...')
    os.system("scrapy runspider scraping/spiders/coinMarket_spider.py --logfile=scraping.log")
    print('Succès')

    print('Scraping des cryptomonnaies en cours, patientez ...')
    os.system("scrapy runspider scraping/spiders/google_actu_spider.py --logfile=scraping.log")
    print('Succès')

    print('Lancement de streamlit en cours, patientez ...')
    os.system("streamlit run web/streamlit.py")
    print('Succès')