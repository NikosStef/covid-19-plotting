import pandas as pd
import numpy as np
import datetime
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

def sigmoid(x, x0, L, k):
    return L / (1 + np.exp(-k*(x-x0)))

def sigmoid_growth(rate):
    return lambda x, x0, L: sigmoid(x, x0, L, rate)

def pull_data():

    url='https://covid.ourworldindata.org/data/ecdc/full_data.csv'
    df = pd.read_csv(url, parse_dates=['date'])

    df.fillna(0, inplace=True)
    df = df.loc[df['location'] == 'United Kingdom']
    df.reset_index(drop=True, inplace=True)

    return df

def main():

    data = pull_data()

    data['date'].astype(str).str.replace("-","").astype(int)
    x0 = data['date'].dt.strftime("%d%m").astype(int)
    y0 = data['total_deaths']
    y1 = data['total_cases']

    popt0, pcov0 = curve_fit(sigmoid, x0, y0)
    popt1, pcov1 = curve_fit(sigmoid, x0, y1)

    """
    $$$ ISSUE WITH DATE FORMATING AND PARSING $$$
    """
    x = range(x0.iloc[-1], (x0.iloc[-1] + 50))
    y0_pred = sigmoid(x, *popt0)
    y1_pred = sigmoid(x, *popt1)
    x = np.concatenate((pd.date_range(data['date'].iloc[0], data['date'].iloc[-1]), pd.date_range(data['date'].iloc[-1], periods=50)))

    dates = []
    format = "%d/%m"
    for _value in x:
        dates.append(pd.to_datetime(str(_value)).strftime(format))

    _series = pd.Series(y0_pred)
    y0_data = pd.concat([y0, _series], ignore_index=True)

    _series = pd.Series(y1_pred)
    y1_data = pd.concat([y1, _series], ignore_index=True)

    fig, ax = plt.subplots()
    ax.plot(dates, y0_data, label='Deaths')
    ax.plot(dates, y1_data, label='Cases')
    ax.set_xlabel('Date')
    ax.set_ylabel('People')
    ax.set_title('Prediction on COVID-19 cases using Sigmoid')
    fig.savefig('prediction.png')
    fig.show()


if __name__=="__main__":
    main()
