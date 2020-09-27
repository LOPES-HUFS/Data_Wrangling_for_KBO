import json
import ast

import pandas as pd

import single_game
import modifying_data
import modifying_players_data as player

namelist = {"페르난데":"페르난데스","해즐베이":"해즐베이커","스몰린스":"스몰린스키","반슬라이":"반슬라이크"}

def get_data(game_list, number = 0):
    """
    디폴트는 game_list 0부터 시작하지만, 
    번호를 넣으시면 game_list에서 그 번호부터 시작하게 됩니다.
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

    if number != 0:
        try:
            for i in range(number, len(game_list)):
                temp_data = single_game.get_data(
                            str(game_list.date[i]), str(game_list.gameid[i]))
                temp_data = single_game.modify_data(temp_data)
                data.update(temp_data)
                print(f'Download complete: {i}',\
                        game_list.date[i], game_list.gameid[i])

        except:
            print(f'error: {i}', \
                    game_list.date[i], game_list.gameid[i])

    else:
        try:
            for i in range(0, len(game_list)):
                temp_data = single_game.get_data(
                            str(game_list.date[i]), str(game_list.gameid[i]))
                temp_data = single_game.modify_data(temp_data)
                data.update(temp_data)
                print(f'Download complete: {i}',\
                        game_list.date[i], game_list.gameid[i])
    
        except:
            print(f'error: {i}', \
                    game_list.date[i], game_list.gameid[i])

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
    # 9회 말 이전에 게임이 끝나면 점수가 '-' 문자로 들어 있는데
    # 이를 -1 숫자로 바꿔서 int 형으로 바꿀 수 있게 조작하였다.
    scoreboard = scoreboard.replace('-', -1)
    scoreboard = scoreboard.astype({
            'i_1':int, 'i_2':int, 'i_3':int, 'i_4':int, 'i_5':int, \
            'i_6':int, 'i_7':int, 'i_8':int, 'i_9':int, 'i_10':int, \
            'i_11':int, 'i_12':int})
    return(scoreboard)

def change_posision(data):
    '''
    data = pandas DF
    '''
    if '一' in data:
        data = data.replace("一","3")
    elif '二' in data: 
        data = data.replace("二","4")
    elif '三' in data:
        data = data.replace("三","5")
    elif "투" in data:
        data = data.replace("투","1")
    elif "포" in data:
        data = data.replace("포","2")
    elif "유" in data:
        data = data.replace("유","6")
    elif "좌" in data:
        data = data.replace("좌","7")
    elif "중" in data:
        data = data.replace("중","8")
    elif "우" in data:
        data = data.replace("우","9")
    elif "지" in data:
        data = data.replace("지","D")
    elif "주" in data:
        data = data.replace("주","R")
    elif "타" in data:
        data = data.replace("타","H")
    return data


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

    new_position_temp = [change_posision(i) for i in temp["포지션"]]
    new_position = [change_posision(i) for i in new_position_temp] 
    temp["포지션"] = new_position                                  
    #temp = temp.fillna(0)
    # 뛰지 않은 회에서는 값을 0으로 일괄 변경했지만, 이렇게 하면
    # 나중에 선발 라인없과 구별이 되지 않았다. 
    # 그래서 -1 값을 넣어서 구별하고자 한다.
    # 또한 연장 경기가 없어도 9회 이상의 열이 있는데 이것도 -1 로 표현한다.
    temp = temp.fillna(-1)
    temp = temp.astype({'1': int, '2':int, '3':int, '4':int, '5':int, '6':int, '7':int, '8':int, '9':int, '10':int, '11':int, '12':int})

    temp.rename(columns = {'1':'i_1', '2':'i_2', '3':'i_3', '4':'i_4', '5':'i_5', '6':'i_6', '7':'i_7', '8':'i_8', '9':'i_9', '10':'i_10', '11':'i_11', '12':'i_12'}, inplace=True)

    temp.rename(columns = {'더블헤더여부':'더블헤더'}, inplace=True)
    temp["경기날짜"] = pd.to_datetime(temp['경기날짜'], format='%Y-%m-%d')

    
    temp.loc[:, 'year'] = temp['경기날짜'].dt.year

    temp.loc[:, 'month'] = temp['경기날짜'].dt.month
    temp.loc[:, 'day'] = temp['경기날짜'].dt.day
    temp.loc[:, 'week'] = temp['경기날짜'].dt.dayofweek
    temp.pop('경기날짜')
    for i in temp["선수명"].unique():
        for j,k in namelist.items():
            if i == j:
                temp.loc[:,'선수명'][temp['선수명']==j] = k
            else:
                pass
    temp = player.make_player_id(temp)

    return temp

def making_pitcher(data):
    away_team = pd.DataFrame()
    home_team = pd.DataFrame()

    for i in data.keys():
        away_team = away_team.append(pd.DataFrame(data[i]['away_pitcher']),sort = True)
        home_team = home_team.append(pd.DataFrame(data[i]['home_pitcher']),sort = True)
    
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
                                       '등판', '이닝', '잔여이닝', '승', '패', '무승부', '세이브', \
                                       '홀드','삼진','사사구','실점','자책','투구수','피안타','피홈런', '타수', '타자'])

    temp = player.make_player_id(temp)    
    return temp