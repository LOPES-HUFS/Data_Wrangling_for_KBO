import json
from selenium import webdriver
from bs4 import BeautifulSoup
from pasing_page import scoreboard,ETC_info,looking_for_team_name
from pasing_page import away_batter,home_batter,away_pitcher,home_pitcher
from modify_data import batter_clean,pitcher_clean
import configparser

config = configparser.ConfigParser()
# 설정파일을 읽어옵니다.
config.read('config.ini')
# 설정파일에 들어있는 KBO url을 가져 옵니다.
url = config['DEFAULT']['KBO_URL']

def getting_page(gameDate,gameld):
    """
    단일 게임 자료를 받아오는 함수이다.

    :param gameDate: "20181010" 와 같이 경기 날짜를 문자열로 받는다.
    :param gameld: 경기를 하는 팀명으로 만들어진다.
        "WOOB0"과 같이 만드는데, WO, OB는 각각 팀명을 의미하고
        0은 더블헤더 경기가 아닌 것을 알려준다.
        만약 더불헤더 경기면 1차전은 "KTLT1"처럼 1로 표시하고
        2차전이면 "KTLT2"으로 표시한다.

    사용법::
        >>> temp_page=getting_page("20181010","KTLT1")
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # 혹은 options.add_argument("--disable-gpu")
 
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    temp_url = url+gameDate+"&gameId="+gameDate+gameld+"&section=REVIEW"
    driver.get(temp_url)
    driver.implicitly_wait(3)
    #driver.get_screenshot_as_file('koreabaseball_headless.png')
    soup = BeautifulSoup(driver.page_source,"html5lib")
    tables = soup.find_all('table')
    record_etc = soup.findAll('div',{'class':'record-etc'})
    box_score = soup.findAll('div',{'class':'box-score-wrap'})
    teams = box_score[0].findAll('span',{'class':'logo'})
    return{'tables':tables, 'record_etc':record_etc, 'teams':teams, 'date':gameDate, 'id':gameld}

#temp_page=getting_page("20180816","WOOB0")

def get_data(date,codelist):
    temp_page=getting_page(date,codelist)
    temp_scoreboard = scoreboard(temp_page['tables'], temp_page['teams'])

    temp_all = {'scoreboard':ast.literal_eval(temp_scoreboard.to_json(orient='records'))}
    temp_all.update({"ETC_info":ETC_info(temp_page['tables'],temp_page['record_etc'])})
    temp_all.update({'away_batter':ast.literal_eval(away_batter(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})
    temp_all.update({'home_batter':ast.literal_eval(home_batter(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})
    temp_all.update({'away_pitcher':ast.literal_eval(away_pitcher(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})
    temp_all.update({'home_pitcher':ast.literal_eval(home_pitcher(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})

    temp_name = temp_page['date']+'_'+temp_page['id']
    return {temp_name:temp_all}

hanhwa=pd.read_csv("./data/sample_codelist.csv")
hanhwa.date=hanhwa.date.astype(str)

temp_full = {}
for i in range(0,len(hanhwa)):
    print(i)
    temp_data = get_data(hanhwa.date[i],hanhwa.codelist[i])
    temp_data = batter_clean(temp_data,'away_batter')
    temp_data = batter_clean(temp_data,'home_batter')
    temp_data = pitcher_clean(temp_data,'away_pitcher')
    temp_data = pitcher_clean(temp_data,'home_pitcher')
    temp_full.update(temp_data)

temp_file_name = "hanhwa"+"_"+"normalseason"+"_"+"2018"+".json"

with open(temp_file_name, 'w') as outfile:  
    json.dump(temp_full, outfile)

'''
위에서 만든 파일을 DataFrame으로 여는 법
앞에서 만든 파일 명과 같은 이름으로 된 파일을 엽니다.

>>> with open(temp_file_name) as outfile:  
>>>    data= json.load(outfile)

>>> pd.DataFrame(data['scoreboard'])
'''