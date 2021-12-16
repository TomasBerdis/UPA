import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import datetime


def A1():
    incremental_stats = pd.read_csv("A1.csv", parse_dates=["datum"]).sort_values(by=["datum"])
    test_stats = pd.DataFrame(data=incremental_stats, columns=['datum'])
    test_stats['Provedené testy'] = incremental_stats['pcr_testov'] + incremental_stats['ag_testov']
    del incremental_stats['pcr_testov']
    del incremental_stats['ag_testov']
    del incremental_stats['umrti']

    incremental_stats.rename(columns = {'datum':'Datum', 'nakazenych':'Nově nakažení', 'vyliecenych':'Nově vyléčení', 'hospitalizovany':'Nově hospitalizovaní'}, inplace = True)
    test_stats.rename(columns = {'datum':'Datum'}, inplace=True)

    fig = plt.figure(figsize=(20,10))

    fig.add_subplot(211)
    l_plot = sns.lineplot(x='Datum', y='value', hue='Proměnná', 
             data=pd.melt(incremental_stats, ['Datum'], var_name='Proměnná'))
    l_plot.set(xlabel ="Datum", ylabel = "Hodnota", title ='Statistiky v rámci ČR')
    
    fig.add_subplot(212)
    sns.lineplot(x='Datum', y='Provedené testy', 
             data=test_stats)

    plt.show()


def B():
    population = pd.read_csv("B_population.csv")
    population.rename(columns = {'vuzemi_txt':'kraj_nazev'}, inplace=True)
    villages = pd.read_csv("B.csv", parse_dates=["datum"]).sort_values(by=["datum"])
    del villages['orp_kod']
    del villages['orp_nazev']
    translations = {'Královéhradecký kraj':'HKK',
                    'Jihočeský kraj':'JHČ',
                    'Jihomoravský kraj':'JHM',
                    'Karlovarský kraj':'KVK',
                    'Liberecký kraj':'LBK',
                    'Moravskoslezský kraj':'MSK',
                    'Olomoucký kraj':'OLK',
                    'Pardubický kraj':'PAK',
                    'Plzeňský kraj':'PLK',
                    'Hlavní město Praha':'Praha',
                    'Středočeský kraj':'STČ',
                    'Ústecký kraj':'ULK',
                    'Kraj Vysočina':'VYS',
                    'Zlínský kraj':'ZLK'}
    for key, value in translations.items():
        villages['kraj_nazev']   = villages['kraj_nazev'].str.replace(key, value)
        population['kraj_nazev'] = population['kraj_nazev'].str.replace(key, value)

    quarter1 = pd.DataFrame(data=villages)
    quarter1 = quarter1[quarter1.datum.between('2021-01', '2021-03')]
    quarter1 = quarter1.groupby(['datum', 'kraj_nazev'], as_index=False)['nove_pripady'].sum()
    quarter1['datum'] = pd.to_datetime(quarter1['datum']) # convert Date to Datetime
    quarter1 = quarter1.groupby('kraj_nazev')['nove_pripady'].sum()
    quarter1 = quarter1.reset_index()
    quarter1 = pd.merge(quarter1, population)
    quarter1.rename(columns = {'kraj_nazev': 'Kraj', 'nove_pripady':'Nové případy' , 'hodnota':'Počet obyvatel'}, inplace=True)
    quarter1['Přepočet na jednoho obyvatele'] = quarter1['Nové případy'] / quarter1['Počet obyvatel']
    line_data1 = pd.DataFrame(quarter1[['Kraj', 'Přepočet na jednoho obyvatele']])
    del quarter1['Přepočet na jednoho obyvatele']

    ax1 = sns.set_style(style=None, rc=None)
    fig, ax1 = plt.subplots(figsize=(12,6))
    sns.lineplot(data = line_data1['Přepočet na jednoho obyvatele'], marker='o', sort=False, ax=ax1)
    ax2 = ax1.twinx()
    bar_data1 = pd.melt(quarter1, ['Kraj'], var_name='Proměnná', value_name='Hodnota')
    plot_b1 = sns.barplot(data = bar_data1, x='Kraj', y='Hodnota', hue='Proměnná', alpha=0.5, ax=ax2)
    plot_b1.set(title ='1. čtvrtletí 2021')

    plt.show()

    
def Custom1():
    # 1 custom task - Statistiky hospitalizovaných v rámci republiky
        ## Průběh nákazy u hospitalizovaných
        ## Typ hospitalizace
    
    hospitalized = pd.read_csv("Custom_1_hospitalized.csv")
   
    # clear nan values
    hospitalized_clear=hospitalized.dropna(how='any').reset_index()
    
    # set seaborn theme
    sns.set_theme(style="darkgrid")
    
    # create figure
    fig  = plt.figure(figsize=(16,9))
   
    
    # set params for subplot about hospitalized course of infection
    plot_1=fig.add_subplot(211)
    plot_1.xaxis.set_major_locator(ticker.MaxNLocator())
    date_format=mdates.DateFormatter('%Y-%m')
    plot_1.xaxis.set_major_formatter(date_format)
    plot_1.tick_params(axis='x', labelrotation= 30, labelsize=7)
    plot_1.set_title("Statistiky hospitalizovaných v rámci ČR",fontsize=20)
    plot_1.set_xlabel('Datum', fontweight='bold')
    plot_1.set_ylabel('Počet hospitalizovaných', fontweight='bold')

    # create stackplot
    y=[hospitalized_clear['stav_bez_priznaku'],hospitalized_clear['stav_lehky'],hospitalized_clear['stav_stredni'], hospitalized_clear['stav_tezky']]
    plot_1.stackplot(hospitalized_clear['datum'],y, alpha=0.8, labels=['bez příznaků', 'lehký', 'střední', 'těžký'])
    plot_1.legend(fontsize=9, loc='upper left', title='Průběh')
    plot_1.set_xlim([hospitalized_clear['datum'][0], hospitalized_clear['datum'].iloc[-1]])

    # set params for subplot about type of hospitalization
    plot_2=fig.add_subplot(212)
    plot_2.xaxis.set_major_locator(ticker.MaxNLocator())
    plot_2.xaxis.set_major_formatter(date_format)
    plot_2.tick_params(axis='x', labelrotation= 30, labelsize=7)

    # create stackplot
    y=[hospitalized_clear['jip'],hospitalized_clear['kyslik'],hospitalized_clear['hfno'], hospitalized_clear['upv'], hospitalized_clear['ecmo'],hospitalized_clear['tezky_upv_ecmo']]
    plot_2.stackplot(hospitalized_clear['datum'],y, alpha=0.8, labels=['jip','kyslík', 'hfno', 'upv', 'ecmo', 'těžký upv ecmo'])
    plot_2.legend(fontsize=9, loc='upper left', title="Typ hospitalizace")
    plot_2.set_xlabel('Datum', fontweight='bold')
    plot_2.set_ylabel('Počet hospitalizovaných', fontweight='bold')
    plot_2.set_xlim([hospitalized_clear['datum'][0], hospitalized_clear['datum'].iloc[-1]])

    # show graphics
    plt.show()


def Custom2():
    # 2 custom task - Poměr počtu zemřelých na Covid a zemřelých celkově (po měsících a podle věkových skupin)
    
    covid_deaths = pd.read_csv("Custom_2_covid_deaths.csv")
    total_deaths = pd.read_csv("Custom_2_total_deaths.csv")

    # consistent vek_txt values
    total_deaths['vek_txt'] = total_deaths['vek_txt'].str.replace('85 a více', '85+')
    
    # inner join over total and covid deaths
    merged_deaths=pd.merge(total_deaths,covid_deaths, how='inner', on=['datum','vek_txt'])
    
    # set datetime format
    merged_deaths['datum'] = pd.to_datetime(merged_deaths['datum'])

    # group data 1 month interval
    merged_deaths=merged_deaths.groupby([pd.Grouper(key='datum',freq='1M'),'vek_txt']).sum().reset_index()  

    # filter last year in data
    merged_deaths=merged_deaths[(merged_deaths['datum'] > (merged_deaths['datum'].iloc[-1]- datetime.timedelta(days=365))) ].reset_index()
    merged_deaths.pop('index')

    # group data to 3 months intervals
    merged_deaths=merged_deaths.groupby([pd.Grouper(key='datum',freq='3MS'),'vek_txt']).sum().reset_index()

    # set format of date 
    merged_deaths['datum'] = merged_deaths['datum'].dt.strftime("%Y-%m")  

    # create new dataframe for categorcal type of death covid or normal
    new_dataframe=pd.DataFrame(columns=['Od','úmrtí','Úmrtí', 'věk'])

    for _,row in merged_deaths.iterrows():
        new_dataframe = new_dataframe.append({'Od' : row['datum'], 'úmrtí' : row['celkove_umrti'],'Úmrtí' : 'Celkově', 'věk' :row['vek_txt']}, ignore_index=True)
        new_dataframe = new_dataframe.append({'Od' : row['datum'], 'úmrtí' : row['covid_umrti'],'Úmrtí' : 'Covid', 'věk' :row['vek_txt']},ignore_index=True)
       
    # create 4 plots each one for 3 months interval and compare covid deaths to total deaths based on a age group
    g= sns.catplot(x='věk', y='úmrtí', col= 'Od', data=new_dataframe, kind='bar', hue='Úmrtí', col_wrap=2, palette=['darkblue','red'])
    g.fig.subplots_adjust(top=0.9, hspace=0.2)
    g.fig.suptitle('Čtvrletní poměr celkového a covid úmrtí za poslední rok',fontsize=20)
    g.set_titles("{col_var}: {col_name} ")
    
    # set x labels for each sublot
    for ax in g.axes.flatten():
        ax.tick_params(labelbottom=True)
    
    # show graphics
    plt.show()


if __name__ == "__main__":
    sns.set_style("dark")
    sns.set_context("talk")

    # queries
    A1()
    B()
    Custom1()
    Custom2()
