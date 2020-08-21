# 게임 정보 가져오기

현재 스트크립트가 돌아가서 자료를 가지고 오려면, `"20200801","HHLG0"`과 같은 형식의 자료가 필요하다. 이 자료를 이용해서 `main.get_data()`를 이용해서 경기 데이터를 불러온다. 다음 예를 봅시다.

```python
HHLG0_20200801 = `get_data("20200801","HHLG0")
```

이때 "20200801"은 경기 날짜, "HHLG0"은 한화, 엘지 1번째 경기를 뜻합니다. 파이썬에서 0부터 숫자를 세기 때문에 0이 첫번째 경기입니다.

따라서 모든 경기를 불러오기 위해서는 앞에서 소개한 형식의 자료가 필요합니다. 현재 이 레포지토리에는 [KBO_gameid_full.csv](https://github.com/LOPES-HUFS/Data_Wrangling_for_KBO/blob/master/data/KBO_gameid_full.csv)에 2020년 8월까지의 자료가 들어 있습니다. 이를 이용하시면, 손쉽게 자료를 다운 받으실 수 있습니다.

이 파일에 없는 게임 자료를 받으려면, 예를 들어 2020년 9월 자료를 받으려면, 위에서 말한 자료 목록을 만들어어야 합니다. 이 자료를 만드는 함수가 `game_info.get_data()`입니다. 이 함수의 용법은 다음과 같습니다. `game_info.modify_data()`는 받은 것을 우리가 사용하기 쉽게 정리하는 함수입니다.

```python
import game_info
may_data = game_info.get_data(2020,"05","정규")
game_id_may = game_info.modify_data(2020, may_data)
```

```python
#game_ids_df = pd.concat([game_id_may,game_id_june,game_id_july])

# game_ids_df.to_csv("kbo_2020_gameid_list.csv")
game_info.get_data_and_merge(2020,["05","06","07","08"])

```
