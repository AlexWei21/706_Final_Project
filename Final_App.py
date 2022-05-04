import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

@st.cache

def load_data():
    
    df = pd.read_csv('https://raw.githubusercontent.com/AlexWei21/706_Final_Project/6f129af67cfa5d50a5cb7ced94095d3639e14fda/Covid_19_Full_Data.csv')
        
    df['Population_Density'] = df['Population'] / df['Area (sq_km)']

    df['Daily_Deaths'] = df.groupby(['Country/Region'])['Deaths'].diff()
    df['Daily_Cases'] = df.groupby(['Country/Region'])['Cases'].diff()

    df['Daily_Death_per_million'] = df['Daily_Deaths'] * 1000000 / df['Population']
    df['Daily_Cases_per_million'] = df['Daily_Cases'] * 1000000 / df['Population']
    df['Vaccinated_Percentage'] = df['People_fully_vaccinated'] / df['Population']

    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['Month'] = pd.DatetimeIndex(df['Date']).month
    df['Day'] = pd.DatetimeIndex(df['Date']).day

    df['Date'] = df['Date'].astype('datetime64[ns]')

    df.loc[df['Country/Region'] == 'US', 'Continent'] = 'North America'

    Vac_Death_df = df[['Country/Region', 'Continent', 'Date','Daily_Deaths', 'Daily_Cases','People_fully_vaccinated', 'Population', 'Vaccinated_Percentage']]

    Vac_Death_df = Vac_Death_df.groupby(['Country/Region','Continent', pd.Grouper(key="Date", freq="1W")]).mean().reset_index()  

    # Vac_Death_df = Vac_Death_df.melt(['Country/Region', 'Date'], var_name = 'Type', value_name = 'Number')

    return Vac_Death_df


df = load_data()

# merge country codes
subset = df

#.merge(country_df[['Country','country-code']], how = 'left', on = 'Country')

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

## st.title('World and Country-wide Covid-19 Pandemic and Vaccination Status Overview')
## st.write("## Global Covid-19 Trend")

## st.altair_chart(W_combine1, use_container_width=True)

## st.altair_chart(W_combine2, use_container_width=True)

## st.write("## Covid-19 Trend for a selected continent and country")

##continent = st.multiselect('Continent',['Asia','European','Africa','North America','South America','Oceania'],['North America'])

##subset = subset[subset["Continent"].isin(continent)]

##rank_data = subset[subset['Date'] == max(subset['Date'])]

# st.write(rank_data)

# rank_data = rank_data.sort_values(by = ['Vaccinated_Percentage'])

# st.write(rank_data)

##bars = alt.Chart(rank_data).mark_bar().encode(
##    x = alt.X('Vaccinated_Percentage:Q',axis=alt.Axis(format = '%'), scale=alt.Scale(domain=(0,1))),
##    y = alt.Y('Country/Region:O', sort = '-x'),
##    tooltip = ['Country/Region','Vaccinated_Percentage']
##).properties(
##    title='Vaccination ranking for selected continents'
##)

## st.write('### Rank of the Vaccination Rate of selected Continent')

## st.altair_chart(bars, use_container_width=True)

## country = st.selectbox('Country', options = subset['Country/Region'].unique())

## st.write('### Covid-19 Cases and Deaths and Vaccination Status in Selected Country')

##subset = subset[subset['Country/Region'] == country]

##base = alt.Chart(subset).encode(
##    alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45))
##)

##d_area = base.mark_area(opacity = 0.5, color = '#FFA500' ).encode(
##    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
##    alt.Y('Daily_Deaths:Q', scale=alt.Scale(domainMin=0)),
##    # color= alt.Color("Type"),
##    tooltip=['Date','Daily_Deaths']
##)

##vaccine_line = base.mark_line(color = '#A9A9A9').encode( 
##    y= alt.Y('Vaccinated_Percentage', axis=alt.Axis(format = '%'), scale=alt.Scale(domain=(0,1))),
##    # color= alt.Color("Type"),
##    tooltip=['Date','Vaccinated_Percentage']
##)

##c_area = base.mark_area(opacity = 0.3, color = '#0000FF' ).encode(
##    # x= alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45)),
##    alt.Y('Daily_Cases:Q',scale=alt.Scale(domainMin=0)),
##    # color= alt.Color("Type"),
##    tooltip=['Date','Daily_Cases']
##)


##combine1 = alt.layer(d_area,vaccine_line).resolve_scale(
##    y = 'independent'
##).properties(
##    title=f'Vaccination Status and Death number for {country}'
##)

##st.altair_chart(combine1, use_container_width=True)

##combine2 = alt.layer(c_area,vaccine_line).resolve_scale(
##    y = 'independent'
##).properties(
##    title=f'Vaccination Status and Case number for {country}'
##)

##st.altair_chart(combine2, use_container_width=True)

##st.write("## Detailed Vaccination Status of selected country compared to Global situation")

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

##year = st.selectbox('Year',(2020,2021,2022), index=1)
##month = st.selectbox('Month',(1,2,3,4,5,6,7,8,9,10,11,12), index = 6)

##vac_subset = vac_subset[(vac_subset['Year'] == year) & (vac_subset['Month'] == month) ]


##donut1 = alt.Chart(vac_subset).mark_arc(innerRadius=50, outerRadius=90).encode(
##    theta = 'sum(Number):Q',
##    color = 'Status',
##).properties(
##    title=f'Vaccination Status globally {year} . {month}',
##    width = 500
##)

##vac_subset = vac_subset[vac_subset['Continent'].isin(continent)]

##donut3 = alt.Chart(vac_subset).mark_arc(innerRadius=50, outerRadius=90).encode(
##    theta = 'sum(Number):Q',
##    color = 'Status',
##).properties(
##    title=f'Vaccination Status in selected continents {year} . {month}',
##    width = 500
##)

##vac_subset = vac_subset[vac_subset['Country/Region'] == country]

##donut2 = alt.Chart(vac_subset).mark_arc(innerRadius=50, outerRadius=90).encode(
##    theta = 'sum(Number):Q',
##    color = 'Status',
##).properties(
##    title=f'Vaccination Status in {country} {year} . {month}',
##    width = 500
##)

##st.altair_chart(donut2)
##st.altair_chart(donut3)
##st.altair_chart(donut1)

def load_geo_data():
    
    geo_data = pd.read_csv('https://raw.githubusercontent.com/AlexWei21/706_Final_Project/89525c718663df6c8bf7f1d48bf695d58d697107/Geometry_Data.csv')

    return geo_data

geo_data = load_geo_data()

source = alt.topo_feature(data.world_110m.url, 'countries')


MODE = st.sidebar.radio('Select view',['Global Covid-19 Trend','Covid-19 Trend and Vaccination Rate in Selected Country', 'World Map of Country Average Daily Cases and Deaths at Selected Time'])

if MODE == 'Global Covid-19 Trend':
    st.title('World and Country-wide Covid-19 Pandemic and Vaccination Status Overview')
    st.write("## Global Covid-19 Trend")
    st.altair_chart(W_combine1, use_container_width=True)
    st.altair_chart(W_combine2, use_container_width=True)

elif MODE == 'Covid-19 Trend and Vaccination Rate in Selected Country':
    st.title('World and Country-wide Covid-19 Pandemic and Vaccination Status Overview')
    st.write("## Covid-19 Trend and Vaccination Rate in Selected Country")
    continent = st.multiselect('Continent',['Asia','European','Africa','North America','South America','Oceania'],['North America'])
    subset = subset[subset["Continent"].isin(continent)]
    rank_data = subset[subset['Date'] == max(subset['Date'])]
    bars = alt.Chart(rank_data).mark_bar().encode(
        x = alt.X('Vaccinated_Percentage:Q',axis=alt.Axis(format = '%'), scale=alt.Scale(domain=(0,1))),
        y = alt.Y('Country/Region:O', sort = '-x'),
        tooltip = ['Country/Region','Vaccinated_Percentage']).properties(
        title='Vaccination ranking for selected continents')

    st.write('### Rank of the Vaccination Rate of selected Continent')
    st.altair_chart(bars, use_container_width=True)
    country = st.selectbox('Country', options = subset['Country/Region'].unique())

    st.write('### Covid-19 Cases and Deaths and Vaccination Status in Selected Country')
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
        title=f'Vaccination Status and Case number for {country}'
    )

    st.altair_chart(combine2, use_container_width=True)

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

else:
    st.title('World and Country-wide Covid-19 Pandemic and Vaccination Status Overview')
    st.write("## World Map of Country Average Daily Cases and Deaths at Selected Time")
    year = st.selectbox('Year',(2020,2021,2022), index=1)
    month = st.selectbox('Month',(1,2,3,4,5,6,7,8,9,10,11,12), index = 6)


    world_map_df = geo_data[(geo_data['Year']==year) & (geo_data['Month']==month)].groupby(['Country', 'country-code'])['Daily_Deaths', 'Daily_Cases', 'Vaccinated_Percentage'].mean().reset_index()

    background = alt.Chart(source
    ).mark_geoshape(
        fill='#aaa',
        stroke='black',
        strokeWidth=0.15
    ).properties(
        width=650,
        height=350
    ).project('naturalEarth1')

    selector = alt.selection_single(
        empty='all'
        )

    case_scale = alt.Scale(domain=[world_map_df['Daily_Cases'].min(), world_map_df['Daily_Cases'].max()])
    case_color = alt.Color(field='Daily_Cases', type="quantitative", scale=case_scale)
    chart_case = alt.Chart(source,
        ).properties( 
            width=650, height=350, title=f'World Average Daily Cases in {year}.{month} '
            ).project('naturalEarth1').add_selection(selector
            ).transform_lookup(
                    lookup="id",
                    from_=alt.LookupData(world_map_df, "country-code", ['Country','Daily_Deaths', 'Daily_Cases', 'Vaccinated_Percentage'])
                ).mark_geoshape(stroke='black', strokeWidth=0.15).encode(
                color = case_color,
                tooltip = [
                    alt.Tooltip("Country:N", title="Country"),
                    alt.Tooltip("Daily_Cases:Q", title="Average Daily Cases"),
                    alt.Tooltip("Vaccinated_Percentage:Q", title="Vaccination Percentage"),
                ]
                ).transform_filter(selector)


    death_scale = alt.Scale(domain=[world_map_df['Daily_Deaths'].min(), world_map_df['Daily_Deaths'].max()])
    death_color = alt.Color(field='Daily_Deaths', type="quantitative", scale = death_scale)
    chart_death = alt.Chart(source,
        ).properties( 
            width=650, height=350, title=f'World Average Daily Deaths in {year}.{month} '
            ).project('naturalEarth1').add_selection(
                selector).transform_lookup(
            lookup="id",
            from_=alt.LookupData(world_map_df, "country-code", ['Country','Daily_Deaths', 'Daily_Cases', 'Vaccinated_Percentage'])
            ).mark_geoshape(stroke='black',strokeWidth=0.15).encode(
                color= death_color,
                tooltip = ['Country:N', alt.Tooltip("Daily_Deaths:Q", title="Average Daily Deaths"), "Vaccinated_Percentage:Q"]
                ).transform_filter(selector)

    world_maps = alt.vconcat(background + chart_case, background + chart_death
    ).resolve_scale(
        color='independent'
    )


    st.altair_chart(world_maps)

