from pymongo import MongoClient
import pandas as pd
import sys

# connect to MongoDB
print('Connecting to the database...', file=sys.stdout)
client = MongoClient('localhost', 27017)


# create/get database
db = client['upa']

# database schema
collection_names = [
    'deaths',
    'vaccination_demographic',
    'vaccination_basic_overview'
    ]


collection_sources = ["https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-demografie.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-zakladni-prehled.csv"
                    ]

collection_cols = [['datum','vek','pohlavi','kraj_nuts_kod','okres_lau_kod']
                 , ['datum', 'vakcina', 'vakcina_kod', 'poradi_davky', 'vekova_skupina', 'pohlavi', 'pocet_davek']
                 , ['kraj_nazev','kraj_nuts_kod','orp_bydliste','orp_bydliste_kod','vakcina','vakcina_kod','poradi_davky','vekova_skupina','pohlavi','pocet_davek']
                ]

def drop_and_create(id, name):
    
    # drop old collections
    db.drop_collection(name)

    # create collections
    db.create_collection(name)

    # load CSV data from API to MongoDB
    print(f'Loading data from {collection_sources[id]}...', file=sys.stdout, sep = '')
    data_from_csv = pd.read_csv(collection_sources[id], usecols=collection_cols[id])
    data_dict = data_from_csv.to_dict('records')
    db[name].insert_many(data_dict)
    print(f'Data \'{name}\' was successfully updated to the database.', file=sys.stdout)

def update_data():
    for id,collection_name in enumerate(collection_names):
        drop_and_create(id,collection_name)

def update_villages():
    print('Loading data from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv ...', file=sys.stdout, sep = '')
    collection_cols = ['datum','orp_kod','orp_nazev','nove_pripady']
    villages_df = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv", usecols=collection_cols)
    villages_df = villages_df.groupby(['datum','orp_kod','orp_nazev']).sum().reset_index()
    villages_df_dict = villages_df.to_dict('records')
    db.drop_collection("villages")
    db.create_collection("villages")
    db["villages"].insert_many(villages_df_dict)
    print('Data \'villages\' was successfully updated to the database.', file=sys.stdout)


def update_incremental_stats_and_hospitalized():
    print('Loading data from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv ...', file=sys.stdout, sep = '')
    incremental_stats_cols = [
        'datum','prirustkovy_pocet_nakazenych', 'prirustkovy_pocet_vylecenych','prirustkovy_pocet_umrti',
        'prirustkovy_pocet_provedenych_testu', 'prirustkovy_pocet_provedenych_ag_testu'
    ]
    incremental_stats_df = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv", usecols=incremental_stats_cols).sort_values(by=["datum"])
    
    print('Loading data from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv ...', file=sys.stdout, sep = '')
    hospitalized_df = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv").sort_values(by=["datum"])
    
    incremental_stats_df = incremental_stats_df.merge(hospitalized_df[["datum", "pacient_prvni_zaznam"]], how='left')
    incremental_stats_df.rename(columns={
        'prirustkovy_pocet_nakazenych': 'nakazenych',
        'prirustkovy_pocet_vylecenych': 'vyliecenych',
        'prirustkovy_pocet_umrti': "umrti",
        'prirustkovy_pocet_provedenych_testu': 'pcr_testov',
        'prirustkovy_pocet_provedenych_ag_testu': 'ag_testou',
        'pacient_prvni_zaznam': 'hospitalizovany'
    }, inplace=True)
    
    hospitalized_df = hospitalized_df.drop(["pacient_prvni_zaznam", "kum_pacient_prvni_zaznam", "umrti", "kum_umrti"], axis=1)

    hospitalized_df_dict = hospitalized_df.to_dict('records')
    incremental_stats_df_dict = incremental_stats_df.to_dict('records')

    db.drop_collection("hospitalized_stats")
    db.create_collection("hospitalized_stats")
    db.drop_collection("incremental_stats")
    db.create_collection("incremental_stats")
    db["hospitalized_stats"].insert_many(hospitalized_df_dict)
    print('Data \'hospitalized_stats\' was successfully updated to the database.', file=sys.stdout)
    db["incremental_stats"].insert_many(incremental_stats_df_dict)
    print('Data \'incremental_stats\' was successfully updated to the database.', file=sys.stdout)
    

if __name__ == "__main__":
    update_data()
    update_incremental_stats_and_hospitalized()
    update_villages()