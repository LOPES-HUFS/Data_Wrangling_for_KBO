# 선수 자료

KBO에는 같은 이름을 가진 선수도 많고, 이름을 개명하는 선수도 많습니다. 이를 처리하기 위해서는 선수 ID를 만들어야 합니다. KBO에서 공식적으로 공개하고 있지 않지만, 홈페이지에서 사용하고 있는 ID가 존재하고 있습니다. 이를 모아보겠습니다.

이 기능을 하는 함수는 `players.py`에 들어 있습니다. 사용방법은 다음과 같습니다.

```python
>>> import players
>>> players.searching("강경학")
[{'61700': {'ID': '61700', '이름': '강경학', '현재 상태': 'KBO', 'team': '한화'}}]
```

많은 선수의 자료를 한꺼번에 모으려면 다음과 같이 하시면 됩니다.

```python
temp_players = ['가득염', '가르시아', '가코', '강경학', '강구성', '강귀태', '강동관', '강동수', '강동연', '강동우']
temp = players.searching_players(temp_players)
```

그러나 이 스크립트를 사용하시는 분들은 이 작업을 해서 선수 명단은 직접 작성하실 필요는 없습니다. 우리 팀에서 이미 모아둔 자료를 사용하시면 됩니다. 다음과 같이 가져오시면 됩니다.

## 타자 포지션 표기 변경하기

KBO 선수들은 하나의 포지션을 가질 때도 있지만 경기가 진행됨에 따라 다른 포지션으로 변경되는 경우도 종종 있습니다. 현재 타자 선수들의 포지션의 고유 값은 96가지입니다. 96가지나 되는 이유는 투수와 지명타자를 포함하여 총 10가지의 단일한 포지션에서 파생된 경우의 수입니다. 게다가 한자와 한글이 병기된 표기를 하고 있기에 쉽게 알아보기 힘듭니다. 이에 따라 표기 방식 통일을 위해 숫자와 영문을 이용한 표기로 변경해 줍니다. 임의의 숫자와 영문 표기로 바꾸는 것이 아닌 야구 경기의 기록 규칙에 따라 숫자와 영문을 적용해줍니다. 선수들의 포지션에 숫자는 [KBO 기록위원회](https://www.koreabaseball.com/About/Committee/RecordRaw.aspx)의 수비 위치 기호에 따라 정했으며, 대타의 경우 타자를 의미하는 H 대주자의 경우 주자를 의미하는 R로 지정했습니다. 이제 직접 선수들의 포지션을 변경해 봅시다.

필요한 라이브러리를 import 하고 타자 데이터를 읽어 옵니다.

```python
import pandas as pd

batter_data = pd.read_csv("./KBO_batter_data_full.csv")
```

고유 포지션 수를 확인해 봅니다. 

```python
len(batter_data["포지션"].unique())

```

포지션 표기를 변경할 수 있는 함수를 만들어 줍니다.

```python

def change_posision(data):
    '''
    data = pandas DF
    '''
    if '一' in data:
        data = data.replace("一","3")
    elif '二' in data: 
        data = data.replace("二","4")
    elif '三' in data:
        data = data.replace("三","5")
    elif "투" in data:
        data = data.replace("투","1")
    elif "포" in data:
        data = data.replace("포","2")
    elif "유" in data:
        data = data.replace("유","6")
    elif "좌" in data:
        data = data.replace("좌","7")
    elif "중" in data:
        data = data.replace("중","8")
    elif "우" in data:
        data = data.replace("우","9")
    elif "지" in data:
        data = data.replace("지","D")
    elif "주" in data:
        data = data.replace("주","R")
    elif "타" in data:
        data = data.replace("타","H")
    return data

```

데이터에 만든 함수를 적용해 줍니다. 이 함수를 두번 적용해야하는데 포지션이 변경된 경우가 있기 때문에 한번만에 완전히 바뀌지 않기 때문입니다.

```python
new_position_temp = [change_posision(i) for i in batter_data["포지션"]]
new_position = [change_posision(i) for i in new_position_temp]
```

이제 새로운 포지션 데이터를 데이터에 붙여줍니다. `copy()` 를 쓰는 이유는 원본 데이터를 보존하기 위해서 입니다.  

```python
batter_temp = batter_data.copy()
batter_temp["포지션"] = new_position
```

## temp_code

```python
import csv
import players

temp_file_name='all_player_list.csv'

with open (temp_file_name, 'rt') as fin:
        cin = csv.DictReader(fin)
        temp_player_list = [row for row in cin]

temp_player_list[0]

temp_players =[]

for item in temp_player_list:
    temp_players.append(item['name'])

temp_players  =sorted(list(set(temp_players)))
temp_players[0:10]

players.searching_players(temp_players[0:9])
```
