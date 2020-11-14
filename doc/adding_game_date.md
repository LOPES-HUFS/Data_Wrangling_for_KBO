# 게임 데이터 추가 하기

경기는 계속 열리기 때문에 자료를 계속해서 갱식, 즉 추가할 필요가 있습니다. 여기서는 추가하는 방법을 소개하도록 하겠습니다. 우선 [게임 정보 가져오기](https://github.com/LOPES-HUFS/Data_Wrangling_for_KBO/blob/master/doc/game_info.md)를 보시고, 기존 자료에 추가할 다음 게임 자료를 다 모았다고 가정하겠습니다. 이 자료는 `data/temp_data.json`이라는 파일에 들어있게 됩니다.

```python
import game_info
data_8 = game_info.get_data(2020, 8, "정규")
game_id_8 = game_info.modify_data(2020, data_8)
data = games.get_data(game_id_8)
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
