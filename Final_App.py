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

    # Vac_Death_df = Vac_Death_df.melt(['Country/Region', 'Date'], var_name = 'Type', value_name = 'Number')

    return Vac_Death_df


df = load_data()

subset = df[df['Country/Region'] == 'US']

base = alt.Chart(subset).encode(
    alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45))
)

line1 = base.mark_area(opacity = 0.3, color = '#57A44C' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('Daily_Deaths:Q',scale=alt.Scale(type='log', domainMin=0.005, clamp = True)),
    # color= alt.Color("Type"),
    tooltip=['Date','Daily_Deaths']
)

line2 = base.mark_line().encode(
    
    y= alt.Y('People_fully_vaccinated:Q'),
    # color= alt.Color("Type"),
    tooltip=['Date','People_fully_vaccinated']
)

combine = alt.layer(line1,line2).resolve_scale(
    y = 'independent'
)

st.altair_chart(combine, use_container_width=True)