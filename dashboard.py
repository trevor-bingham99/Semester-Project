import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('Utah Housing Data Exploration')

df = pd.read_csv("https://raw.githubusercontent.com/trevor-bingham99/Semester-Project/main/Utah_Housing_Unit_Inventory.csv")

st.write("This dashboard will walk through some visualization that I have made about Utah housing information, most of which is also found in a blog post [here](https://trevor-bingham99.github.io/2023/12/13/EDA.html), and you can find my repository with all the data [here](https://github.com/trevor-bingham99/Semester-Project). To start, we will take a look at the general distribution fo the data.")

hist = px.histogram(
    df[df['TOT_VALUE']<9000000],
    x='TOT_VALUE',
    title='Distribution of Total Values',
    nbins=50,  
    opacity=0.7
)
st.plotly_chart(hist)

st.write("For this chart, I have removed some of the more expensive houses, as there are just a few that are way higher than the rest and it makes it hard to see the majority of the values. But we can see most houses are between 200-400k in price, in total. The next thing we want to get a feel for is how many of each sub-type of dwelling was represented in the distribution, which we can see in the following chart.")

category_counts = df['SUBTYPE'].value_counts()

filtered_counts = category_counts[category_counts != 0]

bar = px.bar(x=filtered_counts.index, y=filtered_counts.values, text=filtered_counts.values,color=filtered_counts.index,title='Counts of Each Housing Subtype')
st.plotly_chart(bar)

st.write("Somewhat expectedly, the overwhelming majority of dwellings were single family dwellings, as that is what is most prevalent, followed by apartments and townhouse which are also rising in popularity it feels like. To start looking at more variables, I wanted to get a feel for if any had a higher correlation with each other, so I made the following heatmap to explore this.")

variables = st.multiselect(
    'What variables do you want to include?',
    ['UNIT_ID','IS_OUG','UNIT_COUNT','DUA','ACRES','TOT_BD_FT2','TOT_VALUE','APX_BLT_YR','BLT_DECADE','Shape__Area','Shape__Length'],
    ['TOT_VALUE','TOT_BD_FT2','APX_BLT_YR'])

heatmap = px.imshow(df[variables].corr(numeric_only=True).round(2),
          text_auto=True,
          title='Correlation Heatmap')
st.plotly_chart(heatmap,use_container_width=True)

st.write("You can explore a lot of the correlations here, but one thing this made me want to look a bit into how the different types of dwellings might impact things like acres of the property, so I created a scatterplot that shows how the amount of acres and the price impact each other, colored by their type.")

selected_categories = st.sidebar.multiselect('Select Sub-Types', df['SUBTYPE'].unique())

scat3 = px.scatter(df[(df['APX_BLT_YR']!=0) & (df['TOT_VALUE']<300000000) & (df['ACRES']<500) & (df['SUBTYPE'].isin(selected_categories))], x='ACRES', y='TOT_VALUE', color='SUBTYPE', title='Acres of Land vs Total Value',opacity=.5)
st.plotly_chart(scat3)

st.write("I found this visualization to highlight some very interesting things. We see a lot of the dwellings of the same types clusted around each other, following a similar pattern based on the type of dwelling, which does follow what I would think. It is much easier for a single family house to have more land without impacting price too much, especially compared to apartment building or condos, which seem to have steep increaes in price for little increases in acreage. This then lead me to consider what the relationship between price and the square footage of the house.")

scat4 = px.scatter(df[(df['APX_BLT_YR']!=0) & (df['TOT_BD_FT2']<9000000)], x='TOT_VALUE', y='TOT_BD_FT2', title='Price vs Square Footage',opacity=.5)
st.plotly_chart(scat4)

st.write("This did follow what I would think, that there is a pretty clear relationship between the price of the hosue, and how much square feet the house has. In general, there is very little variance, so the type of dwelling or other factors such as location don't seem to be very relevant to this relationship. One final aspect I wanted to explore some was if there was any relation between when the house was built and its price.")

fig = px.scatter(df[(df['APX_BLT_YR']!=0)], x='APX_BLT_YR', y='TOT_VALUE', color='SUBTYPE', title='Year Built vs Price',opacity=.5)
st.plotly_chart(fig)

st.write("Since it seems that houses of higher values only seem to be coming the last few decades, I want to look into if when the houses were built will have any effect on this distribution of prices.")

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

st.write("")