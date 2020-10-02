import time
from datetime import datetime
import re
import configparser

from selenium import webdriver
import pandas as pd


config = configparser.ConfigParser()
# 설정파일을 읽어옵니다.
config.read('config.ini')
Game_info_URL = config['DEFAULT']['Game_info_URL']
chromium_location = config['DEFAULT']['chromium_location']

team_list = {'KIA':'HT', '두산':'OB', '롯데':'LT', \
                'NC':'NC', 'SK':'SK', 'LG':'LG', \
                '넥센': 'WO','키움':'WO','한화':'HH', \
                '삼성': 'SS','KT':'KT'} 

def get_data(year, month, season):
    ''' 
        Args: year,month,season
        year: 원하는 게임의 연도
        month: 원하는 게임의 월
        season: 시범, 정규, 포스트 
    
    Returns:
        게임 일정 df
    '''
    if season == "시범":
        season = 1
    elif season == "정규":
        season = "0,9"
    else:
        season = "3,4"

    month = str(month).zfill(2)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    url = Game_info_URL + season
    driver = webdriver.Chrome(chromium_location, chrome_options=options)
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_id('ddlYear').send_keys(year)
    time.sleep(1)
    driver.find_element_by_id('ddlMonth').send_keys(month)
    time.sleep(1)
    table = driver.find_element_by_css_selector("table")
    gamelist=[]
    for row in table.find_elements_by_css_selector('tr'):
        gamelist.append([ \
            d.text for d in row.find_elements_by_css_selector('td')])
        
    del gamelist[0]
    
    [gamelist[i].insert(0, gamelist[i-1][0]) \
        for i in range(0, len(gamelist)) if len(gamelist[i])==8]
    if gamelist[0][0] ==  '데이터가 없습니다.':
        return "Please check the date, there are no games in the month of that year."    
    else:
        gamelist_df = pd.DataFrame( gamelist, \
            columns = ['날짜','시간','경기','게임센터','하이라이트','TV','라디오','구장','비고'])
    driver.close()
    return gamelist_df

def change_team_name(string):
    '''
    팀명을 코드로 바꿔 주는 함수.
    만약 팀명이 없는 경우에는 '없음'를 되돌려 준다.

    Arg:
        팀명 : (str)

    Returns:
        팀 코드
    '''

    try:
        return team_list[string]

    except:
        print(string)
        return '없음'

def modify_data(year, data):
    '''
    입력값: data는 get_game_info_table 함수의 return 값

    출력값: 날짜 원정팀, 홈팀 gameid가 포함된 DF
    '''

    data = data[(data['비고'] != "우천취소") & \
                (data['비고'] !="강풍취소") & \
                (data['비고'] !="그라운드사정") & \
                (data['비고'] !="기타") & \
                (data['비고'] !="미세먼지취소")]

    gameinfo=[s.split("vs") for s in data['경기']]
    awayteam = []
    hometeam = []
    for i in gameinfo:
        awayteam.append(''.join(re.findall('[^0-9]',i[0])))
        hometeam.append(''.join(re.findall('[^0-9]',i[1])))

    homecode=[change_team_name(i) for i in hometeam]
    awaycode=[change_team_name(i) for i in awayteam]

    date = [str(year) + i.split(".")[0] + \
        "".join(re.findall("[0-9]",i.split(".")[1])) for i in data['날짜']]
    
    gameid = [awaycode[i] + homecode[i] + "0" for i in range(0,len(awaycode))]
    gameid_list = pd.DataFrame( \
            {"date": date, "away":awaycode,"home":homecode,"gameid":gameid})

    double_header = gameid_list.index[gameid_list.duplicated(keep=False)==True]
    
    one=[i for i in range(0,len(double_header)) if i % 2 == 1]
    gameid_list.gameid[double_header[one]] = [str(i).replace("0","2") for i in gameid_list.gameid[double_header[one]]]
    gameid_list.gameid[double_header[[x for x in range(0,len(double_header)) if x not in one]]] = [str(i).replace("0","1") for i in gameid_list.gameid[double_header[[x for x in range(0,len(double_header)) if x not in one]]]]

    gameid_list = gameid_list[gameid_list['home'] != "없음"]
    gameid_list = gameid_list.reset_index(drop=True)

    return gameid_list

def get_data_and_merge(year,month):
    result = pd.DataFrame()
    for i in month:
       temp = get_data(year,i,"정규")
       monthly_data = modify_data(year,temp)
       result = result.append(monthly_data)
    result.to_csv("2020_gameid.csv",index=False)

def get_year_game_info_until_now():
    """
    현재를 기준으로 올해 정규 시즌 데이터를 받기 위해 게임 정보를 받아오는 함수 
    """
    
    result = pd.DataFrame()
    now = datetime.now()
    month = now.month
    year = now.year

    for i in range(month):
        temp_month = i + 1
        temp = get_data(year, temp_month, "정규")
        monthly_data = modify_data(year, temp)
        result = result.append(monthly_data)
    return result

def get_month_game_info_until_now():
    """
    현재를 기준으로 올해 이번 달 정규 시즌 데이터를 받기 위해 게임 정보를 받아오는 함수 
    """
    
    now = datetime.now()

    temp = get_data(now.year, now.month, "정규")
    game_id = modify_data(now.year, temp)

    temp = pd.to_datetime(game_id['date']) < now 

    return game_id[temp]
