import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dates = pd.date_range(start=dt.date(2014,10,22), periods=10, freq='H')
df = pd.DataFrame({'start': dates, 'duration': np.random.randint(1, 10, len(dates))}, columns=['start', 'duration'])
df['duration'] = df.duration.map(lambda x: pd.datetools.timedelta(0, 0, 0, 0, x))
df.ix[1, 1] = pd.datetools.timedelta(0, 0, 0, 0, 30) # To clearly see the effect at 01:00:00

width=[x.seconds/24.0/60.0 for x in df.duration] # mpl will treat x.minutes as days hense /24/60.

#hours, remainder = divmod(td.seconds, 3600)
#minutes, seconds = divmod(remainder, 60)

height=[1]*df.start.shape[0]

plt.bar(left=df.start, width=width, height=[1]*df.start.shape[0])

ax = plt.gca()
_ = plt.setp(ax.get_xticklabels(), rotation=45)