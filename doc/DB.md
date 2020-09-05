# 다운 받은 자료를 다듬어서 DB에 넣기

지금까지 만든 자료를 다루기 쉽게 잘 다음 DB에 올려봅시다. 여기서는 sqlite3을 이용하여 DB를 만들어보겠습니다. 우선적으로 필요한 것들을 임포트하고 자료를 가지 옵니다.

```python
import pandas as pd
import sqlite3

pitcher = pd.read_csv("./sample/Hanhwa_pitcher_data_2018.csv", index_col=False)
pitcher["경기날짜"] = pd.to_datetime(pitcher['경기날짜'], format='%Y-%m-%d')
# 아래 명령어를 쓰시면 컬럼이 변경된 것을 확인할 수 있습니다.
# hanhwa_pitcher.dtypes
batter = pd.read_csv("./sample/Hanhwa_batter_data_2018.csv",index_col=False)
batter["경기날짜"] = pd.to_datetime(batter['경기날짜'], format='%Y-%m-%d')
```

만약 아래와 같이 쓸모없는 컬럼(예: 'Unnamed: 0')이 있으면 `pitcher.pop()`을 사용하여 제거합니다. 만약 없으면 안 해도 됩니다.

```python
>>> pitcher.columns
Index(['Unnamed: 0', '경기날짜', '선수명', '포지션', '팀', '더블헤더여부', '홈팀', '원정팀', '등판',
       'inning', 'restinning', '승리', '패배', '무승부', '세이브', '홀드', '삼진', '4사구',
       '실점', '자책', '투구수', '피안타', '피홈런', '타수', '타자'],
      dtype='object')

pitcher.pop('Unnamed: 0')
batter.pop('Unnamed: 0')
```

현재 1회가 '1'이라는 컬럼명으로 되어 있는데 이를 모두 수정하겠습니다.

```python
batter = batter.astype({'1': int, '2':int, '3':int, '4':int, '5':int, '6':int, '7':int, '8':int, '9':int, '10':int, '11':int, '12':int})

batter.rename(columns = {'1':'i_1', '2':'i_2', '3':'i_3', '4':'i_4', '5':'i_5', '6':'i_6', '7':'i_7', '8':'i_8', '9':'i_9', '10':'i_10', '11':'i_11', '12':'i_12'}, inplace=True)

batter.rename(columns = {'더블헤더여부':'더블헤더'}, inplace=True)
pitcher.rename(columns = {'inning':'이닝'}, inplace=True)
pitcher.rename(columns = {'restinning':'잔여이닝'}, inplace=True)
pitcher.rename(columns = {'더블헤더여부':'더블헤더'}, inplace=True)
pitcher.rename(columns = {'승리':'승'}, inplace=True)
pitcher.rename(columns = {'패배':'패'}, inplace=True)
pitcher.rename(columns = {'4사구':'사사구'}, inplace=True)
```

```python
batter.loc[:, 'year'] = batter['경기날짜'].dt.year
pitcher.loc[:, 'year'] = pitcher['경기날짜'].dt.year

batter.loc[:, 'month'] = batter['경기날짜'].dt.month
pitcher.loc[:, 'month'] = pitcher['경기날짜'].dt.month

batter.loc[:, 'day'] = batter['경기날짜'].dt.day
pitcher.loc[:, 'day'] = pitcher['경기날짜'].dt.day

batter.loc[:, 'week'] = batter['경기날짜'].dt.dayofweek
pitcher.loc[:, 'week'] = pitcher['경기날짜'].dt.dayofweek

pitcher.pop('경기날짜')
batter.pop('경기날짜')
```

```python
temp_file_name = "./sample/Hanhwa_normalseason_2018.json"
with open(temp_file_name) as outfile:  
    hanhwa_data=json.load(outfile)

scoreboard = pd.DataFrame()

for i in hanhwa_data.keys():
    scoreboard = scoreboard.append(pd.DataFrame(hanhwa_data[i]['scoreboard']),sort=True)
```

지금까지 정리한 파일을 sqlite3에 넣어보겠습니다.

```python
conn = sqlite3.connect('test.db')
pitcher.to_sql('pitcher', conn, index=False)
batter.to_sql('batter', conn, index=False)
conn.close()
```

앞에서는 지금까지 만든 파일을 저장해봤습니다. 저장한 데이터가 잘 들어 갔는지 확인해 봅시다.

```python
import sqlite3

conn = sqlite3.connect('test.db')
cur = conn.cursor()
cur.execute("select * from pitcher")
rows = cur.fetchall()

for row in rows[0:10]:
    print(row)

cur.close()

cur = conn.cursor()
cur.execute("select * from batter")
rows = cur.fetchall()

for row in rows[0:10]:
    print(row)

cur.close()

conn.close()
```

앞에서 만든 DB를 저장해봅시다.

```python
def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')

bck = sqlite3.connect('backup_1.db')

with bck:
    conn.backup(bck, pages=1, progress=progress)

bck.close()
```

## 파케이(Parquet) 포맷으로 저장하기

```python
pip3 install pyarrow

batter.to_parquet('./sample/Hanhwa_batter_data_2018.parquet')
pitcher.to_parquet('./sample/Hanhwa_pitcher_data_2018.parquet')

```

참고로 읽는 방법은 다음과 같다.

```python
batter = pd.read_parquet('./sample/Hanhwa_batter_data_2018.parquet')
pitcher = pd.read_parquet('./sample/Hanhwa_pitcher_data_2018.parquet')
```

조금 더 압축률을 높이고 싶으면 다음과 같은 형식으로 하면 된다.

```python
df.to_parquet('sample.parquet', compression='gzip')
```

## hdf5 포멧으로 저장하고 읽기

```python
pip3 install tables

import tables as tb
import datetime as dt
import pandas as pd
import json
import time
import datetime

h5File = "test.h5"

temp_file_name = "./sample/Hanhwa_normalseason_2018.json"
with open(temp_file_name) as outfile:  
    hanhwa_data=json.load(outfile)

import games

Hanhwa_scoreboard = games.making_scoreboard(hanhwa_data)

h5File = "test.h5"

# 파일에 쓰기
Hanhwa_scoreboard.to_hdf(h5File, "/Hanhwa_scoreboard");

# 앞에서 저장한 파일 읽기
temp_Hanhwa_scoreboard = pd.read_hdf('test.h5', 'Hanhwa_scoreboard')
```

## temp

아래는 테스트 코드 입니다.

```python
with open('./sample/Hanhwa_pitcher_data_2018.csv', 'rt') as fin:
    cin = csv.DictReader(fin)
    villains = [row for row in cin]
```
