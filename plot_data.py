import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt


# Data from John Hopkins University
def pull_data():

    recovered = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
    deaths = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
    cases = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

    rec = pd.read_csv(recovered)
    deaths = pd.read_csv(deaths)
    cases = pd.read_csv(cases)

    return (rec, deaths, cases)

def clean_data():

    rec, deaths, cases = pull_data()

    rec = rec.loc[rec['Province/State'] == 'United Kingdom']

    rec.drop(['Province/State','Lat','Long'], axis=1, inplace=True)
    deaths.drop(['Province/State','Lat','Long'], axis=1, inplace=True)
    cases.drop(['Province/State','Lat','Long'], axis=1, inplace=True)

    rec.dropna(inplace=True)
    deaths.dropna(inplace=True)
    cases.dropna(inplace=True)

    rec.reset_index(drop=True, inplace=True)
    deaths.reset_index(drop=True, inplace=True)
    cases.reset_index(drop=True, inplace=True)

    return rec, deaths, cases

# Data from European Centre for Disease Prevention and Control (ECDC)
def main():
    url='https://covid.ourworldindata.org/data/ecdc/full_data.csv'
    df = pd.read_csv(url, parse_dates=['date'])

    df.fillna(0, inplace=True)

    df_group = df[['date','location','total_cases','total_deaths']]
    group = df_group.groupby(['date','location'], as_index=False).sum()

    date_format = '%d-%m'
    group['date'] = group['date'].dt.strftime(date_format)

    uk_data = group[group.values == 'United Kingdom']
    world_data = group[group.values == 'World']

    uk_data.reset_index(drop=True, inplace=True)
    uk_data.drop(range(0,70), inplace=True)
    world_data.reset_index(drop=True, inplace=True)

    dates = range(0, len(uk_data))

    plt.plot(dates, uk_data['total_cases'], '-g')
    plt.plot(dates, uk_data['total_deaths'], '-r')

    plt.title('COVID-19 in the United Kingdom')
    plt.ylabel('Total Cases')
    plt.xlabel('Date')
    plt.legend(['Cases', 'Deaths'], loc='upper left')
    plt.grid(axis='y', linestyle='-')
    plt.savefig('plot.png')
    plt.show()


if __name__=="__main__":
    main()
