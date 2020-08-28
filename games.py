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