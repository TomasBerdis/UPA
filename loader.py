from numpy import NaN
from pymongo import MongoClient
import pandas
import sys
import re

# connect to MongoDB
print('Connecting to the database...', file=sys.stdout)
client = MongoClient('localhost', 27017)
#client = MongoClient("mongodb+srv://demo:demo@cluster0.qapgw.mongodb.net/upa?retryWrites=true&w=majority")


# create/get database
db = client['upa']

# database schema
collection_names = ['nakazeni_vyleceni_umrti_testy'
                  , 'prehled_hospitalizaci'
                  , 'testy_pcr_antigenni'
                 # , 'osoby_nakaza_kraje'
                  , 'ockovani_kraje'
                  , 'ockovani_zakladni_prehled'
                  , 'vyleceni_kraje'
                  , 'umrti'
                  #, 'obce'
                ]

collection_sources = ["https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/testy-pcr-antigenni.csv"
                   # , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-zakladni-prehled.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/vyleceni.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv"
                    #, "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv"
                    ]

collection_cols = [['datum','prirustkovy_pocet_nakazenych', 'prirustkovy_pocet_vylecenych']
                 , ['datum','pacient_prvni_zaznam']
                 , ['datum','pocet_PCR_testy','pocet_AG_testy']
                 #, ['datum','vek','pohlavi','kraj_nuts_kod','okres_lau_kod','nakaza_v_zahranici','nakaza_zeme_csu_kod']
                 , ['datum','vakcina','kraj_nuts_kod','kraj_nazev','vekova_skupina','prvnich_davek','druhych_davek','celkem_davek']
                 , ['kraj_nazev','kraj_nuts_kod','orp_bydliste','orp_bydliste_kod','vakcina','vakcina_kod','poradi_davky','vekova_skupina','pohlavi','pocet_davek']
                 , ['datum','vek','pohlavi','kraj_nuts_kod','okres_lau_kod']
                 , ['datum','vek','pohlavi','kraj_nuts_kod','okres_lau_kod']
                 #, ['den','datum','kraj_nuts_kod','kraj_nazev','okres_lau_kod','okres_nazev','orp_kod','orp_nazev','obec_kod','obec_nazev','nove_pripady','aktivni_pripady','nove_pripady_65','nove_pripady_7_dni','nove_pripady_14_dni']
                ]

def drop_and_create(id, name):
    
    # drop old collections
    db.drop_collection(name)

    # create collections
    db.create_collection(name)

    # load CSV data from API to MongoDB
    print('Loading data from ', collection_sources[id], '...', file=sys.stdout, sep = '')
    data_from_csv = pandas.read_csv(collection_sources[id], usecols=collection_cols[id])
    data_dict = data_from_csv.to_dict('records')
    db[name].insert_many(data_dict)

    print('Data', name, 'was successfully updated to the database.', file=sys.stdout)

def update_data():
    print('Data update', file=sys.stdout)

    for id,collection_name in enumerate(collection_names):
        col=db[collection_name]
        doc_cnt=col.count_documents({})
        print("\nCollection", col.name)
        data_from_csv = pandas.read_csv(collection_sources[id], usecols=collection_cols[id])
        online_data_amount=len(data_from_csv)
        if online_data_amount == doc_cnt:
            print('is updated  with',doc_cnt, "documents.")
        else:
            number_of_new_docs=online_data_amount-doc_cnt
            print("differs by",number_of_new_docs, "documnets.")
            drop_and_create(id,collection_name)

def update_population():
    kraj_data = pandas.read_csv("https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv", usecols=['vuzemi_cis', 'vuzemi_txt', 'hodnota', 'casref_do', 'pohlavi_kod'])
    kraj_data = kraj_data.loc[kraj_data['casref_do'] == '2020-12-31']
    kraj_data = kraj_data.loc[kraj_data['vuzemi_cis'] == 100]   # kraj
    kraj_data = kraj_data.loc[kraj_data['pohlavi_kod'].isna()]  # NaN values
    kraj_data = kraj_data.groupby(kraj_data['vuzemi_txt']).max().reset_index()    # max NaN value (total for region)
    kraj_data.pop('pohlavi_kod')
    kraj_data.pop('vuzemi_cis')
    kraj_data.pop('casref_do')

    obec_data = pandas.read_csv("https://www.czso.cz/documents/62353418/143520482/130181-21data043021.csv", usecols=['vuzemi_txt', 'vek_txt', 'pohlavi_kod', 'hodnota'])
    obec_data = obec_data.groupby(['vuzemi_txt', 'vek_txt']).sum().reset_index()
    obec_data.pop('pohlavi_kod')
    age = []
    for row in obec_data['vek_txt']:
        row = re.search("^[0-9]+(?=\s)|(?<=^Od\s)[0-9]+", row).group()
        age.append(int(row))
    obec_data['vek'] = age
    obec_data.pop('vek_txt')
    print()


def drop_all():
    for collection_name in collection_names:
         db.drop_collection(collection_name)

#drop_all()
update_population()
update_data()