from curses.ascii import US
import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

@st.cache

def load_data():
    ## {{ CODE HERE }} ##
    df = pd.read_csv('https://raw.githubusercontent.com/AlexWei21/706_Final_Project/6f129af67cfa5d50a5cb7ced94095d3639e14fda/Covid_19_Full_Data.csv')
    df['Death_per_million'] = df['Deaths'] / df['Population']
    df['Cases_per_million'] = df['Cases'] / df['Population']
    df['Recovered_per_million'] = df['Recovered'] / df['Population']
    df['Population_Density'] = df['Population'] / df['Area (sq_km)']
    df['Daily_Death'] = df.groupby(['Country/Region'])['Deaths'].diff()
    return df


df = load_data()
# df

st.write('## Cases and Death of Covid 19 with Vaccine Data')

### Choosing Time Period
# date_slider = alt.binding_range(min=min(df['Date']), max=max(df['Date']), step=30)

subset = df[df['Country/Region'] == 'US']

line = alt.Chart(subset).mark_dot().encode(
    x = 'Date:T',
    y = 'Daily_Death:Q'
    )
    

st.altair_chart(line, use_container_width=True)