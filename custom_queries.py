import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
from sklearn.preprocessing import MinMaxScaler

def A1():

    # load and filter data
    incremental_stats = pd.read_csv("A1.csv", parse_dates=["datum"]).sort_values(by=["datum"])
    test_stats = pd.DataFrame(data=incremental_stats, columns=['datum'])
    test_stats['Provedené testy'] = incremental_stats['pcr_testov'] + incremental_stats['ag_testov']
    del incremental_stats['pcr_testov']
    del incremental_stats['ag_testov']
    del incremental_stats['umrti']

    # renaming collumns
    incremental_stats.rename(columns = {'datum':'Datum', 'nakazenych':'Nově nakažení', 'vyliecenych':'Nově vyléčení', 'hospitalizovany':'Nově hospitalizovaní'}, inplace = True)
    test_stats.rename(columns = {'datum':'Datum'}, inplace=True)
    
    # join stats
    stats=pd.merge(left=incremental_stats, right=test_stats)

    # group by 1 month
    stats=stats.groupby([pd.Grouper(key='Datum',freq='1M')]).sum().reset_index()

    # fig size
    plt.figure(figsize=(16,9))

    # line plot 
    l_plot = sns.lineplot(x='Datum', y='value', hue='Proměnná', 
             data=pd.melt(stats, ['Datum'], var_name='Proměnná'))
    l_plot.set(xlabel ="Datum", ylabel = "Hodnota", title ='Statistiky v rámci ČR')
    # logaritmic scale
    l_plot.set_yscale("log")

    # save image
    plt.savefig("A1.pdf")
    
    # show graphics
    plt.show()

def A3():
    vaccination_basic_overview = pd.read_csv("A3.csv")

    group = {
        '0-11': "0-24",
        '12-15': "0-24", 
        '16-17': "0-24",
        '18-24': "0-24",
        '25-29': "25-59",
        '30-34': '25-59',
        '35-39': '25-59',
        '40-44': '25-59',
        '45-49': '25-59',
        '50-54': '25-59',
        '55-59': '25-59',
        '60-64': 'nad 59',
        '65-69': 'nad 59',
        '70-74': 'nad 59',
        '75-79': 'nad 59',
        '80+': 'nad 59'
    }

    regions_names_map = {
        'Hlavní město Praha': 'PHA',
        'Středočeský kraj':'STC',
        'Jihočeský kraj':'JHC',
        'Plzeňský kraj':'PLK',
        'Karlovarský kraj':'KVK',
        'Ústecký kraj':'ULK',
        'Liberecký kraj':'LBK',
        'Královéhradecký kraj':'HKK',
        'Pardubický kraj':'PAK',
        'Olomoucký kraj':'OLK',
        'Moravskoslezský kraj':'MSK',
        'Jihomoravský kraj':'JHM',
        'Zlínský kraj':'ZLK',
        'Kraj Vysočina':'VYS'
    }

    gender_map = {
        'Z': 'Žena',
        'M': 'Muž'
    }

    vaccination_basic_overview = vaccination_basic_overview.assign(vekova_skupina=vaccination_basic_overview.vekova_skupina.map(group))
    vaccination_basic_overview = vaccination_basic_overview.assign(kraj_nazev=vaccination_basic_overview.kraj_nazev.map(regions_names_map))
    vaccination_basic_overview = vaccination_basic_overview.assign(pohlavi=vaccination_basic_overview.pohlavi.map(gender_map))
    vaccination_basic_overview = vaccination_basic_overview.rename({
        'kraj_nazev': 'Názov kraja',
        'vekova_skupina': 'Veková skupina',
        'pohlavi': 'Pohlavie',
        'pocet_davek': 'Počet dávok'
    }, axis=1)

    vaccination_basic_overview["Pohlavie"] = vaccination_basic_overview["Pohlavie"].fillna("Neznáme")
    vaccination_basic_overview = vaccination_basic_overview.drop(
        vaccination_basic_overview[
            ((vaccination_basic_overview["vakcina"] == 'Comirnaty') & (vaccination_basic_overview["poradi_davky"] < 2)) |
            ((vaccination_basic_overview["vakcina"] == 'COVID-19 Vaccine Janssen') & (vaccination_basic_overview["poradi_davky"] < 1)) |
            ((vaccination_basic_overview["vakcina"] == 'SPIKEVAX') & (vaccination_basic_overview["poradi_davky"] < 2)) |
            ((vaccination_basic_overview["vakcina"] == 'VAXZEVRIA') & (vaccination_basic_overview["poradi_davky"] < 2)) |
            ((vaccination_basic_overview["poradi_davky"] > 2)) | 
            ((vaccination_basic_overview["Pohlavie"] == "Neznáme"))].index)

    total_vaccination_basic_overview = vaccination_basic_overview.groupby(["Názov kraja"])["Počet dávok"].sum().reset_index()

    sns.set()
    fig1, ax1 = plt.subplots()

    plot = sns.barplot(ax=ax1, data=total_vaccination_basic_overview, x="Názov kraja", y="Počet dávok", color='r')
    plot.set_title("Počet provedených očkovaní v jednotlivých krajoch", fontsize=11.0)
    plot.grid(axis="y", color="black", alpha=.2, linewidth=.3, zorder=1)
    plot.set_facecolor("#f0f2f5")

    # save image
    plt.savefig("A3-1-graf.pdf")

    plt.show()

    fig2, ax2 = plt.subplots()

    total_gender_vaccination_basic_overview = vaccination_basic_overview.groupby(["Názov kraja", "Pohlavie"])["Počet dávok"].sum().reset_index()
    plot = sns.barplot(ax=ax2, data=total_gender_vaccination_basic_overview, x="Názov kraja", y="Počet dávok", hue="Pohlavie")
    plot.set_title("Počet provedených očkovaní v jednotlivých krajoch podľa pohlavia", fontsize=11.0)
    plot.grid(axis="y", color="black", alpha=.2, linewidth=.3, zorder=1)
    plot.set_facecolor("#f0f2f5")

    # save image
    plt.tight_layout()
    plt.savefig("A3-2-graf.pdf")

    plt.show()

    total_gender_age_vaccination_basic_overview = vaccination_basic_overview.groupby(["Názov kraja", "Pohlavie", "Veková skupina"])["Počet dávok"].sum().reset_index()
    plot = sns.catplot(data=total_gender_age_vaccination_basic_overview, x="Názov kraja", y="Počet dávok", col="Pohlavie", hue="Veková skupina", col_wrap=2, kind="bar",height=6, aspect=1.4, zorder=2)

    plot.set_titles("{col_name}", size=14).tight_layout()

    for ax in plot.axes.flatten():
        ax.grid(axis="y", color="black", alpha=.2, linewidth=.3, zorder=1)
        ax.set_facecolor("#f0f2f5")

    # save image
    plt.savefig("A3-3-graf.pdf")

    plt.show()

def B():
    # read csv data
    population = pd.read_csv("B_population.csv")
    population.rename(columns = {'vuzemi_txt':'kraj_nazev'}, inplace=True)
    villages = pd.read_csv("B.csv", parse_dates=["datum"]).sort_values(by=["datum"])
    del villages['orp_kod']
    del villages['orp_nazev']
    translations = {
        'Hlavní město Praha': 'PHA',
        'Středočeský kraj':'STC',
        'Jihočeský kraj':'JHC',
        'Plzeňský kraj':'PLK',
        'Karlovarský kraj':'KVK',
        'Ústecký kraj':'ULK',
        'Liberecký kraj':'LBK',
        'Královéhradecký kraj':'HKK',
        'Pardubický kraj':'PAK',
        'Olomoucký kraj':'OLK',
        'Moravskoslezský kraj':'MSK',
        'Jihomoravský kraj':'JHM',
        'Zlínský kraj':'ZLK',
        'Kraj Vysočina':'VYS'
    }
    for key, value in translations.items():
        villages['kraj_nazev']   = villages['kraj_nazev'].str.replace(key, value)
        population['kraj_nazev'] = population['kraj_nazev'].str.replace(key, value)

    # quartals charts
    quarters=[]
    dates=['2021-01', '2021-03','2021-07', '2021-10', '2022-01']
    print("Genrating latex tables for quartals showing best in covid counties in CR, query B")
    for quarter in range(4):
        quarter1 = pd.DataFrame(data=villages)
        quarter1 = quarter1[quarter1.datum.between(dates[quarter], dates[quarter+1])]
        quarter1 = quarter1.groupby(['datum', 'kraj_nazev'], as_index=False)['nove_pripady'].sum()
        quarter1['datum'] = pd.to_datetime(quarter1['datum']) # convert Date to Datetime
        quarter1 = quarter1.groupby('kraj_nazev')['nove_pripady'].sum()
        quarter1 = quarter1.reset_index()
        quarter1 = pd.merge(quarter1, population)
        quarter1.rename(columns = {'kraj_nazev': 'Kraj', 'nove_pripady':'Nové případy' , 'hodnota':'Počet obyvatel'}, inplace=True)
        quarter1['Přepočet na jednoho obyvatele'] = quarter1['Nové případy'] / quarter1['Počet obyvatel']
        quarter1.sort_values('Přepočet na jednoho obyvatele',inplace=True)
        quarter1.reset_index(drop=True,inplace=True)
        print(quarter1.to_latex(caption=str(quarter+1)+ ". čtvrtletí 2021", label=str(quarter+1)+ "Q"))
        quarters.append(quarter1)
        
    # plot first quartal
    line_data1 = pd.DataFrame(quarters[0][['Kraj', 'Přepočet na jednoho obyvatele']])
    del quarters[0]['Přepočet na jednoho obyvatele']
    ax1 = sns.set_style(style=None, rc=None)
    fig, ax1 = plt.subplots(figsize=(16,9))
    sns.lineplot(data = line_data1['Přepočet na jednoho obyvatele'], marker='o', sort=False, ax=ax1)
    ax2 = ax1.twinx()
    bar_data1 = pd.melt(quarters[0], ['Kraj'], var_name='Proměnná', value_name='Obyvatelé [mil]')
    plot_b1 = sns.barplot(data = bar_data1, x='Kraj', y='Obyvatelé [mil]', hue='Proměnná', alpha=0.7, ax=ax2)
    plot_b1.set_title('1. čtvrtletí 2021', fontsize=20)
    plot_b1.legend(loc='upper left', bbox_to_anchor=(0, 1), ncol=2)
    plot_b1.set_xlabel("Kraje")

    # save image
    plt.savefig("B.pdf")

    # show graphics
    plt.show()

def C():
    df = pd.read_csv("C1-before.csv")

    check_outliers = [
        "pocet_nakazenych_Q1", "pocet_nakazenych_Q2", "pocet_nakazenych_Q3", "pocet_nakazenych_Q4",
        "pocet_ockovanich_Q1", "pocet_ockovanich_Q2", "pocet_ockovanich_Q3", "pocet_ockovanich_Q4",
        "0-14", "15-59", "nad 59"
    ]
    print("=============================")
    print("Dotaz C1:")
    print("=============================")
    #odlahle hodnoty
    for col in check_outliers:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        print(f"interval pre: {col}, [{Q1 - 1.5 * IQR}; {(Q3 + 1.5 * IQR)}]")
        lower_bound = df[col].quantile(0.10)
        upper_bound = df[col].quantile(0.90)
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
        df[col] = df[col].astype("int64")
    print("=============================")

    # normalizacia poctu nakazených v prvom kvartáli
    min_max_scaler = MinMaxScaler()
    normalized_data = min_max_scaler.fit_transform(pd.DataFrame(df["pocet_nakazenych_Q1"]))
    df["pocet_nakazenych_Q1"] = pd.DataFrame(normalized_data, columns=["pocet_nakazenych_Q1"])

    # diskretizácia počtu vekov v 0-14 kategórii
    df["0-14"] = pd.cut(df["0-14"], bins=10)
    df.to_csv("C1-after.csv")
    
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
    
    #set datatime format
    hospitalized_clear['datum'] = pd.to_datetime(hospitalized_clear['datum'])
    date_format=mdates.DateFormatter('%Y-%m')

    # set params for subplot about hospitalized course of infection
    plot_1=fig.add_subplot(211)
    plot_1.xaxis.set_major_locator(ticker.MaxNLocator())
    plot_1.xaxis.set_major_formatter(date_format)
    plot_1.tick_params(axis='x', labelrotation= 30, labelsize=10)
    plot_1.set_title("Statistiky hospitalizovaných v rámci ČR",fontsize=20)
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
    plot_2.tick_params(axis='x', labelrotation= 30, labelsize=10)

    # create stackplot
    y=[hospitalized_clear['jip'],hospitalized_clear['kyslik'],hospitalized_clear['hfno'], hospitalized_clear['upv'], hospitalized_clear['ecmo'],hospitalized_clear['tezky_upv_ecmo']]
    plot_2.stackplot(hospitalized_clear['datum'],y, alpha=0.8, labels=['jip','kyslík', 'hfno', 'upv', 'ecmo', 'těžký upv ecmo'])
    plot_2.legend(fontsize=9, loc='upper left', title="Typ hospitalizace")
    plot_2.set_xlabel('Datum', fontweight='bold')
    plot_2.set_ylabel('Počet hospitalizovaných', fontweight='bold')
    plot_2.set_xlim([hospitalized_clear['datum'][0], hospitalized_clear['datum'].iloc[-1]])

    # save image
    plt.savefig("Custom1.pdf")

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

    # save image
    plt.savefig("Custom2.pdf")

    # show graphics
    plt.show()


if __name__ == "__main__":
    sns.set_style("dark")
    sns.set_context("talk")

    # queries
    A1()
    A3()
    B()
    C()
    Custom1()
    Custom2()
