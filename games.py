import json
import ast

import pandas as pd

import single_game
import modifying_data

def get_data(game_list):
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

    data={}

    for i in range(0,len(game_list)):
        temp_data = single_game.get_data(game_list.date[i], game_list.gameid[i])
        temp_data = single_game.modify_data(temp_data)
        data.update(temp_data)
    
    return data

def making_scoreboard(data):
    data = modifying_data.scoreboard(data)
    scoreboard = pd.DataFrame()
    
    for i in data.keys():
        scoreboard = scoreboard.append(pd.DataFrame(data[i]['scoreboard']), sort=True)
    
    scoreboard = pd.DataFrame(
        scoreboard, columns=['year', 'month', 'day', 'week', '팀', '승패', \
                                  'i_1', 'i_2', 'i_3', 'i_4', 'i_5', 'i_6', \
                                  'i_7', 'i_8','i_9', 'i_10', 'i_11','i_12', \
                                  'R', 'H', 'E', 'B', '홈팀', '원정팀', '더블헤더'])
    scoreboard = scoreboard.reset_index(drop=True)
    return(scoreboard)

def making_batter(data):
    away_team = pd.DataFrame()
    home_team = pd.DataFrame()

    for i in data.keys():
        away_team = away_team.append(pd.DataFrame(data[i]['away_batter']),sort = True)
        home_team = home_team.append(pd.DataFrame(data[i]['home_batter']),sort = True)
    
    temp = pd.concat([away_team, home_team], ignore_index = True)
    temp = pd.DataFrame(temp, columns=['경기날짜','선수명','포지션','팀',"더블헤더여부",'홈팀','원정팀', \
                                       '1','2','3','4','5','6','7','8','9','10','11','12', \
                                       '안타','타수','타율','타점','득점'])
    temp = temp.fillna(0)
    temp = temp.astype({'1': int, '2':int, '3':int, '4':int, '5':int, '6':int, '7':int, '8':int, '9':int, '10':int, '11':int, '12':int})

    temp.rename(columns = {'1':'i_1', '2':'i_2', '3':'i_3', '4':'i_4', '5':'i_5', '6':'i_6', '7':'i_7', '8':'i_8', '9':'i_9', '10':'i_10', '11':'i_11', '12':'i_12'}, inplace=True)

    temp.rename(columns = {'더블헤더여부':'더블헤더'}, inplace=True)
    temp["경기날짜"] = pd.to_datetime(temp['경기날짜'], format='%Y-%m-%d')

    
    temp.loc[:, 'year'] = temp['경기날짜'].dt.year

    temp.loc[:, 'month'] = temp['경기날짜'].dt.month
    temp.loc[:, 'day'] = temp['경기날짜'].dt.day
    temp.loc[:, 'week'] = temp['경기날짜'].dt.dayofweek
    temp.pop('경기날짜')

    return temp

def making_pitcher(data):
    away_team = pd.DataFrame()
    home_team = pd.DataFrame()

    for i in data.keys():
        away_team = away_team.append(pd.DataFrame(data[i]['away_pitcher']),sort = True)
        home_team = home_team.append(pd.DataFrame(data[i]['away_pitcher']),sort = True)
    
    temp = pd.concat([away_team, home_team], ignore_index = True)
    temp = pd.DataFrame(temp,
                            columns=['경기날짜','선수명','포지션','팀','더블헤더여부','홈팀','원정팀','등판', 'inning', 'restinning', '승리','패배','무승부','세이브','홀드','삼진','4사구','실점','자책','투구수','피안타','피홈런', '타수', '타자'])
    temp = temp.fillna(0)
    temp.rename(columns = {'inning':'이닝'}, inplace=True)
    temp.rename(columns = {'restinning':'잔여이닝'}, inplace=True)
    temp.rename(columns = {'더블헤더여부':'더블헤더'}, inplace=True)
    temp.rename(columns = {'승리':'승'}, inplace=True)
    temp.rename(columns = {'패배':'패'}, inplace=True)
    temp.rename(columns = {'4사구':'사사구'}, inplace=True)

    temp["경기날짜"] = pd.to_datetime(temp['경기날짜'], format='%Y-%m-%d')

    temp.loc[:, 'year'] = temp['경기날짜'].dt.year
    temp.loc[:, 'month'] = temp['경기날짜'].dt.month
    temp.loc[:, 'day'] = temp['경기날짜'].dt.day
    temp.loc[:, 'week'] = temp['경기날짜'].dt.dayofweek
    temp.pop('경기날짜')
    
    temp = pd.DataFrame(temp, columns=['year', 'month', 'day', 'week', \
                                       '선수명', '포지션', '팀', '더블헤더', '홈팀', '원정팀',\
                                       '등판', '이닝', '잔여이닝', '승리', '패배', '무승부', '세이브', \
                                       '홀드','삼진','사사구','실점','자책','투구수','피안타','피홈런', '타수', '타자'])

    return temp