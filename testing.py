import pandas as pd
import json
temp_file_name = "./sample/Hanhwa_normalseason_2018.json"
with open(temp_file_name) as outfile:  
    hanhwa_data=json.load(outfile)

import games
Hanhwa_batter = games.making_batter(hanhwa_data)
Hanhwa_pitcher = games.making_pitcher(hanhwa_data)