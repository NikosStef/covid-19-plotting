import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

DAYS = 50
COUNTRIES = ['United Kingdom', 'Spain', 'Italy', 'United States', 'World']
X_PLOTS = 3
Y_PLOTS = 2

def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)

    return smoothed_points

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

def select_location(df, country:str):
        temp = df[df.values == country]
        temp.reset_index(drop=True, inplace=True)
        return temp

def grouped_data():
    url='https://covid.ourworldindata.org/data/ecdc/full_data.csv'
    df = pd.read_csv(url, parse_dates=['date'])

    df.fillna(0, inplace=True)

    df_group = df[['date','location','total_cases','total_deaths']]
    group = df_group.groupby(['date','location'], as_index=False).sum()
    return group

def main():

    group = grouped_data()

    # *** TO-DO: Minimize the number of loops ***
    container = {}
    for location in COUNTRIES:
        container.update({location : select_location(group, location)})

    for location in COUNTRIES:
        _buff = get_rates(container.get(location).tail(DAYS))
        container.update({location : _buff})

    for location in COUNTRIES:
        _curr = container.get(location)
        _temp = smooth_curve(_curr.values())
        for index, item in enumerate(_curr.keys()):
            container.get(location).update({item : _temp[index]})

    days = range(0, DAYS-2)

    fig, axs = plt.subplots(X_PLOTS, Y_PLOTS, figsize=(15,15))
    fig.suptitle(f'Rate of increase in COVID-19 number of confirmed new cases in the last {DAYS} days', fontsize=20)

    x = 0
    y = 0
    for location in COUNTRIES:
        if (y == Y_PLOTS):
            x += 1
            y = 0
        if (x == X_PLOTS):
            break
        _buff = container.get(location)
        axs[x, y].plot(days, [*_buff.values()], label=location)
        axs[x, y].set_title(location)
        y += 1

    if (len(COUNTRIES) % 2 == 1):
        axs[X_PLOTS - 1, Y_PLOTS - 1].remove()

    for ax in axs.flat:
        ax.set(xlabel='Days', ylabel='Rate')

    fig.savefig('rates.png')



if __name__=="__main__":
    main()
