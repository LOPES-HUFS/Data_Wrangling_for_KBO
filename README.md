# Data Wrangling for KBO

이 스크립트는 KBO 자료를 수집, 정리하고 분석하고자 만들었습니다. 자료를 수집하는 링크는 다음과 같습니다.

[https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx](https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx)

## 요구 사항

이 스크립트는 다음 것들이 컴퓨터에 설치되어 있어야 제대로 작동합니다. 설치 방법은 위키를 참고하세요. 아래 본 프로젝트의 [위키](https://github.com/LOPES-HUFS/KBO_Data_Wrangling/wiki/요구-사항-설치-방법)를 참고하세요!

**필요한 것들**: 크롬(Chrome) 브라우져, Python 3.6 이상, 크롬드라이버, selenium, 파이선 패키지(requests, selenium, bs4, configparser, pandas, lxml)

## 사용법

우선 이 프로젝트를 다운 받습니다. 이 프로젝트의 [메인 페이지](https://github.com/LOPES-HUFS/KBO_Data_Wrangling) 오른쪽 상단에 'Code' 버튼을 클릭 후 'Download ZIP' 버튼을 눌러 다운받으시면 됩니다. 만약, [git](https://git-scm.com/downloads)을 설치하셨으면, git을 클론하시면 됩니다.

프로젝트를 다 받으셨으면, `터미널`이나 `윈도우 cmd`에서 프로젝트를 받은 곳으로 이동합니다. 다음과 같은 파일이 있으면 잘 이동한 것입니다.

```bash
single_game.py
modifying_data.py
pasing_page.py
```

이 곳에서 파이선을 실행 합니다.

### 경기 자료를 다운 받는 방법

본격적을 경기 자료를 다운받아보겠습니다. 이제부터는 파이썬에서 실행하시면 됩니다. 필요한 것들을 `import`합니다.

```python
import single_game
import modifying_data
import pandas as pd
import json
```

2020년 8월 1일, 한화 대 엘지 경기 자료를 다운받아 보겠습니다. 여기서 "20200801"은 경기 날짜, "HHLG0"은 한화, 엘지 1번째 경기를 뜻합니다. 파이썬에서 0부터 숫자를 시작해서 0이 첫번째 경기입니다.

```python
HHLG_20200801 = single_game.get_data("20200801","HHLG0")
```

다운받은 경기 자료에 어떤 항목들이 있는지 살펴봅시다. 순서대로 확인하면 다음과 같습니다.

```python
>>> list(HHLG_20200801['20200801_HHLG0'].keys())
['scoreboard', 'ETC_info', 'away_batter', 'home_batter', 'away_pitcher', 'home_pitcher']
```

그러면 다운받은 항목들을 하나 하나 살펴 봅시다.

```python
>>> pd.DataFrame(HHLG_20200801['20200801_HHLG0']['scoreboard'])
    팀 승패  1  2  3  4  5  6  7  8  9 10 11 12  R   H  E  B
0  한화  패  0  0  0  0  5  0  0  0  1  -  -  -  6   8  2  6
1  LG  승  6  0  0  1  0  0  0  2  -  -  -  -  9  15  0  2
>>> HHLG_20200801['20200801_HHLG0']['ETC_info']
{'결승타': '김현수(1회 2사 2루서 중전 안타)', '홈런': '노시환5호(5회3점 김윤식)', '2루타': ['김민성(1회', '홍창기(4회', '노수광(6회', '김현수(8회', '반즈(9회)'], '실책': ['노시환(1회', '하주석(3회)'], '도루': '노수광(9회)', '주루사': ['정주현(1회', '유장혁(3회', '홍창기(6회)'], '포일': '이해창(8회)', '폭투': ['서폴드2(1 2회', '김윤식(5회', '고우석(9회)'], '심판': ['정종수', '이계성', '박기택', '오훈규'], '구장': '잠실', '관중': '2,315', '개시': '18:00', '종료': '21:17', '경기시간': '3:17'}
>>> pd.DataFrame(HHLG_20200801['20200801_HHLG0']['away_batter']).head()
  포지션  선수명   1   2   3   4   5   6   7  8   9  타수  안타  타점  득점     타율   팀
0   중  이용규  4구   0  유직   0  중안  1파   0  0  우비   4   1   0   1  0.274  한화
1   二  정은원  1땅   0   0  1땅  4구  삼진   0  0  삼진   4   0   0   1  0.250  한화
2   우   반즈  우비   0   0  중안  4구   0  삼진  0  좌2   4   2   1   0  0.268  한화
3   一  김태균  중비   0   0  우비  좌안   0  3땅  0  중비   5   1   1   0  0.234  한화
4   지  최진행   0  3땅   0  우비  4구   0  2땅  0   0   3   0   1   0  0.237  한화
>>> pd.DataFrame(HHLG_20200801['20200801_HHLG0']['home_batter']).head()
  포지션  선수명         1   2  3   4  5    6   7    8  9  타수  안타  타점  득점     타율   팀
0   중  홍창기  좌중안\/ 우안   0  0  중2  0   좌안   0   2땅  0   5   4   1   2  0.259  LG
1   유  오지환        삼진  좌비  0  1직  0  우중안   0   4구  0   4   1   0   1  0.288  LG
2   우  채은성        유땅  좌안  0  좌안  0   삼진   0  우중안  0   5   3   2   1  0.279  LG
3   좌  김현수        중안  3파  0  우안  0   2땅   0   좌2  0   5   3   2   1  0.346  LG
4   지  김민성        좌2  삼진  0  삼진  0    0  사구    0  0   3   1   1   1  0.309  LG
>>> pd.DataFrame(HHLG_20200801['20200801_HHLG0']['away_pitcher'])
   선수명   등판 결과  승  패  세      이닝  타자  투구수  타수  피안타  홈런  4사구  삼진  실점  자책  평균자책점   팀
0  서폴드   선발  패  5  9  0  3 1\/3  21   74  21   10   0    0   2   7   5   4.96  한화
1  김진욱  4.4  0  1  1  0  1 2\/3   6   26   6    1   0    0   2   0   0   3.95  한화
2  안영명  6.1  0  1  1  0       1   4   12   4    2   0    0   1   0   0   6.48  한화
3  윤대경  7.5  0  0  0  0       1   4   16   3    0   0    1   2   0   0   2.33  한화
4  강재민  8.9  0  0  0  0    2\/3   5   27   4    2   0    1   0   2   2   3.24  한화
5  김종수  8.5  0  0  0  0    1\/3   1    6   1    0   0    0   0   0   0   5.09  한화
>>> pd.DataFrame(HHLG_20200801['20200801_HHLG0']['home_pitcher'])
   선수명   등판  결과  승  패  세      이닝  타자  투구수  타수  피안타  홈런  4사구  삼진  실점  자책  평균자책점   팀
0  김윤식   선발   0  0  1  0  4 1\/3  22   90  17    5   1    5   1   5   5   7.52  LG
1  이정용  5.5   승  1  0  0  1 2\/3   7   31   6    1   0    1   3   0   0   2.70  LG
2  정우영  7.3  홀드  2  1  5       2   6   22   6    0   0    0   3   0   0   2.90  LG
3  고우석  9.9   0  0  0  2       1   5   24   5    2   0    0   1   1   1  10.29  LG
```

지금까지 `single_game.get_data()`을 이용하여 다운받은 자료를 살펴본 코드를 정리하면 다음과 같습니다.

```python
# 경기 자료 다운
HHLG_20200801 = single_game.get_data("20200801","HHLG0")
# 어떤 테이블이 있는지 key 값을 통해 확인합니다.
list(HHLG_20200801['20200801_HHLG0'].keys())
# 도루를 비롯한 구장, 관중 수 등의 정보를 확인합니다.
HHLG_20200801['20200801_HHLG0']['ETC_info']
#경기의 점수 상황 판을 판다스를 이용해서 테이블로 확인합니다.
pd.DataFrame(HHLG_20200801['20200801_HHLG0']['scoreboard'])
# 원정팀 타자 정보를 테이블로 확인합니다.
pd.DataFrame(HHLG_20200801['20200801_HHLG0']['away_batter'])
# 홈팀 타자 정보를 테이블로 확인합니다.
pd.DataFrame(HHLG_20200801['20200801_HHLG0']['home_batter'])
# 원정팀 투수 정보를 테이블로 확인합니다.
pd.DataFrame(HHLG_20200801['20200801_HHLG0']['away_pitcher'])
# 원정팀 투수 정보를 테이블로 확인합니다.
pd.DataFrame(HHLG_20200801['20200801_HHLG0']['home_pitcher'])
```

### 2018 시즌 한화의 전체 경기 자료 데이터를 다운 받기

앞에서 살펴본 `single_game.get_data()`은 한 경기만을 다운받는 함수입니다. 그러면 이 함수를 이용해서 2018 시즌 한화의 전체 경기 자료 데이터를 다운받아 보겠습니다. 저희 팀에서 이미 이 데이터를 자료를 받기 위한 리스트를 `Hanhwa_game_id_sample.csv`에 정리해두었습니다. 이 파일을 가지고 2018 시즌 한화의 전체 경기 자료 데이터를 받아보겠습니다. 다음 코드로 다운받을 리스트를 가져오겠습니다. 리스트의 길이가 144이니 전체 경기수는 144경기가 되겠습니다. 2018 시즌 한 팀 당 경기 수가 144경기였습니다. 이 숫자는 시즌마다 변경되기도 합니다.

```python
>>> import pandas as pd
>>> sample = pd.read_csv("./data/Hanhwa_game_id_sample.csv")
>>> sample.date = sample.date.astype(str)
>>> sample.date
0      20180324
1      20180325
2      20180327
3      20180328
4      20180329
         ...
139    20181004
140    20181006
141    20181009
142    20181010
143    20181013
Name: date, Length: 144, dtype: object
```

그러면 파이썬을 이용해서 받아보겠습니다. 시간이 생각보다 오래걸립니다.

```python
>>> temp_full ={}
>>> for i in range(0,len(sample)):
...     temp_data = single_game.get_data(sample.date[i],sample.gameid[i])
...     temp_data = single_game.modify_data(temp_data)
...     temp_full.update(temp_data)
...
>>> len(temp_full.keys())
144
```

지금까지 다운받은 1년치 한화 경기를 json 파일로 저장해 줍니다.

```python
temp_file_name = "./sample/Hanhwa_normalseason_2018.json"

with open(temp_file_name, 'w') as outfile:  
    json.dump(temp_full, outfile)
```

지금까지 '2018 시즌 한화의 전체 경기 자료 데이터'를 다운받기 위해 사용한 코드를 정리하면 다음과 같습니다.

```python
sample=pd.read_csv("./data/Hanhwa_game_id_sample.csv")
sample.date=sample.date.astype(str)

temp_full ={}

for i in range(0,len(sample)):
    temp_data = main.get_data(sample.date[i],sample.gameid[i])
    temp_data = main.modify_data(temp_data)
    temp_full.update(temp_data)

temp_file_name = "./sample/Hanhwa_normalseason_2018.json"

with open(temp_file_name, 'w') as outfile:  
    json.dump(temp_full, outfile)
```

이제까지 한 것을 정리하여 한번에 다운받는 함수를 만들었습니다. 그리고 정리하는 함수도 만들었습니다. 이것들을 사용해 봅시다. 한화 경기 전체를 다운받는 것으로 연습하는 것은 무리가 있어서 2 경이만 다운 받는 것으로 바꿨습니다.

```python
import pandas as pd

sample = pd.read_csv("./data/Hanhwa_game_id_sample.csv")
sample.date = sample.date.astype(str)

import games

temp = games.get_data(sample[0:2])
scoreboard = games.making_scoreboard(temp)
batter = games.making_batter(temp)
pitcher = games.making_pitcher(temp)

# 한화 경기 전체를 하려면 아래 코드 2줄을 사용하세요
#temp = games.get_data(sample)
#temp_temp = games.modify(temp, sample, 'scoreboard')
```

### KBO 전체 경기 자료 데이터를 다운 받기

지금까지 배운 것을 토대로 KBO 전체 경기 자료 데이터를 다운받아 보겠습니다. 이 방법은 공식 홈페이지에 있는 자료를 다운받는 것입니다. 그렇기 때문에 수집한 자료이기 때문에 공식자료와는 다를 수 있습니다.

```python
kbo_id_full=pd.read_csv("./data/KBO_gameid_full.csv")
kbo_id_full.date=kbo_id_full.date.astype(str)

full_data={}
for i in range(0,len(kbo_id_full)):
    temp_data = main.get_data(kbo_id_full.date[i],kbo_id_full.gameid[i])
    temp_data = main.modify_data(temp_data)
    full_data.update(temp_data)

temp_file_name = "./data/KBO_normalseason_full.json"

with open(temp_file_name, 'w') as outfile:  
    json.dump(full_data, outfile)
```
