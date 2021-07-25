import pymongo
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Adresse de la base de données
DATABASE_ADDRESS = "mongodb+srv://Hakim:PythonProject2021@cluster0.hdu6d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


# Connection à MongoDb
@st.cache(hash_funcs={pymongo.MongoClient: id})
def get_client():
    return pymongo.MongoClient(DATABASE_ADDRESS)


# Chargement des données de coinmarket cap avec reformatage des données
def load_market_data():
    df_markets = pd.DataFrame(list(db['coinMarket'].find()))
    df_markets.pop("_id")
    df_markets.pop("type_7")
    df_markets.pop("type_24")
    df_markets.columns = ['Nom', 'Symbole', 'Prix ($)', 'Variation en 24h', 'Variation en 7j', 'Market Cap ($)',
                          'Volume en 24h ($)']
    df_markets['Nom'] = df_markets['Nom'].astype(str)
    df_markets['Symbole'] = df_markets['Symbole'].astype(str)

    for i in range(len(df_markets['Nom'])):
        df_markets['Nom'][i] = df_markets['Nom'][i][2:len(df_markets['Nom'][i]) - 2]

    for i in range(len(df_markets['Symbole'])):
        df_markets['Symbole'][i] = df_markets['Symbole'][i][2:len(df_markets['Symbole'][i]) - 2]

    for i in range(len(df_markets['Prix ($)'])):
        df_markets['Prix ($)'][i] = df_markets['Prix ($)'][i][0][1::].replace(',', '')

    for i in range(len(df_markets['Market Cap ($)'])):
        df_markets['Market Cap ($)'][i] = df_markets['Market Cap ($)'][i][0][1::].replace(",", "")

    for i in range(len(df_markets['Volume en 24h ($)'])):
        df_markets['Volume en 24h ($)'][i] = df_markets['Volume en 24h ($)'][i][0][1::].replace(",", "")

    df_markets['Prix ($)'] = df_markets['Prix ($)'].astype(float)
    df_markets['Variation en 24h'] = df_markets['Variation en 24h'].astype(float)
    df_markets['Variation en 7j'] = df_markets['Variation en 7j'].astype(float)
    df_markets['Market Cap ($)'] = df_markets['Market Cap ($)'].astype(float)
    df_markets['Volume en 24h ($)'] = df_markets['Volume en 24h ($)'].astype(float)
    return df_markets


# On load les datas
def load_mongo_data():
    df = pd.DataFrame(list(db["coinMarket"].find()))
    df.pop("_id")
    return df


# Récupèrer les prix
def getPrix(symbole):
    for i in range(len(df_market['Prix ($)'])):
        if df_market['Symbole'][i] == symbole:
            return df_market['Prix ($)'][i]


def load_google_article():
    df_gArticles = pd.DataFrame(list(db['articles'].find()))
    df_gArticles.pop('_id')
    return df_gArticles


def afficherArticle(title, texte, media, full_articles):
    middle_page.markdown(f"""
        ### [{title}]({''.join(full_articles)})
    """)
    middle_page.markdown(f"""       
         >-{texte} ***{media}***
    """)



# Setup de la page
st.set_page_config(layout="wide")
st.title("Agrégateur d'informations sur la Cryptommonaie")
st.markdown("""## Application""")

# La bare d'information
extend_bar = st.beta_expander("Information")
extend_bar.markdown("""
- **Description du projet** : Dans le cadre du cours de Scrpting Python, nous devons développer un projet portant un sujet au choix en python. Nous avons choisi de scrapper des données sur internet et les valoriser.Nous avons opté pour la récupération des données en rapport avec la cryptomonnaie pour permettre une accessibilité et une facilité d'accès à la connaissance de la cryptomonnaie et au suivi des tendances du marché.
- **Développeurs** : Toky Cedric Andriamahefa, Hakim Saghir et Thomas Rémy
- **Langage** : Python
- **Frameworks** : Streamlit, Scrapy 
- **Base de données** : MongoDB
- **Sources** : Cryptonaute, CoinMarketCap
""")



# Connexion à la base de données
client = get_client()
db = client["articles_db"]

# Crétation des trois colonnes
side_part = st.sidebar

# Creation des colonnes 2 et 3 tels que la colone 2 est 2 fois plus grande que la colonne 3
middle_page, right_side = st.beta_columns((2, 1))

# Partie coinMarket
df_market = load_market_data()
crypto_ordre = sorted(df_market['Symbole'])



# ** Partie de droite **

# partie 1 du side_part
side_part.header('Paramètres : ')
type_of_cryptocurrency = side_part.selectbox('Choisissez une cryptommonaie de réference : ', crypto_ordre)
side_part.write("Vous avez choisis : " + type_of_cryptocurrency)

# partie 2 du side_part
article = load_mongo_data()

# Partie 3
crypto_selected = side_part.multiselect('Choisissez des cryptomonnaies pour comparer : ', crypto_ordre, )
c_selected = crypto_selected
if not crypto_selected:
    c_selected = ['BTC']
df_crypto_selected = df_market[(df_market['Symbole'].isin(c_selected))]
interval_pourcentage = side_part.selectbox('La période de la variation', ['7j', '24h'])
type_variation = {"7j": 'Variation en 7j', "24h": 'Variation en 24h'}
choix_variation = type_variation[interval_pourcentage]

# Partie 4
res_slider = side_part.slider("Choisissez le nombre d'articles à afficher", 1, 50, 1)



# ** Partie de droite **

# Partie 1
middle_page.markdown(f"""
# Prix du {type_of_cryptocurrency}
""")
middle_page.markdown(f"""
# {getPrix(type_of_cryptocurrency)} $
""")

# Partie 2
middle_page.markdown("""
### Le prix des Cryptos séléctionnées
""")
middle_page.write('Dimension : ' + str(df_crypto_selected.shape[0]) + 'ligne(s) et ' + str(
    df_crypto_selected.shape[1]) + 'colonne(s)')
middle_page.write(df_crypto_selected)

# Partie 3
middle_page.markdown("""
### Tableau de la variation du prix
""")
df_variation = pd.concat(
    [df_crypto_selected.Symbole, df_crypto_selected['Variation en 24h'], df_crypto_selected['Variation en 7j']], axis=1)
df_variation = df_variation.set_index('Symbole')
middle_page.dataframe(df_variation)
df_variation['positif_variation_24'] = df_variation['Variation en 24h'] > 0
df_variation['positif_variation_7'] = df_variation['Variation en 7j'] > 0

# Partie 4
middle_page.markdown("""
### Graph des prix
""")
df_price = pd.concat([df_crypto_selected.Symbole, df_crypto_selected['Prix ($)']], axis=1)

df_price = df_price.set_index('Symbole')

plt.figure(figsize=(15, 5))
plt.subplots_adjust(top=1, bottom=0)

df_price['Prix ($)'].plot(kind='bar', color='b')
middle_page.pyplot(plt)



# *** Affichage des articles ***

middle_page.title('Articles du jour')
titleCollection = {
    "collectionReddit": "Reddit",
    "collectionTwitter": "Twitter"
}

df_Garticles = load_google_article()

for i in range(0, res_slider):
    titre = df_Garticles['title'][i]
    text = df_Garticles['texte'][i]
    full_ref = df_Garticles['full_article_ref'][i]
    afficherArticle(titre[0], text[0], "Cryptonaute", full_ref)



# *** Rightside ***

right_side.markdown("""### Bar plot du % de variation du Prix""")

if interval_pourcentage == '7j':
    right_side.markdown("""*7 derniers jours*""")
    plt.figure(figsize=(6, 6))
    plt.subplots_adjust(top=1, bottom=0)
    df_variation['Variation en 7j'].plot(kind='bar', color=df_variation.positif_variation_7.map({True: 'g', False: 'r'}))
    right_side.pyplot(plt)
else:
    right_side.markdown("""*dernière 24h*""")
    plt.figure(figsize=(6, 6))
    plt.subplots_adjust(top=1, bottom=0)
    df_variation['Variation en 24h'].plot(kind='bar', color=df_variation.positif_variation_24.map({True: 'g', False: 'r'}))
    right_side.pyplot(plt)
