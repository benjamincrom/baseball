
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



```python
fig, ax = plt.subplots(figsize=(15,7))
data.groupby(['Pitcher', 'Pitch Type']).size().unstack().plot.bar(ax=ax)
```




![png](baseball_stats_files/baseball_stats_23_1.png)



```python
x = []
for batter in df3['Batter'].unique():
    s = df3[df3['Batter'] == batter]['On-base?']
    if True in s.value_counts():
        t = s.value_counts()[True]
    else:
        t = 0

    if False in s.value_counts():
        f = s.value_counts()[False]
    else:
        f = 0        

    if f != 0 or t != 0:
        success = t / (f + t)
    else:
        success = None

    if f or f == 0:
        x.append((str(batter), success, t, f))

df5 = pd.DataFrame(data=x, columns=['Batter',
                                    'Success',
                                    'Got on base',
                                    'Did not get on base'])

fig, ax = plt.subplots(figsize=(15,15))
plt.ylim(0, 70)
plt.xlim(0, 70)

lims = [0, 70]
ax.plot(lims, lims, 'k-', alpha=1.0, zorder=0, color="blue", label="OBP .500")
lims_600 = [0, 105]
ax.plot(lims, lims_600, 'k-', alpha=1.0, zorder=0, color="indigo", label="OBP .600")
lims_400 = [0, 46.667]
ax.plot(lims, lims_400, 'k-', alpha=1.0, zorder=0, color="green", label="OBP .400")
lims_300 = [0, 30]
ax.plot(lims, lims_300, 'k-', alpha=1.0, zorder=0, color="orange", label="OBP .300")
lims_200 = [0, 17.5]
ax.plot(lims, lims_200, 'k-', alpha=1.0, zorder=0, color="red", label="OBP .200")

horiz = [1, 1]
ax.plot(lims, horiz, '--', alpha=1.0, zorder=0, color="black", label="25%")
horiz = [3, 3]
ax.plot(lims, horiz, '--', alpha=1.0, zorder=0, color="black", label="50%")
horiz = [8, 8]
ax.plot(lims, horiz, '--', alpha=1.0, zorder=0, color="black", label="75%")


ax.set_aspect('equal')
ax.set_xlim(lims)
ax.set_ylim(lims)
ax.set(xlabel="Failed to get on base", ylabel="Got on base")

t = df5['Got on base']
f = df5['Did not get on base']
plt.legend()
b = plt.scatter(f, t, c='b')
plt.show()

df5.sort_values('Got on base', ascending=False)
```


![png](baseball_stats_files/baseball_stats_25_0.png)





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Batter</th>
      <th>Success</th>
      <th>Got on base</th>
      <th>Did not get on base</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>18</th>
      <td>21 Christian Yelich</td>
      <td>0.469880</td>
      <td>39</td>
      <td>44</td>
    </tr>
    <tr>
      <th>58</th>
      <td>16 Cesar Hernandez</td>
      <td>0.414634</td>
      <td>34</td>
      <td>48</td>
    </tr>
    <tr>
      <th>19</th>
      <td>27 Giancarlo Stanton</td>
      <td>0.361446</td>
      <td>30</td>
      <td>53</td>
    </tr>
    <tr>
      <th>49</th>
      <td>11 Ryan Zimmerman</td>
      <td>0.388889</td>
      <td>28</td>
      <td>44</td>
    </tr>
    <tr>
      <th>286</th>
      <td>13 Asdrubal Cabrera</td>
      <td>0.355263</td>
      <td>27</td>
      <td>49</td>
    </tr>
    <tr>
      <th>16</th>
      <td>9 Dee Gordon</td>
      <td>0.350649</td>
      <td>27</td>
      <td>50</td>
    </tr>
    <tr>
      <th>46</th>
      <td>6 Anthony Rendon</td>
      <td>0.382353</td>
      <td>26</td>
      <td>42</td>
    </tr>
    <tr>
      <th>63</th>
      <td>37 Odubel Herrera</td>
      <td>0.406250</td>
      <td>26</td>
      <td>38</td>
    </tr>
    <tr>
      <th>47</th>
      <td>34 Bryce Harper</td>
      <td>0.431034</td>
      <td>25</td>
      <td>33</td>
    </tr>
    <tr>
      <th>21</th>
      <td>13 Marcell Ozuna</td>
      <td>0.320000</td>
      <td>24</td>
      <td>51</td>
    </tr>
    <tr>
      <th>287</th>
      <td>19 Jay Bruce</td>
      <td>0.461538</td>
      <td>24</td>
      <td>28</td>
    </tr>
    <tr>
      <th>48</th>
      <td>20 Daniel Murphy</td>
      <td>0.359375</td>
      <td>23</td>
      <td>41</td>
    </tr>
    <tr>
      <th>294</th>
      <td>7 Jose Reyes</td>
      <td>0.297297</td>
      <td>22</td>
      <td>52</td>
    </tr>
    <tr>
      <th>17</th>
      <td>11 J.T. Realmuto</td>
      <td>0.314286</td>
      <td>22</td>
      <td>48</td>
    </tr>
    <tr>
      <th>59</th>
      <td>13 Freddy Galvis</td>
      <td>0.291667</td>
      <td>21</td>
      <td>51</td>
    </tr>
    <tr>
      <th>60</th>
      <td>23 Aaron Altherr</td>
      <td>0.381818</td>
      <td>21</td>
      <td>34</td>
    </tr>
    <tr>
      <th>300</th>
      <td>20 Neil Walker</td>
      <td>0.456522</td>
      <td>21</td>
      <td>25</td>
    </tr>
    <tr>
      <th>20</th>
      <td>41 Justin Bour</td>
      <td>0.396226</td>
      <td>21</td>
      <td>32</td>
    </tr>
    <tr>
      <th>64</th>
      <td>7 Maikel Franco</td>
      <td>0.263158</td>
      <td>20</td>
      <td>56</td>
    </tr>
    <tr>
      <th>303</th>
      <td>7 Trea Turner</td>
      <td>0.351852</td>
      <td>19</td>
      <td>35</td>
    </tr>
    <tr>
      <th>22</th>
      <td>32 Derek Dietrich</td>
      <td>0.395833</td>
      <td>19</td>
      <td>29</td>
    </tr>
    <tr>
      <th>285</th>
      <td>30 Michael Conforto</td>
      <td>0.391304</td>
      <td>18</td>
      <td>28</td>
    </tr>
    <tr>
      <th>150</th>
      <td>44 Paul Goldschmidt</td>
      <td>0.586207</td>
      <td>17</td>
      <td>12</td>
    </tr>
    <tr>
      <th>52</th>
      <td>1 Wilmer Difo</td>
      <td>0.377778</td>
      <td>17</td>
      <td>28</td>
    </tr>
    <tr>
      <th>62</th>
      <td>19 Tommy Joseph</td>
      <td>0.288136</td>
      <td>17</td>
      <td>42</td>
    </tr>
    <tr>
      <th>10</th>
      <td>26 Adam Frazier</td>
      <td>0.531250</td>
      <td>17</td>
      <td>15</td>
    </tr>
    <tr>
      <th>51</th>
      <td>32 Matt Wieters</td>
      <td>0.262295</td>
      <td>16</td>
      <td>45</td>
    </tr>
    <tr>
      <th>54</th>
      <td>3 Michael Taylor</td>
      <td>0.313725</td>
      <td>16</td>
      <td>35</td>
    </tr>
    <tr>
      <th>7</th>
      <td>10 Jordy Mercer</td>
      <td>0.516129</td>
      <td>16</td>
      <td>15</td>
    </tr>
    <tr>
      <th>96</th>
      <td>28 Tommy Pham</td>
      <td>0.517241</td>
      <td>15</td>
      <td>14</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>318</th>
      <td>41 John Lackey</td>
      <td>0.000000</td>
      <td>0</td>
      <td>4</td>
    </tr>
    <tr>
      <th>250</th>
      <td>55 Robert Stephenson</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>255</th>
      <td>32 Stuart Turner</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>272</th>
      <td>7 Raimel Tapia</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>341</th>
      <td>64 Chris Flexen</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>306</th>
      <td>52 Zack Godley</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>169</th>
      <td>1 Steve Lombardozzi</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>147</th>
      <td>33 Matt Grace</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>305</th>
      <td>38 Jacob Turner</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>163</th>
      <td>31 Lance Lynn</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>362</th>
      <td>38 Michael Morse</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>361</th>
      <td>22 Christian Arroyo</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>166</th>
      <td>8 Mike Leake</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>359</th>
      <td>57 Trevor Williams</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>284</th>
      <td>49 Ben Lively</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>357</th>
      <td>69 Danny Ortiz</td>
      <td>0.000000</td>
      <td>0</td>
      <td>6</td>
    </tr>
    <tr>
      <th>168</th>
      <td>52 Michael Wacha</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>354</th>
      <td>52 Ryan Tepera</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>200</th>
      <td>29 Jeff Samardzija</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>170</th>
      <td>36 Edinson Volquez</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>171</th>
      <td>20 Justin Nicolino</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>351</th>
      <td>56 Ty Kelly</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>178</th>
      <td>17 Ryan Goins</td>
      <td>0.000000</td>
      <td>0</td>
      <td>18</td>
    </tr>
    <tr>
      <th>183</th>
      <td>31 Joe Biagini</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>186</th>
      <td>31 Jeff Locke</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>195</th>
      <td>47 Johnny Cueto</td>
      <td>0.000000</td>
      <td>0</td>
      <td>4</td>
    </tr>
    <tr>
      <th>346</th>
      <td>76 Dillon Peters</td>
      <td>0.000000</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>345</th>
      <td>50 Rafael Montero</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>198</th>
      <td>45 Matt Moore</td>
      <td>0.000000</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>421</th>
      <td>31 Jared Hoying</td>
      <td>0.000000</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>422 rows × 4 columns</p>
</div>


