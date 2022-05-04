![](RackMultipart20220504-1-3zpcct_html_3d1d00263eea809a.png)

# Covid-19 Status App Guide

Group Members: Alex Wei, Benito D Isaac, Yidan Ma

**Table of Content**

**[Steps](#_5t57xu65mrgb)**

[Tasks Clarification](#_b2655jc2do) 

[Dataset Searching and Understanding](#_z0kdvvqpl0jw) 

[Covid-19 World Case Dataset / Covid-19 World Death Dataset](#_tvx15au8ltta) 

[Covid-19 Vaccination Status Dataset](#_kwsrnnsbezjy) 

[Continent Information Dataset](#_j6rk56ui1fov) 

[World Population Dataset](#_n5uhq2u4yo4e) 

[Dataset Preprocessing](#_6d40w1ezh7a1) 

[Joining Case/Death, vaccination status, continent information, and population datasets](#_r8ch41somjyv) 

[Construct Streamlit App](#_pcqhtdpeeivo) 

[SideBar](#_m9z7a1do28qy) 

[Global Covid-19 Information Line Chart](#_3a1b8ke9ue5t) 

[The rank of the Vaccination Rate of Selected Continent](#_j28r07pf8mvt) 

[Covid-19 Information for a Selected Country Line Chart](#_v5pq7ghm8gmw) 

[Detailed Vaccination Status Pie Chart](#_bch0ywwhdlen) 

[Global Map with Death and Case Data](#_yvhplxc98ewr) 

**[Observations using Our Streamlit App](#_mk43oc8o8wfn)**

**[Future Work and Additional Sketches](#_f81h36pcbkwy)**

[Covid-19 Follow-up](#_h34ms4a1ok2a) 

[Comparison Between Different Diseases](#_x9chswgk9upa) 

[Collect Data With Detailed Stratification](#_1pjxlprggr9o) 

**[Contributions](#_vlpfual29nmb)**

**[Reference](#_itss75kbx4kc)**

## Steps

### Tasks Clarification

Covid-19 is one of the most devastating disasters in human history, and now according to what Dr. Anthony Fauci said on Apr 27th, &#39;the United States is no longer in a pandemic phase&#39;, Covid-19 finally seems to come to an end. It&#39;s a great time to look back into Year 2020, 2021, and 2022 and use the power of data visualization tools to represent the status of Covid-19 in the past years, gain insights on what happened and hopefully get some takeaways from the pandemic. So, our team decided to explore the relationships between vaccination and the death/case rate of covid 19 in the country, continent, and worldwide level, as a way to gain more insights into the pandemics.

### Dataset Searching and Understanding

We searched online about the Covid-19 dataset, and finally, find five datasets that are helpful in analyzing the status of covid-19 in the past two years: Covid-19 World Case Dataset, Covid-19 World Death Dataset, Covid-19 Vaccination Status Dataset, World population dataset, continent information dataset, and Geometric Map Dataset. These datasets are mainly compiled by the Jhon Hopkins University and, we have been able to retrieve the raw data from their repository.

#### Covid-19 World Case Dataset / Covid-19 World Death Dataset

Link to the dataset (Cases): ([https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse\_covid\_19\_data/csse\_covid\_19\_time\_series/time\_series\_covid19\_confirmed\_global.csv](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv))

Link to the dataset (Deaths):

([https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse\_covid\_19\_data/csse\_covid\_19\_time\_series/time\_series\_covid19\_deaths\_global.csv](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv))

Covid-19 World Cases Dataset and Covid-19 World Deaths dataset are from the same publication, where it contains variables: Province/State, Country/Region, Lat, Long, Dates from 1/20/2020 till today, The data was a time-series data containing 3342 collectors&#39; country-wide for Covid-19 Cases and deaths number.

#### Covid-19 Vaccination Status Dataset

Link to the dataset:

([https://raw.githubusercontent.com/govex/COVID-19/master/data\_tables/vaccine\_data/global\_data/time\_series\_covid19\_vaccine\_global.csv](https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv))

This dataset shows the vaccination status of every country in the world. It contains information about admin doses, the partially vaccinated population, and the fully vaccinated population of the country. This information could help us find out how vaccination helps in controlling Covid-19 pandemic.

#### Continent Information Dataset

Link to the dataset:

([https://pypi.org/project/pycountry-convert/](https://pypi.org/project/pycountry-convert/))

This dataset helps to convert the names of the countries to the continent they belong to, thus we could analyze Covid data on a continent level.

#### World Population Dataset

Link to the dataset:

([https://www.kaggle.com/datasets/rsrishav/world-population?resource=download&amp;select=2022\_population.csv](https://www.kaggle.com/datasets/rsrishav/world-population?resource=download&amp;select=2022_population.csv))

World Population Dataset provides the population of countries worldwide. This dataset would be used when calculating cases/million people in order to compare the severity of pandemics between countries. It also contains the area of the country, which might be helpful in calculating the relationship between population density and the covid severity of the country. It also contains geometry shapefile information about countries to build the map visualization.

### Dataset Preprocessing

The dataset we mentioned above are from different sources, thus their covariates, names of the country, and standard of the data might not be exactly the same. So, we need to clean the data and make an integrated dataset for future use.

#### **Joining Case/Death, vaccination status, continent information, and population datasets**

Case and Death datasets contain dates as columns, which is not an ideal data storage format for processing. So we use the &#39;melt&#39; function in pandas to tidy the dataset and spread the date information from columns to rows. Since these two datasets are from the same resource, we don&#39;t need to do much to join them.

The vaccination Status dataset is from another source, after searching, we found that the names of countries in this dataset have some differences compared to the Case/Death dataset. The countries containing different names in the two datasets contain: the United States, South Korea, etc. (12 in total.) We match the country names in these two statuses and left-join the vaccination status dataset to the Case/Death Dataset.

Continent Information is added to the table using the package mentioned above.

The population Status dataset is joined into the dataset using the same method as the vaccination status, it contains fewer countries with different names, and after that, the integrated dataset that is ready for use is produced.

**Outcome**

![](RackMultipart20220504-1-3zpcct_html_6d97f76744a6e65a.png)

Table 1: Outcome Table of the Preprocessing Step


### Construct Streamlit App

The Streamlit app is constructed using packages &#39;altair&#39; and &#39;streamlit&#39;. There are mainly five parts of the app: Global Covid-19 Information Line Chart, Covid-19 Information for a Selected Country Line Chart, Detailed Vaccination Status Pie Chart, and Geometric Map.

Link to the app:

([https://share.streamlit.io/alexwei21/706\_final\_project/main/Final\_App.py](https://share.streamlit.io/alexwei21/706_final_project/main/Final_App.py))


#### SideBar

We decided to create a sidebar to our streamlit app, since we think that users usually come to our app with their own questions that needed to be answered. We want to let them choose what kind of information they want to see instead of seeing all the information that might not be useful for them. So, we divided our app into three parts answering three questions using the sidebar.


#### Global Covid-19 Information Line Chart

The Global Covid-19 information line chart contains two graphs. One graph contains the information on daily deaths interacting with vaccination status all over the world, while the other graph contains the case number with vaccination status. Case and Death numbers are shown as the area in the graph, while the line represents the vaccination percentage around the world.


#### The rank of the Vaccination Rate of Selected Continent

The rank of the vaccination rate of the selected continent shows the ultimate (till now) vaccination rate in all countries belonging to that continent in descending order.


#### Covid-19 Information for a Selected Country Line Chart

Country-wide Covid-19 information line chart contains two graphs. One graph contains the information on daily death cooperates with vaccination status in the selected country, while the other graph contains the case number with vaccination status. Cases and Deaths numbers are shown as the area in the graph, while the line represents the vaccination percentage around the world.

Users could choose the country by filtering continents and thus select a country that is interested in looking deep into the Covid data in that specific country.


#### Detailed Vaccination Status Pie Chart

Detailed Vaccination Status Pie chart enables the user to select a country with a specific month to see the detailed vaccination status of that country compared to the continent that country belongs to and also compare with the entire world in that specific month.


#### Global Map with Death and Case Data

Using the global map as the containing of cases and death around the world could provide a comparison of deaths and cases statistics among countries within a month directly. Also when selected on one country, the country would be highlighted, helping the users to focus on the data of a single country. The tooltip shows the cases/deaths number, country name, and the selected month of the dataset.



## Observations using Our Streamlit App

**Global Covid-19 Information**

From the global covid-19 information, we could see that before 2021/7, as the case number increases, the death rate would also increase significantly. However, after that, the peak of cases after 2022/1 doesn&#39;t cause a boost in death numbers. This may indicate that the mutation of the virus has been on the trend of being less lethal. We could also see from the graph that as the vaccination rate increased globally, there is a significant decrease in both case and death numbers, as time passed, the cases number may increase again due to mutation, however, the death rate stayed low, which may indicate that vaccination may not always be effective on preventing infection, but is useful in controlling death rate, especially on controlling the severe symptom of the Covid Virus even considering virus mutation.

![](RackMultipart20220504-1-3zpcct_html_3d83f0e1fe8af70f.png)

**The rank of the Vaccination Rate of Selected Continent**

Take North America as an example continent, we could see from the bar graph here the ranking of vaccination rate in the continent. We could see that the vaccination rate differs a lot among countries on the same continent. For example, here in North America, the United States has a high vaccination rate of 66%, while countries like Jamaica only have a vaccination rate of 23%. From this data, we could see that though large countries have a relatively quick response to spreading vaccination, there are still lots of countries in the world that lack the ability to produce vaccines, and the transportation of mRNA vaccines is still a limitation to the global defense of pandemic.

![](RackMultipart20220504-1-3zpcct_html_bc73a9931db633d5.png)

**Covid-19 Information for a selected continent and country**

Besides all the information Global Covid-19 Information could provide, cases and death rates of a specific country over time might help us have a glance at how different countries respond to Covid-19 Pandemic. Take China as an example, we could see there in the line chart that the death and case rate decreased to almost zero even before the vaccine was introduced. This may indicate a different strategy China is using that is successful in preventing the spread of pandemics.

![](RackMultipart20220504-1-3zpcct_html_3e8093f2b3638784.png)

**Detailed Vaccination Status of the selected country compared to the continent and the global situation**

Take the vaccination status in Antigua and Barbuda in July 2021 as an example. We could see here that Barbuda has a higher rate of people fully vaccinated and a lower rate of people who have not been vaccinated at all compared to the average level of North America and also the entire world. So we could infer that Antigua and Barbuda did a better job on vaccination spreading compared to most other countries in North America and the entire world. We could also select a different month in order to see the performance of vaccine spreading of a certain country over different time periods compared to the continent it belongs to and the entire world.

![](RackMultipart20220504-1-3zpcct_html_fe13e970d4a88702.png) ![](RackMultipart20220504-1-3zpcct_html_a83b82418882ac2c.png)

**Compare Global Covid-19 Information and Covid-19 Information for a selected continent and country**

When comparing the global Covid-19 information with continent data and country-specific data, we could see how fast each country is responding to the pandemic with respect to other countries in the world, we could also see that though sometimes the pandemic isn&#39;t that severe when looking that globally, some countries may suffer much more than the global average. As a result, we should focus both on the global information and country-specific information about the pandemic when we are facing other future pandemics.

**Global Map with Death and Case Number**

Taking Russia at 2021.8 as an example, we could see that that case number is relatively low in Russia compared to other countries in the world, however, the death number in Russia is one of the highest in the world. This indicates that case numbers and death numbers are not always proportional worldwide. The lethality of viruses keeps changing as time passes and virus mutations don&#39;t have to be the same around the world at the same time, leading to a difference in death/case ratio.

![](RackMultipart20220504-1-3zpcct_html_4788e972eefc4d15.png)

## Contributions

**Alex Wei**

- Design Streamlit App
- Provide Sketches
- Preprocessed the Dataset
- Line Chart Construction
- Write-up and Video Demo

**Benito D Isaac**

- Design Streamlit App
- Provide Sketches
- Preprocessed the Dataset
- Map Construction
- Review and edit write-up

**Yidan Ma**

- Design Streamlit App
- Provide Sketches
- Preprocessed the Dataset
- Pie Chart Construction
- Write-up and Video Demo
- Map Construction
- Sidebar Construction

## Reference

We used PSet2 for Reference
