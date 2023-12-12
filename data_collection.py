import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json


url = 'https://services1.arcgis.com/99lidPhWCzftIe9K/arcgis/rest/services/HousingUnitInventory/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json'

df = pd.read_csv('./Utah_Housing_Unit_Inventory.csv')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)

pre = driver.find_element(By.TAG_NAME,"pre").text
data = json.loads(pre)

df = pd.json_normalize(data['features'])

new_column_names = {col: col.replace('attributes.', '') for col in df.columns}
df.rename(columns=new_column_names, inplace=True)
df.set_index('OBJECTID', inplace=True)