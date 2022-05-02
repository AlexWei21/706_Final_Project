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

    df.loc[df['Country/Region'] == 'US', 'Continent'] = 'North America'

    Vac_Death_df = df[['Country/Region', 'Continent', 'Date', 'Daily_Deaths', 'Daily_Cases', 'Vaccinated_Percentage']]

    Vac_Death_df = Vac_Death_df.groupby(['Country/Region','Continent', pd.Grouper(key="Date", freq="1W")]).mean().reset_index()  

    # Vac_Death_df = Vac_Death_df.melt(['Country/Region', 'Date'], var_name = 'Type', value_name = 'Number')

    return Vac_Death_df


df = load_data()

subset = df

continent = st.multiselect('Continent',[
    'Asia',
    'Europe',
    'Africa',
    'North America',
    'South America',
    'Oceania'
    ],[
    'Asia',
    'Europe',
    'Africa',
    'North America',
    'South America',
    'Oceania'
    ]
)
subset = subset[subset['Continent'] == continent]

base = alt.Chart(subset).encode(
    alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45))
)

d_area = base.mark_area(opacity = 0.3, color = '#FFA500' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('sum_Daily_Deaths:Q'),
    # color= alt.Color("Type"),
    tooltip=['Date','sum_Daily_Deaths']
).transform_aggregate(
    sum_Daily_Deaths = 'sum(Daily_Deaths)',
    groupby=['Date']
)

vaccine_line = base.mark_line(color = '#A9A9A9').encode(
    
    y= alt.Y('mean(Vaccinated_Percentage)', axis=alt.Axis(format = '%'), scale=alt.Scale(domain=(0,1))),
    # color= alt.Color("Type"),
    tooltip=['Date','mean_Vaccinated_Percentage']
).transform_aggregate(
    mean_Vaccinated_Percentage = 'mean(Vaccinated_Percentage)',
    groupby=['Date']
)

c_area = base.mark_area(opacity = 0.3, color = '#0000FF' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('sum_Daily_Cases:Q'),
    # color= alt.Color("Type"),
    tooltip=['Date','sum_Daily_Cases']
).transform_aggregate(
    sum_Daily_Cases = 'sum(Daily_Cases)',
    groupby=['Date']
)


combine1 = alt.layer(d_area,vaccine_line).resolve_scale(
    y = 'independent'
)

st.altair_chart(combine1, use_container_width=True)

combine2 = alt.layer(c_area,vaccine_line).resolve_scale(
    y = 'independent'
)

st.altair_chart(combine2, use_container_width=True)