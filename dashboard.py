import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('Utah Housing Data Exploration')

df = pd.read_csv("/Users/trevorbingham/Documents/Classes/STAT386/Semester-Project/Utah_Housing_Unit_Inventory.csv")

st.markdown("This dashboard will walk through some visualization that I have made about Utah housing information, most of which is also found in a blog post [here](https://trevor-bingham99.github.io/2023/12/13/EDA.html). To start, we will take a look at the general distribution fo the data.")

hist = px.histogram(
    df[df['TOT_VALUE']<9000000],
    x='TOT_VALUE',
    title='Distribution of Total Values',
    nbins=50,  
    opacity=0.7
)
st.plotly_chart(hist)

st.markdown("For this chart, I have removed some of the more expensive houses, as there are just a few that are way higher than the rest and it makes it hard to see the majority of the values. But we can see most houses are between 200-400k in price, in total. The next thing we want to get a feel for is how many of each sub-type of dwelling was represented in the distribution, which we can see in the following chart.")

category_counts = df['SUBTYPE'].value_counts()

filtered_counts = category_counts[category_counts != 0]

bar = px.bar(x=filtered_counts.index, y=filtered_counts.values, text=filtered_counts.values,color=filtered_counts.index,title='Counts of Each Housing Subtype')
st.plotly_chart(bar)

st.markdown("Somewhat expectedly, the overwhelming majority of dwellings were single family dwellings, as that is what is most prevalent, followed by apartments and townhouse which are also rising in popularity it feels like. To start looking at more variables, I wanted to get a feel for if any had a higher correlation with each other, so I made the following heatmap to explore this.")

variables = st.multiselect(
    'What variables do you want to include?',
    ['UNIT_ID','IS_OUG','UNIT_COUNT','DUA','ACRES','TOT_BD_FT2','TOT_VALUE','APX_BLT_YR','BLT_DECADE','Shape__Area','Shape__Length'],
    ['TOT_VALUE','TOT_BD_FT2','APX_BLT_YR'])

heatmap = px.imshow(df[variables].corr(numeric_only=True).round(2),
          text_auto=True,
          title='Correlation Heatmap')
st.plotly_chart(heatmap,use_container_width=True)

st.markdown(" Next we want to look into if when the houses were built will have any effect on this distribution of prices.")

slider_value = st.slider('Select a year range:', min_value=1860, max_value=2020, value=(1950,2000), step=1)
st.write('Your selected range:', slider_value)


hist = px.histogram(
    df[(df['TOT_VALUE']<9000000) & (df['APX_BLT_YR'] > slider_value[0]) & (df['APX_BLT_YR'] < slider_value[1])],
    x='TOT_VALUE',
    title='Distribution of Total Values',
    nbins=50,  
    opacity=0.7
)
st.plotly_chart(hist)

st.markdown("")