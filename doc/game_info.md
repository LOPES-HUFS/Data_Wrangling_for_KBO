# 게임 정보 가져오기

현재 스트크립트가 돌아가서 자료를 가지고 오려면, `"20200801","HHLG0"`과 같은 형식 KBO 게임 일정 자료가 필요합니다. 이 프로젝트에서는 이것을 이용해서 `main.get_data()`를 이용해서 경기 데이터를 불러옵니다.

```python
HHLG0_20200801 = get_data("20200801","HHLG0")
```

이때 "20200801"은 경기 날짜, "HHLG0"은 한화, 엘지 1번째 경기를 뜻합니다. 파이썬에서 0부터 숫자를 세기 때문에 0이 첫번째 경기입니다.

따라서 모든 경기를 불러오기 위해서는 앞에서 소개한 형식의 KBO 스케줄 자료가 필요합니다. 현재 이 레포지토리에는 [KBO_game_schedule.csv](https://github.com/LOPES-HUFS/Data_Wrangling_for_KBO/blob/master/data/KBO_game_schedule.csv)에 2010년 3월 부터 2020년 8월까지의 KBO 게임 일정 자료가 들어 있습니다. 이를 이용하시면, 손쉽게 자료를 다운 받으실 수 있습니다.

이 파일에 없는 게임 자료를 받으려면, 예를 들어 2020년 9월 자료를 받으려면, 위에서 말한 자료 목록을 만들어어야 합니다. 이 자료를 만드는 함수가 `game_info.get_data()`입니다. 이 함수의 용법은 다음과 같습니다. `game_info.modify_data()`는 받은 것을 우리가 사용하기 쉽게 정리하는 함수입니다. 다음과 같이 하시면 2020년 5월 자료를 받으실 수 있습니다.

```python
import game_info
may_data = game_info.get_data(2020, 5, "정규")
game_id_may = game_info.modify_data(2020, may_data)
```

만약 특정 시간 자료를 받으시려면 다음과 같이 하시면 됩니다.

```python
game_info.get_data_and_merge(2020,[5, 6, 7, 8])
```

## 현재까지의 KBO 정규 시즌 자료 다운 받기

현재를 기준으로 올해 정규 시즌 일정 데이터를 받기 위해 게임 정보를 받아오시려면 다음과 같이 하면 됩니다.

```python
temp = game_info.get_year_game_info_until_now()
```

그러나 기본적으로 저희 팀에서 2010년부터 조사한 전체 정규 시즌 일정을 [KBO_game_schedule.csv](https://github.com/LOPES-HUFS/Data_Wrangling_for_KBO/blob/master/data/KBO_game_schedule.csv)이라는 파일에 저장하고 있으며, 지속적으로 갱신하고 있습니다. 그래서 여러분이 년 단위의 시즌 일정 데이터를 받아오실 필요는 없습니다. 만약 만약 현재 현재 달 정규 시즌 일정을 받으시려면 아래 코드를 이용하시면 어제까지의 일정을 받으실 수 있습니다.

```python
import game_info
temp = game_info.get_month_game_info_until_now()
```

참고로 위에서 만든 코드를 가지고 모은 일정 자료를 가지고 실제 경기 자료를 모으려면 다음과 같이 하면 됩니다. 시간이 오래걸릴 수도 있기 때문에 주의하시기 바랍니다. 테스트만 하고 싶은 분은 아래 주석처리된 `games.get_data(temp[:1])`을 실행시키면 됩니다.

```python
import game_info
import games
temp = game_info.get_month_game_info_until_now()
# games.get_data(temp[:1])
 this_month_games = games.get_data(temp)
```

만약 앞에서 저장한 이번 달 경기 자료를 `csv`형식으로 저장하고자 한다면 다음과 같이 하면 됩니다.

```python
temp_data = temp[['date','gameid']]
temp_data.to_csv("data/temp_schedule.csv", index = False)
```
