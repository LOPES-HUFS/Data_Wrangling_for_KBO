# 게임 데이터 추가 하기

경기는 계속 열리기 때문에 자료를 계속해서 갱식, 즉 추가할 필요가 있습니다. 여기서는 추가하는 방법을 소개하도록 하겠습니다. 우선 [게임 정보 가져오기](https://github.com/LOPES-HUFS/Data_Wrangling_for_KBO/blob/master/doc/game_info.md)를 보시고, 기존 자료에 추가할 다음 게임 자료를 다 모았다고 가정하겠습니다. 이 자료는 `data/temp_data.json`이라는 파일에 들어있게 됩니다.

```python
import game_info
data_8 = game_info.get_data(2020, 8, "정규")
game_id_8 = game_info.modify_data(2020, data_8)
data = games.get_data(game_id_8)
```

## 연 자료에 월 자료 추가

앞에서 만든 월 자료를 가지고 연 자료에 추가해 보겠습니다. 현재 2020년 자료가 9월 자료까지 있다고 가정하겠습니다. 여기에 10월 자료를 추가해보겠습니다. 기본적인 방법은 우선 2020년 9월까지 자료가 들어 있는 파일과 10월 자료가 들어있는 파일을 열고, 10월 자료를 가지고 2020년 자료를 갱신한 다음 저장하면 됩니다. 여기서는 2020년 자료를 `temp_data_2020.json`에 저장하도록 하겠습니다. 갱신할 파일은 `temp_data_2020.json`, `temp_schedule_2020`, 총 2개입니다.

```python
file_name = "data/temp_data_2020.json"

with open(file_name) as json_file:
    temp_data_2020 = json.load(json_file)

file_name = "data/temp_data_2020_10.json"

with open(file_name) as json_file:
    temp_data_2020_10 = json.load(json_file)

temp_data_2020.update(temp_data_2020_10)

file_name = 'data/temp_data_2020.json'
with open(file_name, 'w') as outfile:
    json.dump(temp_data_2020, outfile)

kbo_id_temp_2020=pd.read_csv("./data/temp_schedule_2020.csv")

kbo_id_temp_9=pd.read_csv("./data/temp_schedule_2020_10.csv")

frames = [kbo_id_temp_2020, kbo_id_temp_9]

kbo_id_full = pd.concat(frames)
kbo_id_full = kbo_id_full.reset_index(drop=True)

kbo_id_full.to_csv("data/temp_schedule_2020.csv", index = False)
```

## 스코어 자료 추가하기

`.drop_duplicates()`은 중복된 것을 제거하는 옵션입니다. 아래에서처럼 `scoreboard.drop_duplicates()`이라고 하더라도 원래 값을 바꾸지는 않기 때문에 아래와 같이 제거한 것으로 덮어쓰기를 해야한다.

## temp_code

```python
import game_info
data_8 = game_info.get_data(2020, 8, "정규")
game_id_8 = game_info.modify_data(2020, data_8)
data = games.get_data(game_id_8)
scoreboard_8 = games.making_scoreboard(data)
scoreboard = pd.read_parquet('./sample/scoreboard.parquet')
scoreboard = pd.concat([scoreboard, scoreboard_8])
scoreboard = scoreboard.drop_duplicates()
scoreboard = scoreboard.reset_index(drop=True)
```
