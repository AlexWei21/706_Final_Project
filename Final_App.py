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
    df['Vaccinated_Percentage'] = df['People_fully_vaccinated'] / df['Population']

    df['Date'] = df['Date'].astype('datetime64[ns]')

    Vac_Death_df = df[['Country/Region', 'Date', 'Daily_Deaths', 'People_fully_vaccinated']]

    Vac_Death_df = Vac_Death_df.groupby(['Country/Region',pd.Grouper(key="Date", freq="1W")]).mean().reset_index()  

    Vac_Death_df = Vac_Death_df.melt(['Country/Region', 'Date'], var_name = 'Type', value_name = 'Number')

    return Vac_Death_df


df = load_data()

subset = df[df['Country/Region'] == 'US']

line = alt.Chart(subset).mark_line().encode(
    x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    y='Daily_Deaths:Q',
    color= alt.Color("Type"),
    tooltip=['Date','Number']
)


st.altair_chart(line, use_container_width=True)