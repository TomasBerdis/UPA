from pymongo import MongoClient
import pandas
import sys

# connect to MongoDB
print('Connecting to the database...', file=sys.stdout)
#client = MongoClient('localhost', 27017)
client = MongoClient("mongodb+srv://demo:demo@cluster0.qapgw.mongodb.net/upa?retryWrites=true&w=majority")


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

def drop_all():
    for collection_name in collection_names:
         db.drop_collection(collection_name)

#drop_all()
update_data()