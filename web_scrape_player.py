#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

option = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

# inputted player name
# PUT THIS BACK IN
# player = input("Enter player name: ")
# player_team = input("Enter player team: ")
# player_team = player_team.replace(" ", "-")
# player_team = player_team.lower()
# print(player_team)
# player = player.replace(" ", "-")

# for now save time
player = "miles-byrd"
player_team = "san-diego-state-aztecs"

# search for player
driver.get("https://www.espn.com/mens-college-basketball/teams")
time.sleep(3)
element = driver.find_element(By.XPATH, f"//a[contains(@href,'{player_team}')]")
element.click()
time.sleep(3)
element = driver.find_element(By.XPATH, "//a[@data-track-nav_item='statistics']")
element.click()
time.sleep(3)

# get the player
element = driver.find_element(By.XPATH, f"//a[contains(@href,'{player}')]")
element.click()
time.sleep(3)

# get the game log 
element = driver.find_element(By.XPATH, f"//a[contains(@href,'/gamelog/')]")
element.click()
time.sleep(3)

# Locate the table
table = driver.find_element(By.XPATH, "//table[@class='Table Table--align-right']")

# Get the headers
headers = table.find_elements(By.TAG_NAME, "th")
headers_text = [header.text for header in headers]
headers_text.append("Full_Team_Name")
print(headers_text)

# Extract rows 
rows = table.find_elements(By.TAG_NAME, "tr")
rows_data = []
for row in rows[1:]:
    cells = row.find_elements(By.TAG_NAME, "td")
    cells_data = [cell.text for cell in cells]
    try:
        a_element = row.find_element(By.TAG_NAME, "a")
        team_full_name = a_element.get_attribute("title")
        team_full_name = team_full_name.replace("Team - ", "")
    except:
        team_full_name = None
    cells_data.append(team_full_name)
    rows_data.append(cells_data)

# Data Frame Modifications
df = pd.DataFrame(rows_data, columns=headers_text)
df = df.dropna(subset=["MIN"])

df['Home'] = df['OPP'].apply(lambda row: 1 if "vs" in row else 0)
df['Away'] = df['OPP'].apply(lambda row: 1 if "@" in row else 0)


# Save the Dataframe to a csv file 
df.to_csv(f"{player}_game_log.csv", index=False)

driver.quit()






