import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=43.1152&lon=-89.6422#.Ye7hNvtMHJE")
soup = BeautifulSoup(page.content, 'html.parser')
currentConditions_tableData = []

# location, current temp and sky conditions are located in a separate section of HTML
# they will need be added to currentConditions_tableData
currentConditions = soup.find(id="current-conditions")
currentConditions_location = currentConditions.find('h2', class_="panel-title").get_text()
currentConditions_temp = currentConditions.find(class_="myforecast-current-lrg").get_text()
currentConditions_sky = currentConditions.find(class_="myforecast-current").get_text()
currentConditions_detail = currentConditions.find(id="current_conditions_detail")


# collect current conditions table and populate currentConditions_tableData
currentConditions_table = currentConditions_detail.find("table")
rows = currentConditions_table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    currentConditions_tableData.append([ele for ele in cols if ele]) # Get rid of empty values
currentConditions_tableData.insert(0,["Current Temp", currentConditions_temp])
currentConditions_tableData.append(["Sky Conditions", currentConditions_sky])
currentConditions_tableFormatted = pd.DataFrame(currentConditions_tableData, columns=currentConditions_tableData)

# display the current weather conditions
print("Current Conditions at: " + currentConditions_location)
print(currentConditions_tableFormatted.to_string(index=False,header=False))
