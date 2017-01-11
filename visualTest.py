import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

start = pd.to_datetime("5-1-2012")
idx = pd.date_range(start, periods= 365)
df = pd.DataFrame({'A':np.random.random(365), 'B':np.random.random(365)})
df.index = idx
df_ts = df.resample('W', how= 'max')

ax = df_ts.plot(kind='bar', x=df_ts.index, stacked=True)

# Make most of the ticklabels empty so the labels don't get too crowded
ticklabels = ['']*len(df_ts.index)
# Every 4th ticklable shows the month and day
ticklabels[::4] = [item.strftime('%b %d') for item in df_ts.index[::4]]
# Every 12th ticklabel includes the year
ticklabels[::12] = [item.strftime('%b %d\n%Y') for item in df_ts.index[::12]]
ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
plt.gcf().autofmt_xdate()

plt.show()