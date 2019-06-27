import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

watchlist = ["AAPL", "GOOG"]
token = 'insert your IEXApi token here'

df = pd.DataFrame(columns = ['Date'])

# while True: put a while loop here to run this continuously
for stock in watchlist:

    df[stock+'50d'] = ""
    df[stock+'200d'] = ""
    
    url = 'https://cloud.iexapis.com/stable/stock/'+stock+'/chart/5y/tops?token='+token
    apiResult = requests.get(url)
    chart = apiResult.json()

    print("STOCK DATA DOWNLOADING..", stock)

    for i in range(0,730): #730 is the number of days to go back
        count50 = 0
        sum50 = 0
        count200 = 0
        sum200 = 0
        chartlen = len(chart)-1-i
        today = chart[chartlen]['date']

        for day in reversed(chart):
            count50 += 1
            count200 += 1

            if count50 >= 1+i and count50 <= 50+i: #1-50 is the number of days to average over
                sum50 += (day['close'])

            if count50 > 50+i:
                close50 = sum50 / 50
                df.loc[i, 'Date'] = today
                df.loc[i, stock+'50d'] = close50

            if count200 >= 1+i and count200 <= 200+i: #1-200 is the number of days to average over
                sum200 += (day['close'])

            if count200 > 200+i:
                close200 = sum200 / 200
                df.loc[i, stock+'200d'] = close200
                break
            
df.sort_values(by=['Date'], inplace=True, ascending=True)
print(df)

fig, axes = plt.subplots(nrows=len(watchlist), ncols=1, figsize=(15,15))
plt.xticks(np.arange(0,730,48)) #0-730 are the start and end points, 48 is the gap between points

axescount = 0
for stock in watchlist:
    df.plot(kind='line', x='Date', y=stock+'50d', color='blue', ax=axes[axescount])
    df.plot(kind='line', x='Date', y=stock+'200d', color='red', ax=axes[axescount])
    axescount += 1

plt.xticks(fontsize=6, rotation=45)
# plt.show(block=False)
plt.pause(10)
# plt.close()
    # print("NEXT LOOP")