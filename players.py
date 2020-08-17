import requests
from bs4 import BeautifulSoup
import csv
import json

player_search_url = "https://www.koreabaseball.com/Player/Search.aspx?searchWord="

def searching(name):
    url = (f'{player_search_url}{name}')
    r = requests.post(url)
    try:
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find('table')
        table_rows = table.find_all('a')
        tds = table.find_all('td')
        temp = [parsing_player_table(table_row, tds) for table_row in table_rows]
        res = [{item['ID']:item} for item in temp]
    except:
        res = False
    return (res)

def parsing_player_table(table_row, tds):
    if str(table_row).split('/')[1] == 'Futures':
        status = 'Futures'
    elif str(table_row).split('/')[2] == 'Retire':
        status = '은퇴'
    else:
        status = 'KBO'
    player_id = str(table_row).split('playerId=')[1].split('">')[0]
    team = tds[2].get_text()
    name = table_row.get_text()
    return{"ID":player_id, "이름":name, "현재 상태":status, "team": team}

def searching_players(players_list):
    total = []
    error_list =[]
    
    for name in players_list:
        temp = searching(name)
        if len(temp) == 0:
            error_list.append(name)
        else:
            total += temp
    return {"list":total, "error_list":error_list}
