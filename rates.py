import pandas as pd
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

def slope(x1, x2):
    if x1 is 0:
        return 0
    else:
        return (abs(x2 - x1))/x1

def get_rates(df):
    dict = {}
    df.reset_index(drop=True, inplace=True)
    for index, row in df.iterrows():

        if (index is (len(df) - 2)):
            break

        next_row = df.iloc[index + 1]
        dict[next_row['date']] = slope(row['total_cases'], next_row['total_cases'])

    return dict

def main():
    url='https://covid.ourworldindata.org/data/ecdc/full_data.csv'
    df = pd.read_csv(url, parse_dates=['date'])

    df.fillna(0, inplace=True)

    df_group = df[['date','location','total_cases','total_deaths']]
    group = df_group.groupby(['date','location'], as_index=False).sum()

    date_format = '%d-%m'
    group['date'] = group['date'].dt.strftime(date_format)

    uk_data = group[group.values == 'United Kingdom']
    spain_data = group[group.values == 'Spain']
    italy_data = group[group.values == 'Italy']
    us_data = group[group.values == 'United States']
    world_data = group[group.values == 'World']

    uk_data.reset_index(drop=True, inplace=True)
    spain_data.reset_index(drop=True, inplace=True)
    italy_data.reset_index(drop=True, inplace=True)
    us_data.reset_index(drop=True, inplace=True)
    world_data.reset_index(drop=True, inplace=True)

    uk_rate = get_rates(uk_data.tail(30))
    spain_rate = get_rates(spain_data.tail(30))
    italy_rate = get_rates(italy_data.tail(30))
    us_rate = get_rates(us_data.tail(30))
    world_rate = get_rates(world_data.tail(30))


    """
    print(type(list(uk_rate.keys())[0]))
    days = mdates.drange(list(uk_rate.keys())[0].date(), dt.date.today(), dt.timedelta(days=1))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    """

    days = list(spain_rate.keys())
    fig, ax = plt.subplots(2, 2)
    ax[0, 0].plot(days, list(spain_rate.values()), label='Spain')
    ax[0, 0].set_title('Spain')
    ax[0, 1].plot(days, list(italy_rate.values()), label='Italy')
    ax[0, 1].set_title('Italy')
    ax[1, 0].plot(days, list(us_rate.values()), label='United States')
    ax[1, 0].set_title('United States')
    ax[1, 1].plot(days, list(uk_rate.values()), label='United Kingdom')
    ax[1, 1].set_title('United Kingdom')
    plt.gcf().autofmt_xdate()
    fig.savefig('rates.png')
    fig.show()



if __name__=="__main__":
    main()
