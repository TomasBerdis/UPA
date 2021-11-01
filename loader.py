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
collection_names = ['nakazeni_vyleceni'
                  , 'hospitalizace'
                  , 'testy']
collection_sources = ["https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/testy-pcr-antigenni.csv"]
collection_cols = [['datum','prirustkovy_pocet_nakazenych', 'prirustkovy_pocet_vylecenych']
                 , ['datum','pacient_prvni_zaznam']
                 , ['datum','pocet_PCR_testy','pocet_AG_testy']]

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
        data_from_csv = pandas.read_csv(collection_sources[id], usecols=collection_cols[id])
        online_data_amount=len(data_from_csv)
        if online_data_amount == doc_cnt:
            print("Collection", col.name, 'is updated  with',doc_cnt, "documents.")
        else:
            number_of_new_docs=online_data_amount-doc_cnt
            print("Collection", col.name, "differs by",number_of_new_docs, "documnets.")
            drop_and_create(id,collection_name)
            
update_data()