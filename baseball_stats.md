
## Analyze a game: 2017 World Series - Game 7


```python
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import sys
import matplotlib

import baseball

%matplotlib inline

game_id, game = baseball.get_game_from_url('11-1-2017', 'HOU', 'LAD', 1)

pitch_tuple_list = []
for inning in game.inning_list:
    for appearance in inning.top_half_appearance_list:
        for event in appearance.event_list:
            if isinstance(event, baseball.Pitch):
                pitch_tuple_list.append(
                    (str(appearance.pitcher), 
                     event.pitch_description,
                     event.pitch_position,
                     event.pitch_speed,
                     event.pitch_type)
                )

data = pd.DataFrame(data=pitch_tuple_list, columns=['Pitcher', 'Pitch Description', 'Pitch Coordinate', 'Pitch Speed', 'Pitch Type'])
data.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pitcher</th>
      <th>Pitch Description</th>
      <th>Pitch Coordinate</th>
      <th>Pitch Speed</th>
      <th>Pitch Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>21 Yu Darvish</td>
      <td>Ball</td>
      <td>(155.47, 160.83)</td>
      <td>96.0</td>
      <td>FF</td>
    </tr>
    <tr>
      <th>1</th>
      <td>21 Yu Darvish</td>
      <td>Called Strike</td>
      <td>(107.0, 171.09)</td>
      <td>83.9</td>
      <td>FC</td>
    </tr>
    <tr>
      <th>2</th>
      <td>21 Yu Darvish</td>
      <td>In play, no out</td>
      <td>(115.36, 183.1)</td>
      <td>83.9</td>
      <td>SL</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21 Yu Darvish</td>
      <td>In play, run(s)</td>
      <td>(80.06, 168.03)</td>
      <td>96.6</td>
      <td>FF</td>
    </tr>
    <tr>
      <th>4</th>
      <td>21 Yu Darvish</td>
      <td>Ball</td>
      <td>(54.1, 216.52)</td>
      <td>84.6</td>
      <td>SL</td>
    </tr>
  </tbody>
</table>
</div>

```python
data['Pitcher'].value_counts().plot.bar()
```

![png](baseball_stats_files/baseball_stats_3_1.png)

```python
for pitcher in data['Pitcher'].unique():
    plt.ylim(0, 125)
    plt.xlim(0, 250)
    bx = [250 - x[2][0] for x in pitch_tuple_list if x[0] == pitcher if 'Ball' in x[1]]
    by = [250 - x[2][1] for x in pitch_tuple_list if x[0] == pitcher if 'Ball' in x[1]]
    cx = [250 - x[2][0] for x in pitch_tuple_list if x[0] == pitcher if 'Called Strike' in x[1]]
    cy = [250 - x[2][1] for x in pitch_tuple_list if x[0] == pitcher if 'Called Strike' in x[1]]
    ox = [250 - x[2][0] for x in pitch_tuple_list if x[0] == pitcher if ('Ball' not in x[1] and 'Called Strike' not in x[1])]
    oy = [250 - x[2][1] for x in pitch_tuple_list if x[0] == pitcher if ('Ball' not in x[1] and 'Called Strike' not in x[1])]
    b = plt.scatter(bx, by, c='b')
    c = plt.scatter(cx, cy, c='r')
    o = plt.scatter(ox, oy, c='g')

    plt.legend((b, c, o),
               ('Ball', 'Called Strike', 'Other'),
               scatterpoints=1,
               loc='upper right',
               ncol=1,
               fontsize=8)

    plt.title(pitcher)
    plt.show()
```


![png](baseball_stats_files/baseball_stats_4_0.png)



![png](baseball_stats_files/baseball_stats_4_1.png)



![png](baseball_stats_files/baseball_stats_4_2.png)



![png](baseball_stats_files/baseball_stats_4_3.png)



![png](baseball_stats_files/baseball_stats_4_4.png)



```python
plt.axis('equal')
data['Pitch Description'].value_counts().plot(kind='pie', radius=1.5, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
```



![png](baseball_stats_files/baseball_stats_6_1.png)



```python
data.plot.kde()
```




![png](baseball_stats_files/baseball_stats_7_1.png)



```python
fig, ax = plt.subplots()
ax.set_xlim(50, 120)
for pitcher in data['Pitcher'].unique():
    s = data[data['Pitcher'] == pitcher]['Pitch Speed']
    s.plot.kde(ax=ax, label=pitcher)

ax.legend()
```






![png](baseball_stats_files/baseball_stats_8_1.png)



```python
fig, ax = plt.subplots()
ax.set_xlim(50, 120)
for desc in data['Pitch Type'].unique():
    s = data[data['Pitch Type'] == desc]['Pitch Speed']
    s.plot.kde(ax=ax, label=desc)

ax.legend()
```






![png](baseball_stats_files/baseball_stats_9_1.png)



```python
fig, ax = plt.subplots(figsize=(15,7))
data.groupby(['Pitcher', 'Pitch Description']).size().unstack().plot.bar(ax=ax)
```




![png](baseball_stats_files/baseball_stats_10_1.png)



## Analyze a player's season: R.A. Dickey - 2017


```python
game_list_2017 = baseball.get_game_list_from_file_range('1-1-2017', '12-31-2017', '/Users/benjamincrom/repos/livebaseballscorecards-artifacts/baseball_files')

pitch_tuple_list_2 = []
for game_id, game in game_list_2017:
    if game.home_team.name == 'Atlanta Braves' or game.away_team.name == 'Atlanta Braves':
        for inning in game.inning_list:
            for appearance in (inning.top_half_appearance_list +
                               (inning.bottom_half_appearance_list or [])):
                if 'Dickey' in str(appearance.pitcher):
                    for event in appearance.event_list:
                        if isinstance(event, baseball.Pitch):
                            pitch_tuple_list_2.append(
                                (str(appearance.pitcher), 
                                 event.pitch_description,
                                 event.pitch_position,
                                 event.pitch_speed,
                                 event.pitch_type)
                            )

df = pd.DataFrame(data=pitch_tuple_list_2, columns=['Pitcher', 'Pitch Description', 'Pitch Coordinate', 'Pitch Speed', 'Pitch Type'])
df['Pitch Type'].value_counts().plot.bar()
```



![png](baseball_stats_files/baseball_stats_14_1.png)



```python
plt.axis('equal')
df['Pitch Description'].value_counts().plot(kind='pie', radius=2, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
plt.ylabel('')
plt.show()
```


![png](baseball_stats_files/baseball_stats_15_0.png)



```python
df.dropna(inplace=True)
ax.set_xlim(50, 100)
df.plot.kde()
ax.legend()
```





![png](baseball_stats_files/baseball_stats_16_1.png)



```python
fig, ax = plt.subplots()
ax.set_xlim(50, 100)
for desc in df['Pitch Type'].unique():
    if desc != 'PO':
        s = df[df['Pitch Type'] == desc]['Pitch Speed']
        s.plot.kde(ax=ax, label=desc)

ax.legend()
```






![png](baseball_stats_files/baseball_stats_17_1.png)


## Analyze a lineup of pitchers: Atlanta Braves - 2017 Regular Season


```python
import datetime
import dateutil.parser
import pytz
pitch_tuple_list_3 = []
for game_id, game in game_list_2017:
    if game.home_team.name == 'Atlanta Braves' and dateutil.parser.parse(game.game_date_str) > datetime.datetime(2017, 3, 31):
        for inning in game.inning_list:
            for appearance in inning.top_half_appearance_list:
                pitch_tuple_list_3.append(
                    (str(appearance.pitcher),
                     str(appearance.batter),
                     len(appearance.out_runners_list),
                     len(appearance.scoring_runners_list),
                     len(appearance.runners_batted_in_list),
                     appearance.scorecard_summary,
                     appearance.got_on_base,
                     appearance.plate_appearance_summary,
                     appearance.plate_appearance_description,
                     appearance.error_str,
                     appearance.inning_outs)
                )
    if game.away_team.name == 'Atlanta Braves' and dateutil.parser.parse(game.game_date_str) > datetime.datetime(2017, 3, 31):
        for inning in game.inning_list:
            if inning.bottom_half_appearance_list:
                for appearance in inning.bottom_half_appearance_list:
                    pitch_tuple_list_3.append(
                        (str(appearance.pitcher),
                         str(appearance.batter),
                         len(appearance.out_runners_list),
                         len(appearance.scoring_runners_list),
                         len(appearance.runners_batted_in_list),
                         appearance.scorecard_summary,
                         appearance.got_on_base,
                         appearance.plate_appearance_summary,
                         appearance.plate_appearance_description,
                         appearance.error_str,
                         appearance.inning_outs)
                    )

df3 = pd.DataFrame(data=pitch_tuple_list_3, columns=['Pitcher',
                                                     'Batter',
                                                     'Out Runners',
                                                     'Scoring Runners',
                                                     'RBIs',
                                                     'Scorecard',
                                                     'On-base?',
                                                     'Plate Summary',
                                                     'Plate Description',
                                                     'Error',
                                                     'Inning Outs'])

for pitcher in df3['Pitcher'].unique():
    summary = df3[df3['Pitcher'] == pitcher]['Plate Summary']
    s = summary.value_counts(sort=False)
    if len(summary) > 400:
        fig, ax = plt.subplots()
        ax.set_ylim(0, 250)
        s.plot.bar()
        plt.title(pitcher)
        plt.show()

```


![png](baseball_stats_files/baseball_stats_20_0.png)



![png](baseball_stats_files/baseball_stats_20_1.png)



![png](baseball_stats_files/baseball_stats_20_2.png)



![png](baseball_stats_files/baseball_stats_20_3.png)



![png](baseball_stats_files/baseball_stats_20_4.png)



```python
x = []
for pitcher in df3['Pitcher'].unique():
    #f = df3[df3['Pitcher'] == pitcher]['On-base?'].value_counts()[0]
    s = df3[df3['Pitcher'] == pitcher]['On-base?'].value_counts()
    if len(s) == 2:
        f = s[0]
        t = s[1]
        x.append((str(pitcher), f, t))

df4 = pd.DataFrame(data=x, columns=['Pitcher',
                                    'Did not get on base',
                                    'Got on base'])

df4.index = df4['Pitcher']
df4.sort_values(by=['Got on base']).nlargest(10, 'Did not get on base').plot.bar()
```



![png](baseball_stats_files/baseball_stats_22_1.png)

