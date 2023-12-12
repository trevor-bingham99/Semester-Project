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


#pre = driver.find_element(By.TAG_NAME,"pre").text
#data = json.loads(pre)

#df = pd.json_normalize(data['features'])

#new_column_names = {col: col.replace('attributes.', '') for col in df.columns}
#df.rename(columns=new_column_names, inplace=True)
#df.set_index('OBJECTID', inplace=True)

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
        if new_row_count == current_row_count:
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

# Now 'all_rows' contains all the rows in the table
len(all_rows)