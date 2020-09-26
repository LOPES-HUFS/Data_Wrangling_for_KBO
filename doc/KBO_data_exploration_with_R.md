# R로 KBO 데이터 분석하기

현재 자료가 완벽하게 정리되어 있지는 않습니다. 그러나 자료가 충분히 모이면 R을 이용하여 KBO 자료를 분석할 예정입니다. 이 문서를 그 내용을 정리하고자 합니다.

## 필요한 R 패키지

우선 사용하기 위해서는 다음 패키지가 설치되어 있어야 합니다.

```R
install.packages("tidyverse")
install.packages("RSQLite")
install.packages("arrow")
```

## RSQLite를 이용하여 선수 테이더 살펴보기

만들어 놓은 자료를 R을 이용해서 SQLite에 올려봅시다. 이 글은 외부 DB를 사용하는 것을 상정하고 만들었기 때문에 SQLite을 이용하여 DB를 사용하는 작업 환경을 설정하고 있습니다. 우선 자료를 다운받습니다.

```R
url <- "https://raw.githubusercontent.com/LOPES-HUFS/Data_Wrangling_for_KBO/master/sample/test.db"
download.file(url = url, destfile ="test.db")

```

다운받은 파일롤 DB를 만들어봅시다.

```R
con <- DBI::dbConnect(RSQLite::SQLite(), "test.db")
```

SQLite에 올린 자료를 R에서 사용하기 위하여 야수와 투수 자료를 뽑습니다.

```R
pitcher <- tbl(con, "pitcher")
batter <- tbl(con, "batter")
pitcher
batter
```

한화 샘슨 선수의 등판 이닝을 모두 찾아 합쳐봅시다.

```R
pitcher %>%
    filter(선수명 == "샘슨") %>%
    summarize(sum = sum(등판), na.rm = TRUE)
```

한화 이용규 선수의 한 게임 안타 평균을 구해 봅시다. 다음으로 요일 경기를 뽑아봅시다. 0이 월요일 6이 일요일입니다.

```R
batter %>%
    filter(선수명 == "이용규") %>%
    filter(week == 5) %>%
    summarize(mean = mean(안타), na.rm = TRUE)

batter %>%
    filter(선수명 == "이용규") %>%
    filter(week == 4) %>%
    summarize(mean = mean(안타), na.rm = TRUE)
```

1회 선택

```R
> batter %>%
    filter(선수명 == "이용규") %>%
    filter(week == 5) %>%
    select(i_1)

```

다 사용했으면 연결 해체

```R
dbListTables(con)
```

## 스코어 자료를 이용한 팀 데이터 살펴보기

스코어보드 자료를 가져옵니댜. 이번에는 `parquet`형식으로 만들 파일을 가져오겠습니다. 이 형식은 자료를 기본적으로 압축하기 때문에 사용하기가 편리합니다.

```R
url <- "https://raw.githubusercontent.com/LOPES-HUFS/Data_Wrangling_for_KBO/master/sample/scoreboard.parquet"
download.file(url = url, destfile = "scoreboard.parquet")
scoreboard <- read_parquet("scoreboard.parquet")
```

현재 `scoreboard`에는 날짜가 복잡하게 다음과 같이 들어 있습니다.

```R
> scoreboard %>%
+ select(year, month, day)
# A tibble: 13,614 x 3
    year month   day
   <int> <int> <int>
 1  2010     3    27
 2  2010     3    27
 3  2010     3    27
 4  2010     3    27
 5  2010     3    27
 6  2010     3    27
 7  2010     3    27
 8  2010     3    27
 9  2010     3    28
10  2010     3    28
# … with 13,604 more rows

```

이를 쉽게 사용하는 방법은 다음과 같습니다. `make_date()`로 시계열 날짜를 만들 수 있습니다. 만약 시분초까지 추가하고 싶다면 `make_datetime()`을 대신 사용하면 됩니다. 현재 자료에는 그런 것이 없기 때문에 아래와 같이 사용하면 됩니다.

```R
> scoreboard %>%
+ select(year, month, day) %>%
+ mutate(date = make_date(year, month, day))
# A tibble: 13,614 x 4
    year month   day date
   <int> <int> <int> <date>
 1  2010     3    27 2010-03-27
 2  2010     3    27 2010-03-27
 3  2010     3    27 2010-03-27
 4  2010     3    27 2010-03-27
 5  2010     3    27 2010-03-27
 6  2010     3    27 2010-03-27
 7  2010     3    27 2010-03-27
 8  2010     3    27 2010-03-27
 9  2010     3    28 2010-03-28
10  2010     3    28 2010-03-28
# … with 13,604 more rows
```

현재 입력된 자료에는 팀명이 다음과 같이 문자열로 들어 습니다.

```R
> scoreboard %>%
+ select(팀, 홈팀, 원정팀)
# A tibble: 13,614 x 3
   팀    홈팀  원정팀
   <chr> <chr> <chr>
 1 기아  기아  두산  
 2 두산  기아  두산  
 3 한화  한화  SK
 4 SK    한화  SK
 5 LG    LG    삼성  
 6 삼성  LG    삼성  
 7 키움  키움  롯데  
 8 롯데  키움  롯데  
 9 한화  한화  SK
10 SK    한화  SK
# … with 13,604 more rows
```

이를 팩터형으로 바꿔보면 다음과 같이 동일합니다. 당연합니다. ^^;

```R
> levels(factor(scoreboard$팀))
 [1] "기아" "두산" "롯데" "삼성" "키움" "한화" "KT"   "LG"   "NC"   "SK"  
> levels(factor(scoreboard$홈팀))
 [1] "기아" "두산" "롯데" "삼성" "키움" "한화" "KT"   "LG"   "NC"   "SK"  
> levels(factor(scoreboard$원정팀))
 [1] "기아" "두산" "롯데" "삼성" "키움" "한화" "KT"   "LG"   "NC"   "SK"  
```

그리고 승패도 바꾸보면 아래와 같이 됩니다.

```R
> levels(factor(scoreboard$승패))
[1] "무" "승" "패"
```

그러면 지금까지 한 것을 토대로 `scoreboard`에서 승패만 뽑아봅아 새로운 `tibble`을 만들어 봅시다.

```R
scoreboard_win <- scoreboard %>%
    mutate(
        date = make_date(year, month, day),
        team = factor(팀),
        home_team = factor(팀) == factor(홈팀),
        win = factor(scoreboard$승패)
    ) %>%
    select(date, team, home_team, win)
```

홈팀이 두산팀만 뽑고 싶다면,

```R
scoreboard_win %>%
    filter(team == "두산")
```

결과는 다음과 같습니다.

```R
> scoreboard_win %>%
+     filter(team == "두산")
# A tibble: 1,468 x 4
   date       team  home_team win  
   <date>     <fct> <lgl>     <fct>
 1 2010-03-27 두산  FALSE     승
 2 2010-03-28 두산  FALSE     승
 3 2010-03-30 두산  TRUE      승
 4 2010-04-02 두산  TRUE      승
 5 2010-04-03 두산  TRUE      패
 6 2010-04-04 두산  TRUE      승
 7 2010-04-06 두산  FALSE     승
 8 2010-04-07 두산  FALSE     승
 9 2010-04-08 두산  FALSE     승
10 2010-04-09 두산  FALSE     무
# … with 1,458 more rows
```

위의 결과를 조금 더 확장해서, 두산의 연도별 승패를 뽑아보겠습니다.

- 1번째 줄에서 두산 자료만 뽑고,
- 2번째 줄은 `select`은 필요한 날짜, 승패를 선택한 다음,
- 3번째 줄은 date에서 year를 뽑아 새로운 줄을 만들고,
- 4번째 줄은 앞에서 뽑은 year으로 묶은 다음,
- 5번째 줄은 이렇게 묶은 것을 승패를 계산하게 됩니다.

```R
scoreboard_win %>%
    filter(team == "두산") %>%
    select(date, win) %>%
    mutate(year = factor(year(date))) %>%
    group_by(year) %>%
    count(win)
```

결과는 다음과 같습니다.

```R
> scoreboard_win %>%
+     filter(team == "두산") %>%
+     select(date, win) %>%
+     mutate(year = factor(year(date))) %>%
+     group_by(year) %>%
+     count(win)
# A tibble: 31 x 3
# Groups:   year [11]
   year  win       n
   <fct> <fct> <int>
 1 2010  무        3
 2 2010  승       73
 3 2010  패       57
 4 2011  무        2
 5 2011  승       61
 6 2011  패       70
 7 2012  무        3
 8 2012  승       68
 9 2012  패       62
10 2013  무        3
# … with 21 more rows
```

앞에서 작업한 것을 토대로 그래프를 그리면 다음과 같습니다. 앞에서 year를 `factor`으로 바꾸지 않으면, year가 숫자로 남기 때문에 그래프가 이쁘지 않습니다. x축은 연도(year), y축은 승패숫자(win)를 계산한 결과, `fill=win`은 win에 승,패,무라는 항목이 있는데 이를 따로 분리해서 그려보게 만드는 것입니다.

```R
temp <- scoreboard_win %>%
    filter(team == "두산") %>%
    select(date, win) %>%
    mutate(year = factor(year(date))) %>%
    group_by(year) %>%
    count(win)

ggplot(data = temp, aes(x = year, y = n, fill=win)) +
    geom_bar(stat="identity", position=position_dodge())
```

이번에는 주별 승패 결과를 세어본 것입니다.

```R
scoreboard_win %>%
    filter(team == "두산") %>%
    select(date, win) %>%
    mutate(wday = wday(date, label = TRUE)) %>%
    group_by(wday) %>%
    count(win)
```

아래 결과를 보시면 바로 아실 수 있습니다.

```R
> scoreboard_win %>%
+     filter(team == "두산") %>%
+     select(date, win) %>%
+     mutate(wday = wday(date, label = TRUE)) %>%
+     group_by(wday) %>%
+     count(win)
# A tibble: 20 x 3
# Groups:   wday [7]
   wday  win       n
   <ord> <fct> <int>
 1 일    무        2
 2 일    승      139
 3 일    패      107
 4 월    승        8
 5 월    패        5
 6 화    무        5
 7 화    승      135
 8 화    패       89
 9 수    무        2
10 수    승      130
11 수    패      108
12 목    무        2
13 목    승      141
14 목    패      109
15 금    무        3
16 금    승      134
17 금    패      100
18 토    무        5
19 토    승      133
20 토    패      111
```

앞에서 만든 것으로 그래프를 그려봅시다. 화요일은 당연히 경기가 없는 날이니 결과가 적습니다.

```R
temp <- scoreboard_win %>%
    filter(team == "두산") %>%
    select(date, win) %>%
    mutate(wday = wday(date, label = TRUE)) %>%
    group_by(wday) %>%
    count(win)

ggplot(data = temp, aes(x = wday, y = n, fill=win)) +
    geom_bar(stat="identity", position=position_dodge())
```
