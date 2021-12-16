from numpy import nan
from pymongo import MongoClient
import pandas as pd
import sys
from datetime import datetime

# connect to MongoDB
print('Connecting to the database...', file=sys.stdout)
client = MongoClient('localhost', 27017)

# create/get database
db = client['upa']

# A1
incremental_stats = pd.DataFrame(list(db['incremental_stats'].find()))
del incremental_stats['_id']    # remove _id column
incremental_stats.to_csv('A1.csv', index=False)

# A3
vaccination_basic_overview = pd.DataFrame(db['vaccination_basic_overview'].find({}, {
    "_id":1,
    "kraj_nazev":1,
    "vekova_skupina":1,
    "pohlavi":1,
    "pocet_davek":1,
    "vakcina": 1,
    "poradi_davky": 1

})).drop(["_id"], axis=1).set_index("kraj_nazev")

vaccination_basic_overview.to_csv("A3.csv")

# B
villages = pd.DataFrame(list(db['villages'].find()))
del villages['_id']    # remove _id column
villages.to_csv('B.csv', index=False)

population_region = pd.DataFrame(list(db['population_region'].find()))
del population_region['_id']    # remove _id column
population_region.to_csv('B_population.csv', index=False)

# C1

fifty_most_populated_towns = [
    'Praha', 'Brno', 'Ostrava', 'Plzeň',
    'Olomouc', 'České Budějovice','Černošice',
    'Hradec Králové','Liberec','Pardubice','Kladno',
    'Ústí nad Labem','Brandýs nad Labem-Stará Boleslav',
    'Mladá Boleslav','Frýdek-Místek','Teplice','Jihlava',
    'Opava','Zlín','Prostějov','Znojmo','Uherské Hradiště',
    'Karlovy Vary','Havířov','Kolín','Chrudim','Chomutov',
    'Tábor','Přerov','Česká Lípa','Děčín','Sokolov','Třebíč',
    'Most','Říčany','Šlapanice','Příbram','Šumperk','Kroměříž',
    'Beroun','Vsetín','Trutnov','Karviná','Benešov','Hodonín',
    'Náchod','Břeclav','Litoměřice','Nýřany','Blansko', 'Jablonec nad Nisou'
 ]

positive_in_towns = pd.DataFrame(db['villages'].aggregate([
    {"$match": { "orp_nazev": { "$in": fifty_most_populated_towns}, "$expr": { "$lt": [{ "$toDate": datetime.strptime("31/12/20", '%d/%m/%y').isoformat()}, "$datum"]}}},
    { "$group": {
        "_id": {
          "orp_nazev": "$orp_nazev",
          "truncatedOrderDate": {"$dateTrunc": { "date": "$datum", "unit": "quarter"}}
          },
        "total": { "$sum": "$nove_pripady" }
  }},
  {"$project":{
      "_id": "$_id.truncatedOrderDate",
      "orp_nazev": "$_id.orp_nazev",
      "pocet_nakazených": "$total",
  }},
])).sort_values("orp_nazev", ascending=False)

vaccinated_in_towns = pd.DataFrame(db['vaccination_geographic'].aggregate([
    {"$match": { "orp_bydliste": { "$in": fifty_most_populated_towns}, "$expr": { "$lt": [{ "$toDate": datetime.strptime("31/12/20", '%d/%m/%y').isoformat()}, "$datum"]}}},
    { "$group": {
        "_id": {
          "orp_nazev": "$orp_bydliste",
          "truncatedOrderDate": {"$dateTrunc": { "date": "$datum", "unit": "quarter"}}
          },
        "total": { "$sum": {
          "$cond": {
            "if": {
               "$or": [
                 {"$and": [{"$eq": ["$vakcina", 'Comirnaty']}, {"$gte": ["$poradi_davky", 2]}]},
                 {"$and": [{"$eq": ["$vakcina", 'COVID-19 Vaccine Janssen']}, {"$gte": ["$poradi_davky", 1]}]},
                 {"$and": [{"$eq": ["$vakcina", 'SPIKEVAX']}, {"$gte": ["$poradi_davky", 2]}]},
                 {"$and": [{"$eq": ["$vakcina", 'VAXZEVRIA']}, {"$gte": ["$poradi_davky", 2]}]}
               ]
              }, "then": "$pocet_davek", "else": 0
            } 
          } 
        }
  }},
  {"$project":{
      "_id": "$_id.truncatedOrderDate",
      "orp_nazev": "$_id.orp_nazev",
      "pocet_ockovanych": "$total",
  }},
])).sort_values("orp_nazev", ascending=False)

people_in_towns = pd.DataFrame(db['population_villages'].aggregate([
    {"$match": { "vuzemi_txt": { "$in": fifty_most_populated_towns}, }},
    {
      "$group": {
          "_id": "$vuzemi_txt",
          "0-14": { "$sum": { "$cond": { "if": { "$and": [{"$gte": [ "$vek", 0 ]}, {"$lte": [ "$vek", 14 ]}]} ,"then": "$hodnota", "else": 0 } } },
          "15-59": { "$sum": { "$cond": { "if": { "$and": [{"$gte": [ "$vek", 15 ]}, {"$lte": [ "$vek", 59 ]}]} ,"then": "$hodnota", "else": 0 } } },
          "nad 59": { "$sum": { "$cond": { "if": { "$gte": [ "$vek", 60 ] } ,"then": "$hodnota", "else": 0 } } },
        }
    }
])).rename({"_id": "orp_nazev"}, axis=1).sort_values(by=["orp_nazev"], ascending=False)

positive_in_towns = positive_in_towns.pivot_table('pocet_nakazených', ["orp_nazev"], '_id').reset_index()
vaccinated_in_towns = vaccinated_in_towns.pivot_table('pocet_ockovanych', ["orp_nazev"], '_id').reset_index()

positive_in_towns = positive_in_towns.rename({
  datetime.strptime("1/1/21", '%d/%m/%y'): "pocet_nakazenych_Q1",
  datetime.strptime("1/4/21", '%d/%m/%y'): "pocet_nakazenych_Q2",
  datetime.strptime("1/7/21", '%d/%m/%y'): "pocet_nakazenych_Q3",
  datetime.strptime("1/10/21", '%d/%m/%y'): "pocet_nakazenych_Q4"
}, axis=1)

vaccinated_in_towns = vaccinated_in_towns.rename({
  datetime.strptime("1/1/21", '%d/%m/%y'): "pocet_ockovanich_Q1",
  datetime.strptime("1/4/21", '%d/%m/%y'): "pocet_ockovanich_Q2",
  datetime.strptime("1/7/21", '%d/%m/%y'): "pocet_ockovanich_Q3",
  datetime.strptime("1/10/21", '%d/%m/%y'): "pocet_ockovanich_Q4"
}, axis=1)


positive_vaccineted_in_towns = positive_in_towns.merge(vaccinated_in_towns[["orp_nazev", "pocet_ockovanich_Q1", "pocet_ockovanich_Q2", "pocet_ockovanich_Q3", "pocet_ockovanich_Q4"]], how='left')
positive_vaccineted_in_towns.merge(people_in_towns[["orp_nazev", "0-14", "15-59", "nad 59"]], how='left').set_index("orp_nazev").to_csv("C1-before.csv")


# Custom 1
hospitalized_stats = pd.DataFrame(list(db['hospitalized_stats'].find()))
del hospitalized_stats['_id']    # remove _id column
hospitalized_stats.to_csv('Custom_1_hospitalized.csv', index=False)

# Custom 2
total_deaths = pd.DataFrame(list(db['total_deaths'].find()))
del total_deaths['_id']    # remove _id column
total_deaths.to_csv('Custom_2_total_deaths.csv', index=False)

covid_deaths = pd.DataFrame(list(db['covid_deaths'].find()))
del covid_deaths['_id']    # remove _id column
covid_deaths.to_csv('Custom_2_covid_deaths.csv', index=False)
