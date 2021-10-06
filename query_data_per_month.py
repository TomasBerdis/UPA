from pymongo import MongoClient
import pandas
import sys
import matplotlib.pyplot as plt

# connect to MongoDB
print('Connecting to the database...', file=sys.stdout)
client = MongoClient('localhost', 27017)

# create/get database
db = client['upa']

## NAKAZENI/VYLECENI
nakazeni_vyleceni = pandas.DataFrame(list(db['nakazeni_vyleceni'].find()))
# DatetimeIndex is needed for grouping by month
nakazeni_vyleceni['datum'] = pandas.to_datetime(nakazeni_vyleceni['datum']) # convert Date to Datetime
nakazeni_vyleceni = nakazeni_vyleceni.set_index('datum')
nakazeni_vyleceni = nakazeni_vyleceni.groupby([pandas.Grouper(freq='M')]).sum()

## HOSPITALIZACE
hospitalizace = pandas.DataFrame(list(db['hospitalizace'].find()))
hospitalizace['datum'] = pandas.to_datetime(hospitalizace['datum'])
hospitalizace = hospitalizace.set_index('datum')
hospitalizace = hospitalizace.groupby([pandas.Grouper(freq='M')]).sum()

## TESTY
testy = pandas.DataFrame(list(db['testy'].find()))
testy['datum'] = pandas.to_datetime(testy['datum'])
testy = testy.set_index('datum')
testy = testy.groupby([pandas.Grouper(freq='M')]).sum()
testy_total = pandas.DataFrame({"Testy": (testy['pocet_PCR_testy'] + testy['pocet_AG_testy'])})

plot_frame = hospitalizace.join(testy_total)
plot_frame = plot_frame.join(nakazeni_vyleceni)
#plot_frame.reset_index()
print(plot_frame)

plot_frame.plot.line()
plt.show()