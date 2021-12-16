from pymongo import MongoClient
import pandas
import sys

# connect to MongoDB
print('Connecting to the database...', file=sys.stdout)
client = MongoClient('localhost', 27017)

# create/get database
db = client['upa']

# A1
incremental_stats = pandas.DataFrame(list(db['incremental_stats'].find()))
del incremental_stats['_id']    # remove _id column
incremental_stats.to_csv('A1.csv', index=False)

# A3

# B
villages = pandas.DataFrame(list(db['villages'].find()))
del villages['_id']    # remove _id column
villages.to_csv('B.csv', index=False)

population_region = pandas.DataFrame(list(db['population_region'].find()))
del population_region['_id']    # remove _id column
population_region.to_csv('B_population.csv', index=False)

# C

# Custom 1
hospitalized_stats = pandas.DataFrame(list(db['hospitalized_stats'].find()))
del hospitalized_stats['_id']    # remove _id column
hospitalized_stats.to_csv('Custom_1_hospitalized.csv', index=False)

# Custom 2
total_deaths = pandas.DataFrame(list(db['total_deaths'].find()))
del total_deaths['_id']    # remove _id column
total_deaths.to_csv('Custom_2_total_deaths.csv', index=False)

covid_deaths = pandas.DataFrame(list(db['covid_deaths'].find()))
del covid_deaths['_id']    # remove _id column
covid_deaths.to_csv('Custom_2_covid_deaths.csv', index=False)
