from curses.ascii import US
import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

@st.cache

def load_data():
    ## {{ CODE HERE }} ##
    df = pd.read_csv('https://raw.githubusercontent.com/AlexWei21/706_Final_Project/6f129af67cfa5d50a5cb7ced94095d3639e14fda/Covid_19_Full_Data.csv')
        
    df['Population_Density'] = df['Population'] / df['Area (sq_km)']

    df['Daily_Deaths'] = df.groupby(['Country/Region'])['Deaths'].diff()
    df['Daily_Cases'] = df.groupby(['Country/Region'])['Cases'].diff()

    df['Daily_Death_per_million'] = df['Daily_Deaths'] * 1000000 / df['Population']
    df['Daily_Cases_per_million'] = df['Daily_Cases'] * 1000000 / df['Population']

    df['Date'] = df['Date'].astype('datetime64[ns]')

    Case_Death = df[['Country/Region', 'Date', 'Daily_Deaths', 'Daily_Cases', 'Daily_Death_per_million', 'Daily_Cases_per_million']]

    Case_Death = Case_Death.groupby(['Country/Region',pd.Grouper(key="Date", freq="1W")]).mean().reset_index()    

    return Case_Death


df = load_data()

subset = df[df['Country/Region'] == 'US']

line = alt.Chart(subset).mark_line().encode(
    x='Date:T',
    y='Daily_Deaths',
    # color= alt.Color("Rate", title = "Log of Motality rate per 100k", scale=alt.Scale(type='log', domain=(0.005, 1), clamp = True)),
    # tooltip=[""]
)

st.altair_chart(line, use_container_width=True)