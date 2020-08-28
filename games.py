import json
import ast

import pandas as pd

import single_game
from modifying_data import scoreboard

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

def modify(data, section):
    temp = scoreboard(data)
    return(temp)

