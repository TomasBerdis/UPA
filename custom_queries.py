import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import matplotlib.pyplot as plt


def load_deaths():
    covid_umrti = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv", usecols=['datum','vek'])
    covid_umrti['datum'] = pd.to_datetime(covid_umrti['datum'])
    bins = [0,15, 40, 65, 75, 85, 100]
    labels = ['0-14', '15-39', '40-64', '65-74', '75-84', '85+']
    covid_umrti['vek_txt'] = pd.cut(covid_umrti.vek, bins, labels = labels, right=False)  # creates age intervals
    covid_umrti.pop('vek')
    covid_umrti=covid_umrti.groupby([pd.Grouper(key='datum',freq='1W'),'vek_txt']).size().to_frame('covid_umrti') # group by date and age category
    covid_umrti=covid_umrti.reset_index()
    
    
    celkova_umrti_data = pd.read_csv("https://www.czso.cz/documents/62353418/155512385/130185-21data110221.csv", usecols=['casref_do', 'vek_txt', 'hodnota'], parse_dates=["casref_do"])
    celkova_umrti_data = celkova_umrti_data.rename(columns={'casref_do': 'datum','hodnota': 'celkove_umrti'})
    celkova_umrti_data = celkova_umrti_data[celkova_umrti_data['vek_txt']!='celkem'] # delete category celkem
    celkova_umrti_data = celkova_umrti_data.loc[(celkova_umrti_data['datum'] >= '2020-01-01') & (celkova_umrti_data['datum'] <= '2021-12-31')] # filter only 2 last years

    return covid_umrti, celkova_umrti_data
    
def load_hospitalized():
   
    hospitalized_df = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv", parse_dates=["datum"]).sort_values(by=["datum"])
      
    hospitalized_df = hospitalized_df.drop(["pacient_prvni_zaznam", "kum_pacient_prvni_zaznam", "umrti", "kum_umrti"], axis=1)

    return hospitalized_df


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
    
    hospitalized = load_hospitalized()
   
    # clear nan values
    hospitalized_clear=hospitalized.dropna(how='any').reset_index()
    
    # set seaborn theme
    sns.set_theme(style="darkgrid")
    
    # create figure
    fig  = plt.figure(figsize=(17,10))
   
    
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


def Custom2():
    # 2 custom task - Poměr počtu zemřelých na Covid a zemřelých celkově (po měsících a podle věkových skupin)
    
    covid_deaths, total_deaths = load_deaths()

    # consistent vek_txt values
    total_deaths['vek_txt'] = total_deaths['vek_txt'].str.replace('85 a více', '85+')
    
    # inner join over total and covid deaths
    merged_deaths=pd.merge(total_deaths,covid_deaths, how='inner', on=['datum','vek_txt'])

    # group data to 1 month intervals
    merged_deaths=merged_deaths.groupby([pd.Grouper(key='datum',freq='1M'),'vek_txt']).sum().reset_index()

    # set format of date 
    merged_deaths['datum'] = merged_deaths['datum'].dt.strftime("%Y-%m")
   
    # create figure for second task
    fig = plt.figure(figsize=(17,10))
    # set width of bars
    
    # make the custum group bar plot showing death ratio between covid and total deaths based on age
    
    # create custom bars
    barWidth = 0.15
    
    # compute x postions for every age group
    cat=merged_deaths[merged_deaths["vek_txt"] == '0-14']
    r1 = np.arange(len(cat))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    r6 = [x + barWidth for x in r5]
    wids=[r1,r2,r3,r4,r5,r6]
    leg=['0-14','15-39','40-64','65-74','75-84', "85+"]
    cols=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=False)

    # plot individual charts for every age group
    for age,wids,col in zip(leg,wids, cols):
        
        # filter data by age
        cat=merged_deaths[merged_deaths["vek_txt"] == age]
        
        # total deaths
        plt.bar(wids, cat['celkove_umrti'], color=col, width=barWidth, edgecolor='white', label=age)

        # covid deaths
        plt.bar(wids, cat['covid_umrti'], color='red', width=barWidth, edgecolor='white')
       

    
    # add xticks on the middle of the group bars
    plt.xlabel('Datum', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(r1))],cat['datum'])
    plt.tick_params(axis='x', labelrotation= 30, labelsize=7)

    # y label
    plt.ylabel('Celková úmrtí',fontweight='bold')
    

    # function to add custom legend item
    def add_patch(legend):
        ax = legend.axes

        handles, labels = ax.get_legend_handles_labels()
        handles.append(Patch(facecolor='red', edgecolor='white'))
        labels.append("covid")

        legend._legend_box = None
        legend._init_legend_box(handles, labels)
        legend._set_loc(legend._loc)
        legend.set_title('Věk')

    # set title
    plt.title("Poměr počtu zemřelých na Covid a zemřelých celkově podle věku",fontsize=20)

    # create legend and add custom item
    lgd=plt.legend()
    add_patch(lgd)

    # show graphics
    plt.show()


if __name__ == "__main__":
    sns.set_style("dark")
    sns.set_context("talk")

    # queries
    # A1()
    B()
    Custom1()
    # Custom2()