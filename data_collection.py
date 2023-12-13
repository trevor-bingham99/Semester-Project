import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np
import time
from itertools import groupby
import plotly.express as px


def scroll(driver, timeout):
    # get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        for i in range(timeout):
            # scroll down
            driver.find_element(By.XPATH,"/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div/div[2]/div/table").send_keys(Keys.END)

            # wait for page to load
            time.sleep(1)

        # get new scroll height and compare to last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

#url = 'https://services1.arcgis.com/99lidPhWCzftIe9K/arcgis/rest/services/HousingUnitInventory/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json'

df = pd.read_csv('./Utah_Housing_Unit_Inventory.csv')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


pre = driver.find_element(By.TAG_NAME,"pre").text
data = json.loads(pre)

df = pd.json_normalize(data['features'])

new_column_names = {col: col.replace('attributes.', '') for col in df.columns}
df.rename(columns=new_column_names, inplace=True)
df.set_index('OBJECTID', inplace=True)

url1= 'https://opendata.gis.utah.gov/datasets/utah::utah-housing-unit-inventory/about'

driver.get(url1)

def get_all_rows(driver, table_locator):
    # Scroll to the bottom of the page to ensure all rows are loaded
    last_row_count = 0

    while True:
        # Record the current number of rows
        current_row_count = len(driver.find_elements(By.XPATH, table_locator + "//tr"))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for a short time to let new rows load
        scroll(driver,10)

        # Get the new number of rows
        new_row_count = len(driver.find_elements(By.XPATH, table_locator + "//tr"))

        # If the number of rows hasn't increased, break the loop
        if new_row_count == current_row_count or new_row_count==10000:
            break

        # Update the last row count
        last_row_count = new_row_count

    html = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table in the parsed HTML
    table = soup.find('table')

    # Check if the table was found
    if table:
        # Extract all rows from the table
        all_rows = table.find_all('tr')
        return all_rows
    else:
        print("Table not found.")
        return []    


driver.find_element(By.ID,"ember99").click()

driver.find_element(By.ID,"ember241-title").click()
driver.find_element(By.ID,"ember241-title").click()
# Replace with the correct XPath or other locator for your table
table_locator = "/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div/div[2]/div/table"

all_rows = get_all_rows(driver, table_locator)

driver.close()

header_columns = [span.get_text(strip=True) for span in all_rows[0].find_all('span', {'role': 'button'})]

# Initialize an empty list to store row data
all_rows_data = []

# Iterate through each row
for row_html in all_rows:
    # Extract data from each cell in the row
    data = [cell.get_text(strip=True) for cell in row_html.find_all('td', {'role': 'gridcell'})]
    
    # Create a dictionary for the row
    row_dict = dict(zip(header_columns, data))
    
    # Append the row data to the list
    all_rows_data.append(row_dict)

# Create a DataFrame from the list of row data
df1 = pd.DataFrame(all_rows_data)
df1.dropna(inplace=True)

combined_df = pd.concat([df, df1], ignore_index=True)
combined_df.drop_duplicates(subset='UNIT_ID', keep='first',inplace=True)

columns_to_convert_to_float = ['UNIT_ID', 'UNIT_COUNT', 'DUA','ACRES','TOT_BD_FT2','TOT_VALUE','APX_BLT_YR','BLT_DECADE','Shape__Area','Shape__Length','IS_OUG']

# Convert specified columns to int
combined_df[columns_to_convert_to_float] = combined_df[columns_to_convert_to_float].replace(",","",regex=True).replace('', 0).astype(float)

fig = px.scatter(combined_df, x='TOT_VALUE', y='TOT_BD_FT2', color='SUBTYPE', title='Value vs Square Footage',opacity=.5)
fig.show()

fig = px.scatter(combined_df[(combined_df['APX_BLT_YR']!=0) & (combined_df['TOT_BD_FT2']<9000000)], x='APX_BLT_YR', y='TOT_BD_FT2', color='SUBTYPE', title='Decade Built vs Square Footage',opacity=.5)
fig.show()

category_counts = combined_df['SUBTYPE'].value_counts()

# Exclude categories with a count of 0
filtered_counts = category_counts[category_counts != 0]

# Create the bar chart with the filtered counts
fig = px.bar(x=filtered_counts.index, y=filtered_counts.values, text=filtered_counts.values,color=filtered_counts.index,title='Counts of Each Housing Subtype')
fig.show()

combined_df.to_csv('./HousingData.csv')