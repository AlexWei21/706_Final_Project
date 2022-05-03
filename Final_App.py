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

continent = st.multiselect('Continent',['Asia','European','Africa','North America','South America','Oceania'],['North America'])

subset = subset[subset["Continent"].isin(continent)]

country = st.selectbox('Country', options = subset['Country/Region'].unique() )

subset = subset[subset['Country/Region'] == country]

base = alt.Chart(subset).encode(
    alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45))
)

d_area = base.mark_area(opacity = 0.5, color = '#FFA500' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('Daily_Deaths:Q'),
    # color= alt.Color("Type"),
    tooltip=['Date','Daily_Deaths']
)

vaccine_line = base.mark_line(color = '#A9A9A9').encode( 
    y= alt.Y('Vaccinated_Percentage', axis=alt.Axis(format = '%'), scale=alt.Scale(domain=(0,1))),
    # color= alt.Color("Type"),
    tooltip=['Date','Vaccinated_Percentage']
)

c_area = base.mark_area(opacity = 0.3, color = '#0000FF' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('Daily_Cases:Q'),
    # color= alt.Color("Type"),
    tooltip=['Date','Daily_Cases']
)


combine1 = alt.layer(d_area,vaccine_line).resolve_scale(
    y = 'independent'
)

st.altair_chart(combine1, use_container_width=True)

combine2 = alt.layer(c_area,vaccine_line).resolve_scale(
    y = 'independent'
)

st.altair_chart(combine2, use_container_width=True)

def load_vac_data():
    
    df = pd.read_csv('https://raw.githubusercontent.com/AlexWei21/706_Final_Project/6f129af67cfa5d50a5cb7ced94095d3639e14fda/Covid_19_Full_Data.csv')

    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['Month'] = pd.DatetimeIndex(df['Date']).month
    df['Day'] = pd.DatetimeIndex(df['Date']).day

    df = df[['Country/Region','Year','Month','People_partially_vaccinated','People_fully_vaccinated','Population']]
    df['People_not_vaccinated'] = df['Population'] - df['People_partially_vaccinated'] - df['People_fully_vaccinated']

    df = df.melt(['Country/Region', 'Year','Month'], var_name = 'Status', value_name = 'Number')

    return df

vac_data = load_vac_data()

year = st.selectbox('Year',('2020','2021','2022'))
month = st.selectbox('Month',('1','2','3','4','5','6','7','8','9','10','11','12'))
vac_subset = vac_data[(vac_data['Year'] == year) & (vac_data['Month'] == month)]
vac_subset = vac_subset[vac_subset['Country/Region'] == country]

donut1 = alt.Chart(vac_subset).mark_arc(innerRadius=50, outerRadius=90).encode(
    theta = 'sum(Number):Q',
    color = 'Status',
)

st.altair_chart(donut1)



