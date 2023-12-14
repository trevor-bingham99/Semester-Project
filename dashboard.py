import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('Utah Housing Data Exploration')

df = pd.read_csv("./HousingData.csv")

st.text("This dashboard will walk through some visualization that I have made about Utah housing information. To start, we will take a look at the general distribution fo the data.")



slider_value = st.slider('Select a year range:', min_value=1860, max_value=2020, value=(1950,2000), step=1)
st.write('Your selected range:', slider_value)
