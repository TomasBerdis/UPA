from numpy import NaN
from pymongo import MongoClient
import pandas as pd
import sys
import re


# connect to MongoDB
print('Connecting to the database...', file=sys.stdout)
client = MongoClient('localhost', 27017)


# create/get database
db = client['upa']

# database schema
collection_names = [
    'vaccination_demographic',
    'vaccination_geographic',
    'vaccination_basic_overview'
    ]


collection_sources = ["https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-demografie.csv",
                      "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-geografie.csv"
                    , "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-zakladni-prehled.csv"
                    ]

collection_cols = [['datum', 'vakcina', 'vakcina_kod', 'poradi_davky', 'vekova_skupina', 'pohlavi', 'pocet_davek']
                 , ['datum', 'vakcina', 'vakcina_kod', 'poradi_davky', 'kraj_nazev', 'kraj_nuts_kod', 'orp_bydliste', 'orp_bydliste_kod', 'pocet_davek']
                 , ['kraj_nazev','kraj_nuts_kod','orp_bydliste','orp_bydliste_kod','vakcina','vakcina_kod','poradi_davky','vekova_skupina','pohlavi','pocet_davek']
                ]


def drop_and_create(id, name):
    
    # drop old collections
    db.drop_collection(name)

    # create collections
    db.create_collection(name)

    # load CSV data from API to MongoDB
    print(f'Loading data from {collection_sources[id]}...', file=sys.stdout, sep = '')
    if name == "vaccination_demographic" or name == "vaccination_geographic":
        data_from_csv = pd.read_csv(collection_sources[id], usecols=collection_cols[id], parse_dates=["datum"])
    else:
        data_from_csv = pd.read_csv(collection_sources[id], usecols=collection_cols[id])
    data_dict = data_from_csv.to_dict('records')
    db[name].insert_many(data_dict)
    print(f'Data \'{name}\' was successfully updated to the database.', file=sys.stdout)


def update_data():
    for id,collection_name in enumerate(collection_names):
        drop_and_create(id,collection_name)


def update_population():
    kraj_data = pd.read_csv("https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv", usecols=['vuzemi_cis', 'vuzemi_txt', 'hodnota', 'casref_do', 'pohlavi_kod'])
    kraj_data = kraj_data.loc[kraj_data['casref_do'] == '2020-12-31']
    kraj_data = kraj_data.loc[kraj_data['vuzemi_cis'] == 100]   # kraj
    kraj_data = kraj_data.loc[kraj_data['pohlavi_kod'].isna()]  # NaN values
    kraj_data = kraj_data.groupby(kraj_data['vuzemi_txt']).max().reset_index()    # max NaN value (total for region)
    kraj_data.pop('pohlavi_kod')
    kraj_data.pop('vuzemi_cis')
    kraj_data.pop('casref_do')

    data_dict = kraj_data.to_dict('records')
    db.drop_collection('population_region')
    db['population_region'].insert_many(data_dict)
    print('Data', 'population_region', 'was successfully updated to the database.', file=sys.stdout)

    obec_data = pd.read_csv("https://www.czso.cz/documents/62353418/143520482/130181-21data043021.csv", usecols=['vuzemi_txt', 'vek_txt', 'pohlavi_kod', 'hodnota'])
    obec_data = obec_data.groupby(['vuzemi_txt', 'vek_txt']).sum().reset_index()
    obec_data.pop('pohlavi_kod')
    age = []
    for row in obec_data['vek_txt']:
        row = re.search("^[0-9]+(?=\s)|(?<=^Od\s)[0-9]+", row).group()
        age.append(int(row))
    obec_data['vek'] = age
    obec_data.pop('vek_txt')
    
    data_dict = obec_data.to_dict('records')
    db.drop_collection('population_villages')
    db['population_villages'].insert_many(data_dict)
    print('Data', 'population_villages', 'was successfully updated to the database.', file=sys.stdout)


def update_deaths():
    covid_umrti = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv", usecols=['datum','vek'])
    covid_umrti['datum'] = pd.to_datetime(covid_umrti['datum'])
    bins = [0,15, 40, 65, 75, 85, 100]
    labels = ['0-14', '15-39', '40-64', '65-74', '75-84', '85+']
    covid_umrti['vek_txt'] = pd.cut(covid_umrti.vek, bins, labels = labels, right=False)  # creates age intervals
    covid_umrti.pop('vek')
    covid_umrti=covid_umrti.groupby([pd.Grouper(key='datum',freq='1W'),'vek_txt']).size().to_frame('covid_umrti') # group by date and age category
    covid_umrti=covid_umrti.reset_index()
    
    data_dict = covid_umrti.to_dict('records')
    db.drop_collection("covid_deaths")
    db['covid_deaths'].insert_many(data_dict)
    print('Data', 'covid_deaths', 'was successfully updated to the database.', file=sys.stdout)
    
    celkova_umrti_data = pd.read_csv("https://www.czso.cz/documents/62353418/155512385/130185-21data110221.csv", usecols=['casref_do', 'vek_txt', 'hodnota'], parse_dates=["casref_do"])
    celkova_umrti_data = celkova_umrti_data.rename(columns={'casref_do': 'datum','hodnota': 'celkove_umrti'})
    celkova_umrti_data = celkova_umrti_data[celkova_umrti_data['vek_txt']!='celkem'] # delete category celkem
    celkova_umrti_data = celkova_umrti_data.loc[(celkova_umrti_data['datum'] >= '2020-01-01') & (celkova_umrti_data['datum'] <= '2021-12-31')] # filter only 2 last years
    
    data_dict = celkova_umrti_data.to_dict('records')
    db.drop_collection('total_deaths')
    db['total_deaths'].insert_many(data_dict)
    print('Data', 'total_deaths', 'was successfully updated to the database.', file=sys.stdout)


def update_villages():
    print('Loading data from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv ...', file=sys.stdout, sep = '')
    collection_cols = ['datum','orp_kod','orp_nazev','kraj_nazev','nove_pripady']
    villages_df = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv", usecols=collection_cols, parse_dates=["datum"])
    villages_df = villages_df.groupby(['datum','orp_kod','orp_nazev','kraj_nazev']).sum().reset_index()
    villages_df_dict = villages_df.to_dict('records')
    db.drop_collection("villages")
    db["villages"].insert_many(villages_df_dict)
    print('Data \'villages\' was successfully updated to the database.', file=sys.stdout)


def update_incremental_stats_and_hospitalized():
    print('Loading data from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv ...', file=sys.stdout, sep = '')
    incremental_stats_cols = [
        'datum','prirustkovy_pocet_nakazenych', 'prirustkovy_pocet_vylecenych','prirustkovy_pocet_umrti',
        'prirustkovy_pocet_provedenych_testu', 'prirustkovy_pocet_provedenych_ag_testu'
    ]
    incremental_stats_df = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv", usecols=incremental_stats_cols,  parse_dates=["datum"]).sort_values(by=["datum"])
    
    print('Loading data from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv ...', file=sys.stdout, sep = '')
    hospitalized_df = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv", parse_dates=["datum"]).sort_values(by=["datum"])
    
    incremental_stats_df = incremental_stats_df.merge(hospitalized_df[["datum", "pacient_prvni_zaznam"]], how='left')
    incremental_stats_df.rename(columns={
        'prirustkovy_pocet_nakazenych': 'nakazenych',
        'prirustkovy_pocet_vylecenych': 'vyliecenych',
        'prirustkovy_pocet_umrti': "umrti",
        'prirustkovy_pocet_provedenych_testu': 'pcr_testov',
        'prirustkovy_pocet_provedenych_ag_testu': 'ag_testov',
        'pacient_prvni_zaznam': 'hospitalizovany'
    }, inplace=True)
    
    hospitalized_df = hospitalized_df.drop(["pacient_prvni_zaznam", "kum_pacient_prvni_zaznam", "umrti", "kum_umrti"], axis=1)

    hospitalized_df_dict = hospitalized_df.to_dict('records')
    incremental_stats_df_dict = incremental_stats_df.to_dict('records')

    db.drop_collection("hospitalized_stats")
    db.drop_collection("incremental_stats")
    db["hospitalized_stats"].insert_many(hospitalized_df_dict)
    print('Data \'hospitalized_stats\' was successfully updated to the database.', file=sys.stdout)
    db["incremental_stats"].insert_many(incremental_stats_df_dict)
    print('Data \'incremental_stats\' was successfully updated to the database.', file=sys.stdout)
    

if __name__ == "__main__":
    update_data()
    update_incremental_stats_and_hospitalized()
    update_villages()
    update_deaths()
    update_population()
