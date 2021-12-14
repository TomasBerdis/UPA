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

# C

# Custom 1

# Custom 2