# 모든 자료로 DB로

지금까지 만든 자료를 DB에 올려봅시다.

```python
hanhwa_pitcher = pd.read_csv("./sample/Hanhwa_pitcher_data_2018.csv")

import sqlite3
conn = sqlite3.connect('test.db')
hanhwa_pitcher.to_sql('hanhwa_pitcher', conn)
cur = conn.cursor()
cur.execute("select * from hanhwa_pitcher")
rows = cur.fetchall()

for row in rows:
    print(row)
cur.close()

conn.close()
```

앞에서 만든 DB를 저장해봅시다.

```python
def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')

bck = sqlite3.connect('backup.db')

with bck:
    conn.backup(bck, pages=1, progress=progress)
bck.close()
```