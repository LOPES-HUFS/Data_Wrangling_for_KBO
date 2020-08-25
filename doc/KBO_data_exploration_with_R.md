# R로 KBO 데이터 분석하기

현재 자료가 완벽하게 정리되어 있지는 않습니다. 그러나 자료가 충분히 모이면 R을 이용하여 KBO 자료를 분석할 예정입니다. 이 문서를 그 내용을 정리하고자 합니다.

## 필요한 R 패키지

우선 사용하기 위해서는 다음 패키지가 설치되어 있어야 합니다.

```R
install.packages("RSQLite")
install.packages("tidyverse")
```

## 사용법

만들어 놓은 자료를 R을 이용해서 SQLite에 올려봅시다.

```R
library(tidyverse)
con <- DBI::dbConnect(RSQLite::SQLite(), "test.db")
```

SQLite에 올린 자료를 R에서 사용하기 위하여 봅아봅시다.

```R
pitcher <- tbl(con, "pitcher")
batter <- tbl(con, "batter")
pitcher
batter
```

한화 샘슨 선수의 등판 이닝을 모두 합해봅시다.

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