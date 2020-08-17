import requests
from bs4 import BeautifulSoup
import csv
import json


def finding_player(name):
    url =(f'https://www.koreabaseball.com/Player/Search.aspx?searchWord={name}')
    r = requests.post(url)
    try:
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find('table')
        table_rows = table.find_all('a')
        temp = [parsing_player(table_row) for table_row in table_rows]
        res = [{item['ID']:item} for item in temp]
    except:
        error_list.append(name)
    return (res)

def parsing_player(table_row):
    table_rows = table.find_all('a')
    if str(table_row).split('/')[1] == 'Futures':
        status = 'Futures'
    elif str(table_row).split('/')[2] == 'Retire':
        status = '은퇴'
    else:
        status = 'KBO'
    player_id = str(table_row).split('playerId=')[1].split('">')[0]
    name = table_row.get_text()
    return{"ID":player_id, "이름":name, "현재 상태":status}