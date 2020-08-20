from selenium import webdriver
import pandas as pd
import time
import re
import configparser

config = configparser.ConfigParser()
# 설정파일을 읽어옵니다.
config.read('config.ini')
Game_info_URL = config['DEFAULT']['Game_info_URL']
chromium_location = config['DEFAULT']['chromium_location']

def get_table(year,month,season):
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
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    url = Game_info_URL + season
    #url = f"https://www.koreabaseball.com/Schedule/Schedule.aspx?seriesId={season}" # 시범=1 정규=0,9 포스트=3,4,5,7
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
        gamelist.append([d.text for d in row.find_elements_by_css_selector('td')])
        
    del gamelist[0]
    
    [gamelist[i].insert(0,gamelist[i-1][0]) for i in range(0,len(gamelist)) if len(gamelist[i])==8]
    
    gamelist_df=pd.DataFrame(gamelist,columns=['날짜','시간','경기','게임센터','하이라이트','TV','라디오','구장','비고'])
    driver.close()
    return gamelist_df

team_list={'HT':'KIA','OB':'두산','LT':'롯데','NC':'NC','SK':'SK','LG':'LG','WO':'키움','HH':'한화','SS':'삼성','KT':'KT'}

def change_team_name(string):
    temp = [string.find(team) for team in team_list.values()]
    temp[:] = [0 if ele != -1 else ele for ele in temp]
    temp=temp.index(0)
    temp=list(team_list.items())[temp]
    return temp[0]

def change_df(data):
    '''
    입력값: data는 get_game_info_table 함수의 return 값

    출력값: 날짜 원정팀, 홈팀 gameid가 포함된 DF
    '''

    data = data[(data['비고'] != "우천취소") & (data['비고'] !="강풍취소")]

    gameinfo=[s.split("vs") for s in data['경기']]
    awayteam = []
    hometeam = []
    for i in gameinfo:
        awayteam.append(''.join(re.findall('[^0-9]',i[0])))
        hometeam.append(''.join(re.findall('[^0-9]',i[1])))

    homecode=[change_team_name(i) for i in hometeam]
    awaycode=[change_team_name(i) for i in awayteam]

    date=["2020"+i.split(".")[0]+"".join(re.findall("[0-9]",i.split(".")[1])) for i in data['날짜']]
    gameid = [awaycode[i]+homecode[i]+"0" for i in range(0,len(awaycode))]
    gameid_list = pd.DataFrame({"date":date,"away":awaycode,"home":homecode,"gameid":gameid})

    double_header = gameid_list.index[gameid_list.duplicated(keep=False)==True]
    
    one=[i for i in range(0,len(double_header)) if i % 2 == 1]
    gameid_list.gameid[double_header[one]] = [str(i).replace("0","2") for i in gameid_list.gameid[double_header[one]]]
    gameid_list.gameid[double_header[[x for x in range(0,len(double_header)) if x not in one]]] = [str(i).replace("0","1") for i in gameid_list.gameid[double_header[[x for x in range(0,len(double_header)) if x not in one]]]]

    gameid_list = gameid_list[gameid_list.gameid!="드림나눔0"]

    return gameid_list



#may_data = get_game_info_table(2020,"05","정규")
#june_data = get_game_info_table(2020,"06","정규")
#july_data = get_game_info_table(2020,"07","정규")

#game_id_may = get_game_list(may_data)
#game_id_june = get_game_list(june_data)
#game_id_july = get_game_list(july_data)

#game_ids_df = pd.concat([game_id_may,game_id_june,game_id_july])

#game_ids_df.to_csv("kbo_2020_gameid_list.csv")
