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

driver.get("https://kenpom.com/")
time.sleep(3)

table = driver.find_element(By.ID, "ratings-table")
table_rows = table.find_elements(By.TAG_NAME, "tr")
table_head = table.find_element(By.CLASS_NAME, "thead2")

headers = table_head.find_elements(By.TAG_NAME, "th")
headers_text = [header.text for header in headers]
headers_text.insert(6,"R_ORtg")
headers_text.insert(8,"R_DRtg")
headers_text.insert(10,"R_Tempo")
headers_text.insert(12,"R_Luck")
headers_text.insert(14,"R_SOS_NetRTG")
headers_text.insert(16,"R_SOS_ORTG")
headers_text.insert(18,"R_SOS_DRtg")
headers_text.insert(20,"R_Non_Conf_SOS_NetRTG")
print(headers_text)

rows_data = []
for row in table_rows[1:]:
    cells = row.find_elements(By.TAG_NAME, "td")
    cells_data = [cell.text for cell in cells]
    rows_data.append(cells_data)

# Create a DataFrame
# Modify so St. becomes state
df = pd.DataFrame(rows_data, columns=headers_text)
df = df.dropna(axis=0, how='all')

df.to_csv("advanced_analytics_cbb.csv", index=False)
driver.quit()
print("Scraping is done")

print(headers_text)