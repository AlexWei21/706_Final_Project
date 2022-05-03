import altair as alt
import pandas as pd
import streamlit as st

import geopandas as gpd
alt.data_transformers.enable('default', max_rows=None)
import numpy as np
import matplotlib.pyplot as plt

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

    Vac_Death_df = df[['Country/Region', 'Continent', 'Date','Daily_Deaths', 'Daily_Cases','People_fully_vaccinated', 'Population', 'Vaccinated_Percentage']]

    Vac_Death_df = Vac_Death_df.groupby(['Country/Region','Continent', pd.Grouper(key="Date", freq="1W")]).mean().reset_index()  

    # Vac_Death_df = Vac_Death_df.melt(['Country/Region', 'Date'], var_name = 'Type', value_name = 'Number')

    return Vac_Death_df


df = load_data()

subset = df

global_subset = df

# st.write(global_subset)

global_daily_death = global_subset.groupby(['Date']).sum().reset_index()[['Date','Daily_Deaths']]
global_daily_case = global_subset.groupby(['Date']).sum().reset_index()[['Date','Daily_Cases']]

global_subset = global_subset[global_subset['Country/Region'] == 'World']

# st.write(global_daily_case)
# st.write(global_subset)

global_death_case = global_daily_case.merge(how = 'left', on = 'Date', right=global_daily_death)

#st.write(global_death_case)

global_subset['Global_Vaccination_Rate'] = global_subset['People_fully_vaccinated']/ 7868872451

global_subset = global_subset.merge(how = 'right', on = 'Date', right= global_death_case)

global_subset['Country/Region'] = global_subset['Country/Region'].fillna('World')

# st.write(global_subset)

W_base = alt.Chart(global_subset).encode(
    alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45))
)

W_d_area = W_base.mark_area(opacity = 0.5, color = '#FFA500' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('Daily_Deaths_y:Q', scale=alt.Scale(domainMin=0)),
    # color= alt.Color("Type"),
    tooltip=['Date','Daily_Deaths_y']
)

W_vaccine_line = W_base.mark_line(color = '#A9A9A9').encode( 
    y= alt.Y('Global_Vaccination_Rate', axis=alt.Axis(format = '%'), scale=alt.Scale(domain=(0,1))),
    # color= alt.Color("Type"),
    tooltip=['Date','Global_Vaccination_Rate']
)

W_c_area = W_base.mark_area(opacity = 0.3, color = '#0000FF' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('Daily_Cases_y:Q',scale=alt.Scale(domainMin=0)),
    # color= alt.Color("Type"),
    tooltip=['Date','Daily_Cases_y']
)

W_combine1 = alt.layer(W_d_area,W_vaccine_line).resolve_scale(
    y = 'independent'
).properties(
    title='Global Vaccination Status and Death number'
)

W_combine2 = alt.layer(W_c_area,W_vaccine_line).resolve_scale(
    y = 'independent'
).properties(
    title='Global Vaccination Status and Case number'
)

st.title('World and Country-wide Covid-19 Situation and Vaccination Status Overview')
st.write("## Global Covid-19 Information")

st.altair_chart(W_combine1, use_container_width=True)

st.altair_chart(W_combine2, use_container_width=True)

st.write("## Covid-19 Information for a selected continent and country")

continent = st.multiselect('Continent',['Asia','European','Africa','North America','South America','Oceania'],['North America'])

subset = subset[subset["Continent"].isin(continent)]

rank_data = subset[subset['Date'] == max(subset['Date'])]

# st.write(rank_data)

# rank_data = rank_data.sort_values(by = ['Vaccinated_Percentage'])

# st.write(rank_data)

bars = alt.Chart(rank_data).mark_bar().encode(
    x = alt.X('Vaccinated_Percentage:Q',axis=alt.Axis(format = '%'), scale=alt.Scale(domain=(0,1))),
    y = alt.Y('Country/Region:O', sort = '-x'),
    tooltip = ['Country/Region','Vaccinated_Percentage']
).properties(
    title='Vaccination ranking for selected continents'
)

st.write('### Rank of the Vaccination Rate of selected Continent')

st.altair_chart(bars, use_container_width=True)

country = st.selectbox('Country', options = subset['Country/Region'].unique())

st.write('### Covid-19 and Vaccination Status in Selected Country')

subset = subset[subset['Country/Region'] == country]

base = alt.Chart(subset).encode(
    alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45))
)

d_area = base.mark_area(opacity = 0.5, color = '#FFA500' ).encode(
    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
    alt.Y('Daily_Deaths:Q', scale=alt.Scale(domainMin=0)),
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
    alt.Y('Daily_Cases:Q',scale=alt.Scale(domainMin=0)),
    # color= alt.Color("Type"),
    tooltip=['Date','Daily_Cases']
)


combine1 = alt.layer(d_area,vaccine_line).resolve_scale(
    y = 'independent'
).properties(
    title=f'Vaccination Status and Death number for {country}'
)

st.altair_chart(combine1, use_container_width=True)

combine2 = alt.layer(c_area,vaccine_line).resolve_scale(
    y = 'independent'
).properties(
    title=f'Global Vaccination Status and Case number for {country}'
)

st.altair_chart(combine2, use_container_width=True)

st.write("## Detailed Vaccination Status of selected country compared to Global situation")

def load_vac_data():
    
    df = pd.read_csv('https://raw.githubusercontent.com/AlexWei21/706_Final_Project/6f129af67cfa5d50a5cb7ced94095d3639e14fda/Covid_19_Full_Data.csv')

    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['Month'] = pd.DatetimeIndex(df['Date']).month
    df['Day'] = pd.DatetimeIndex(df['Date']).day

    df = df[['Country/Region','Continent','Year','Month','People_partially_vaccinated','People_fully_vaccinated','Population']]
    df['People_not_vaccinated'] = df['Population'] - df['People_partially_vaccinated'] - df['People_fully_vaccinated']

    df = df.drop(['Population'], axis=1)

    df = df.melt(['Country/Region','Continent', 'Year','Month'], var_name = 'Status', value_name = 'Number')

    return df

vac_data = load_vac_data()
vac_subset = vac_data

# st.write(vac_subset)
# st.write(continent)

year = st.selectbox('Year',(2020,2021,2022), index=1)
month = st.selectbox('Month',(1,2,3,4,5,6,7,8,9,10,11,12), index = 6)

vac_subset = vac_subset[(vac_subset['Year'] == year) & (vac_subset['Month'] == month) ]


donut1 = alt.Chart(vac_subset).mark_arc(innerRadius=50, outerRadius=90).encode(
    theta = 'sum(Number):Q',
    color = 'Status',
).properties(
    title=f'Vaccination Status globally {year} . {month}',
    width = 500
)

vac_subset = vac_subset[vac_subset['Continent'].isin(continent)]

donut3 = alt.Chart(vac_subset).mark_arc(innerRadius=50, outerRadius=90).encode(
    theta = 'sum(Number):Q',
    color = 'Status',
).properties(
    title=f'Vaccination Status in selected continents {year} . {month}',
    width = 500
)

vac_subset = vac_subset[vac_subset['Country/Region'] == country]

donut2 = alt.Chart(vac_subset).mark_arc(innerRadius=50, outerRadius=90).encode(
    theta = 'sum(Number):Q',
    color = 'Status',
).properties(
    title=f'Vaccination Status in {country} {year} . {month}',
    width = 500
)


st.altair_chart(donut2)
st.altair_chart(donut3)
st.altair_chart(donut1)


def load_data():
    gob_cases = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    glob_recovered = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    glob_deaths = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    glob_vacc = pd.read_csv(
        "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv")
    glob_vac_admin = pd.read_csv(
        "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_doses_admin_global.csv")

    return glob_cases, glob_recovered, glob_deaths, glob_vacc, glob_vac_admin

glob_cases, glob_recovered, glob_deaths, glob_vacc, glob_vac_admin = load_data()



st.write("## Data Wrangling")

# Changing the different names for the US into a single name "US"
glob_vacc['Country_Region'] = glob_vacc['Country_Region'].replace(['US (Aggregate)', "United States of America"],'US')
glob_cases['Country/Region'] = glob_cases['Country/Region'].replace(['US (Aggregate)', "United States of America"],'US')
glob_recovered['Country/Region'] = glob_recovered['Country/Region'].replace(['US (Aggregate)', "United States of America"],'US')
glob_deaths['Country/Region'] = glob_deaths['Country/Region'].replace(['US (Aggregate)', "United States of America"],'US')

#Melting the deaths dataset
deaths = pd.melt(glob_deaths,
                 ["Province/State", "Country/Region", "Lat", "Long"],
                 var_name="Date",
                 value_name="Deaths")

deaths = deaths.drop(['Province/State','Lat','Long'],axis=1)
deaths = deaths.groupby(['Country/Region','Date']).sum().reset_index()
deaths['Date'] = pd.to_datetime(deaths['Date'], errors='coerce')
deaths = deaths.sort_values(by=['Country/Region','Date'])
deaths

# Melting the recovery datasets
recovered = pd.melt(glob_recovered,
                    ["Province/State", "Country/Region", "Lat", "Long"],
                    var_name="Date",
                    value_name="Recovered")

recovered = recovered.drop(['Province/State','Lat','Long'], axis=1)
recovered = recovered.groupby(['Country/Region','Date']).sum().reset_index()
recovered['Date'] = pd.to_datetime(recovered['Date'], errors='coerce')
recovered = recovered.sort_values(by=['Country/Region','Date'])
recovered

# Joining Deaths and Recovery datasets
data = deaths.merge(how = 'outer', right=recovered, on=['Country/Region', 'Date'])

# Melting the cases dataset
cases = pd.melt(glob_cases,
                ["Province/State", "Country/Region", "Lat", "Long"],
                var_name="Date",
                value_name="Cases")

cases = cases.drop(['Province/State','Lat','Long'], axis=1)
cases = cases.groupby(['Country/Region','Date']).sum().reset_index()
cases['Date'] = pd.to_datetime(cases['Date'], errors='coerce')
cases = cases.sort_values(by=['Country/Region','Date'])

# Merge Cases with previous Merge
data = data.merge(how = 'outer', right=cases, on=['Country/Region', 'Date'])

# Renaming and subseting the Vaccination dataset
vacc_data = glob_vacc[['Country_Region','Date','Doses_admin','People_partially_vaccinated','People_fully_vaccinated']]
vacc_data = vacc_data.rename(columns={'Country_Region': 'Country/Region'})
vacc_data['Date'] =  pd.to_datetime(vacc_data['Date'], errors='coerce')

# Merge Vaccination dataset with previous merge
full_data = data.merge(right = vacc_data, on = ['Country/Region', 'Date'], how = 'outer')

# Splitting dates by day month and year
full_data['Year'] = pd.DatetimeIndex(full_data['Date']).year
full_data['Month'] = pd.DatetimeIndex(full_data['Date']).month
full_data['Day'] = pd.DatetimeIndex(full_data['Date']).day

#Importing the world dataset in geopandas format
world=gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world=world.rename(columns={"name": "Country/Region"}) # Renaiming the column name into Country/Region in order to index it while joining the datasets
world['Country/Region'] = world['Country/Region'].replace(['United States of America'],'US')
world

#Creating a multiselect for country
Country=st.multiselect("Select the Countries you want to display", options=np.unique(list(Y["Country/Region"])))
Y=Y[(Y["Country/Region"]==country)]
# Creating the Chloropeth map for Deaths
# Create a drop-down quarter selector
Y = Y.astype({"Quarter": str}, errors="raise")  # Forcing the Quarter column into a string format
quarter = Y['Quarter'].unique()
Q_dropdown = alt.binding_select(options=quarter)
Q_select = alt.selection_single(bind=Q_dropdown, fields=["Quarter"])

# Creating a geopandas dataframe

Y = Y.merge(world, on="Country/Region", how="left")
# Y['Death_Ratio']= Y['Deaths']/Y['pop_est']
geo = gpd.GeoDataFrame(Y)  # Creating the geopandas dataframe
# geo=gpd.GeoDataFrame(Full_data) # Creating the geopandas dataframe
# Displaying the map chart
base = alt.Chart(geo).mark_geoshape().project().encode(color=alt.Color('Deaths'),
                                                       tooltip=['Country/Region', "Deaths", "Cases", "Recovered"]
                                                       ).properties(
    width=500,
    height=400).add_selection(Q_select).transform_filter(Q_select).properties(title="World Chloropeth of Covid Deaths")

st.altair_chart(base)

# Creating the Chloropeth map for Cases

map_cases = alt.Chart(geo).mark_geoshape().project().encode(color=alt.Color('Cases'),
                                                            tooltip=['Country/Region', "Deaths", "Cases", "Recovered"]
                                                            ).properties(
    width=500,
    height=400).add_selection(Q_select).transform_filter(Q_select).properties(title="World Chloropeth of Covid Deaths")

map_cases

st.altair_chart(map_cases)