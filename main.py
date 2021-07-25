import requests
from bs4 import BeautifulSoup

BALLISTICS_URI = "https://escapefromtarkov.fandom.com/wiki/Ballistics"
result = requests.get(BALLISTICS_URI)
soup = BeautifulSoup(result.content, 'html.parser')
ballistics_table = soup.find_all(id="trkballtablediv")[0]
rows = ballistics_table.find_all('tr')
ballistics_data = {}
skip_rows = 0
ammo_caliber = None
ammo_type = None
column_names = ["Damage", "pen", "armor dam%", "accuracy", "recoil", "fragment", "light bleed", "heavy bleed",
                "class 1", "class 2", "class 3", "class 4", "class 5", "class 6"]
for row in rows:
    column_index = 0
    if skip_rows > 2:
        if not row.get('id') is None:
            cells = row.find_all('td')
            ammo_caliber = None
            ammo_type = None
            for cell in cells:
                if ammo_caliber is None:
                    ammo_caliber = cell.getText().rstrip('\n')
                    ballistics_data[ammo_caliber] = {}
                elif ammo_type is None:
                    ammo_type = cell.getText().rstrip('\n')
                    ballistics_data[ammo_caliber][ammo_type] = {}
                else:
                    ballistics_data[ammo_caliber][ammo_type][column_names[column_index]] = cell.getText().rstrip('\n')
                    column_index += 1
        else:
            ammo_type = None
            cells = row.find_all('td')
            for cell in cells:
                if ammo_type is None:
                    ammo_type = cell.getText().rstrip('\n')
                    ballistics_data[ammo_caliber][ammo_type] = {}
                else:
                    ballistics_data[ammo_caliber][ammo_type][column_names[column_index]] = cell.getText().rstrip('\n')
                    column_index += 1
    else:
        skip_rows += 1

print(ballistics_data)
