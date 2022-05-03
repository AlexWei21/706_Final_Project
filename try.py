import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

@st.cache

def load_data():
    ## {{ CODE HERE }} ##
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
    )

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Sex"],
        var_name="Age",
        value_name="Pop",
    )

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    
    return df


df = load_data()

### P1.2 ###
st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
year = st.slider("Year", min(df["Year"]),max(df["Year"]), 2012)
subset = df[df["Year"] == year]
### P2.1 ###



### P2.2 ###
# replace with st.radio
sex = st.radio("Sex", ('M', 'F'))
subset = subset[subset["Sex"] == sex]
### P2.2 ###


### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = st.multiselect("Country", [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
],
[
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
])
subset = subset[subset["Country"].isin(countries)]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox
cancer = st.selectbox("Cancer Type ", df["Cancer"].unique())
subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Country"),
    color= alt.Color("Rate", title = "Log of Motality rate per 100k", scale=alt.Scale(type='log', domain=(0.005, 1), clamp = True)),
    tooltip=["Rate"]
).properties(
    title=f"{cancer} Log mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")

















base = alt.Chart(subset).encode(
    alt.X('Date:T', axis=alt.Axis(format = '%Y/%m',labelAngle=45))
).transform_aggregate(
    groupby=['Date']
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