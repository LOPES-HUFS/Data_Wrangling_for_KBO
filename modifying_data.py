import ast
import datetime

import pandas as pd

from pasing_page import looking_for_team_name


def change_record(temp,column,factorlist):
    for i in range(0,len(temp[[str(column)]])):
        if "/" in list(str(temp[str(column)].tolist()[i])):
            temp1=factorlist.code[factorlist.factor_list==str(temp[str(column)].tolist()[i].split("/ ")[0].split("\\")[0])]
            temp2=factorlist.code[factorlist.factor_list==str(temp[str(column)].tolist()[i].split("/ ")[1])]
            temp.loc[i,str(column)]=str(list(temp1)[0])+str(list(temp2)[0])
    return temp

def batter_clean(data,section):
    temp_b=pd.DataFrame(data[list(data.keys())[0]][section])
    temp_b['경기날짜']= list(data.keys())[0][0:4]+"-"+list(data.keys())[0][4:6]+"-"+list(data.keys())[0][6:8]
    temp_b['원정팀']=looking_for_team_name(list(data.keys())[0][9:11])
    temp_b['홈팀']=looking_for_team_name(list(data.keys())[0][11:13])
    temp_b['더블헤더여부'] = list(data.keys())[0][-1]
    factorlist = pd.read_csv("./data/KBO_factor_list.csv")
    for i in factorlist.factor_list:
        temp_b=temp_b.replace(i,factorlist.code[factorlist.factor_list==i].tolist()[0])
        
    columns=[x for x in temp_b.columns if x in ['1', '2', '3', '4', '5', '6', '7', '8', '9',"10","11","12"]]
    for j in columns:
        temp_b=change_record(temp_b,j,factorlist)

    data[list(data.keys())[0]][section]=ast.literal_eval(temp_b.to_json(orient='records'))
    return data

def change_inning(item):
    if ('/' and " ") in list(str(item)):
        inning=list(item)[0]
        rest_inning=list(item)[2]
    elif '/' in list(str(item)):
        inning=0
        rest_inning=item.split('\/')[0]
    else:
        inning=item
        rest_inning=0
    
    return [inning,rest_inning]

#section은 away_pitcher,home_pitcher 구분
def pitcher_clean(data,section):
    temp_p=pd.DataFrame(data[list(data.keys())[0]][section])
    temp_p['경기날짜'] = list(data.keys())[0][0:4]+"-"+list(data.keys())[0][4:6]+"-"+list(data.keys())[0][6:8]
    temp_p['원정팀'] = looking_for_team_name(list(data.keys())[0][9:11])
    temp_p['홈팀'] = looking_for_team_name(list(data.keys())[0][11:13])
    temp_p['더블헤더여부'] = list(data.keys())[0][-1]
    temp1 = temp_p['등판'] == '선발'
    temp1 = temp1.replace(True,"선발투수")
    temp1 = temp1.replace(False,"불펜투수")
    temp_p['포지션'] = temp1
    temp_p['등판'] = temp_p['등판'].replace('선발',1.1)
    temp_p['결과']= temp_p['결과'].astype(str)
    temp2=temp_p['결과']=='승'
    temp_p['승리'] = temp2.astype(int)
    temp3 = temp_p['결과']=='패'
    temp_p['패배'] = temp3.astype(int)
    temp4 = temp_p['결과']=='무'
    temp_p['무승부'] = temp4.astype(int)
    temp5 = temp_p['결과']=='홀드'
    temp_p['홀드'] = temp5.astype(int)
    temp6 = temp_p['결과']=='세'
    temp_p['세이브'] = temp6.astype(int)
    temp7= temp_p['이닝'].map(lambda x :change_inning(x))
    temp_p['inning'] = temp7.map(lambda x :x[0])
    temp_p['restinning'] = temp7.map(lambda x :x[1])
    temp_p = temp_p[['경기날짜','선수명','포지션','등판','원정팀','홈팀','더블헤더여부','팀','승리', '패배', '무승부', '홀드', '세이브', 'inning', 
            'restinning','4사구','삼진','실점', '자책','투구수','피안타','홈런','타수', '타자']]
    data[list(data.keys())[0]][section]=ast.literal_eval(temp_p.to_json(orient='records'))
    return data

def get_game_info(game_list):
                
    #temp = list(data.keys())[0].split('_')
    #temp_date = str(game_list.date[1])
    temp_date = game_list.split('_')[0]
    temp_date = datetime.datetime.strptime(temp_date.split("_")[0], '%Y%m%d')
    temp = {"year": temp_date.year, "month": temp_date.month, "day": temp_date.day, "week": temp_date.weekday()}
    
    temp_team = game_list.split('_')[1]
    temp_team = {"홈팀": temp_team[0:2], "원정팀": temp_team[2:4], "더블헤더":int(temp_team[4:])}
    temp.update(temp_team)
    
    return temp

def scoreboard(data):
    """
    Args: 
        game_list (pd): pd.read_csv()함수로 읽은 다음과 같은 게임 리스트

             date gameid
    0    20180324  HHWO0
    1    20180325  HHWO0
    2    20180327  HHNC0
    
    Returns:
        (json): 리스트에 들어 있는 전체 
    """
    i = 0
    
    for key, value in data.items():
        temp_p = pd.DataFrame(value['scoreboard'])
        game_info = get_game_info(key)
        temp_p.loc[:, 'year'] = game_info['year']
        temp_p.loc[:, 'month'] = game_info['month']
        temp_p.loc[:, 'day'] = game_info['day']
        temp_p.loc[:, 'week'] = game_info['week']
        temp_p.loc[:, '홈팀'] = game_info['홈팀']
        temp_p.loc[:, '원정팀'] = game_info['원정팀']
        temp_p.loc[:, '더블헤더'] = game_info['더블헤더']
        #print(ast.literal_eval(temp_p.to_json(orient='records')))
        data[list(data.keys())[i]]['scoreboard'] = ast.literal_eval(temp_p.to_json(orient='records'))
        i = i + 1
    return data