import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

# TODO add caching so we load the data only once w/ [at]st.cache
@st.cache(suppress_st_warning=True)
def load_data(url):
    st.write("Loading data (uncached)", url)
    return pd.read_csv(url)

# Filter by PA state only, and add `date` column in date-time for altair
def clean(df):
    PA_FIPS = 42
    df_pa = df[df['statefips'] == PA_FIPS]
    cols = ['year', 'month', 'day']
    df_pa['date'] = pd.to_datetime(df_pa[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1))
    return df_pa

#########################

st.title("📚 Reopen schools or restaurants first?! Your attention-grabbing title here 🍢")

"""_Feel free to change any of the provided text, the provided charts, and their captions/labels/titles below! Feel free to remove/reorder things to fit your argument as well._"""


"""Add your names and team affiliation here."""

"""Add your persuasive introduction here."""

# Covid, state, daily
covid_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/COVID%20-%20State%20-%20Daily.csv?raw=true"

# employment, state, daily
jobs_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/Employment%20-%20State%20-%20Daily.csv?raw=true"

df_covid = load_data(covid_url)

df_jobs = load_data(jobs_url)

st.write("# COVID cases per state, daily")

df_covid_pa = clean(df_covid)

covid_chart = alt.Chart(df_covid_pa).mark_line().encode(
    x=alt.X('date:T', axis=alt.Axis(title='Date')),
    y=alt.Y('new_case_count:Q', axis=alt.Axis(title='New case count')),
).properties(
    width=600, height=400,
    title="Number of new cases in PA over time (Feb 2020-Mar 2021)"
)

"""Add your framing here."""

"""Here is a sample COVID visualization for PA only, showing the new confirmed COVID-19 cases over time (seven day moving average)."""

st.write(covid_chart)

"""Add your framing here."""

if st.checkbox("Show PA COVID data"):
    st.write(df_covid_pa)

#################################################

st.write("# Employment per state, daily over time")

"""One sample employment vis for PA only:"""

df_jobs_pa = clean(df_jobs)

jobs_chart = alt.Chart(df_jobs_pa).mark_line().encode(
    x=alt.X('date:T', axis=alt.Axis(title='Date')),
    y=alt.Y('emp_combined:Q', axis=alt.Axis(title='Combined employment'))
).properties(
    width=600, height=400,
    title="Employment level for all workers in PA over time (Feb 2020-Mar 2021)"
).interactive()

st.write(jobs_chart)

if st.checkbox("Show PA jobs data"):
    st.write(df_jobs_pa)

#################################################

"""# Percent change in employment since January for Feb 2, 2021"""

# employment, county, daily
county_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/Employment%20-%20County%20-%20Daily.csv?raw=true"

county_metadata_url = "https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/GeoIDs%20-%20County.csv"

df_counties_us = load_data(county_url)
counties_metadata = load_data(county_metadata_url)

df_counties_us = df_counties_us.join(counties_metadata.set_index('countyfips'), on='countyfips')

"""Daily employment data by county"""

YEAR = 2021
MONTH = 2
DAY = 5

df_counties_us = df_counties_us[df_counties_us['year'] == YEAR]
df_counties_us = df_counties_us[df_counties_us['month'] == MONTH]
df_counties_us = df_counties_us[df_counties_us['day'] == DAY]

counties = alt.topo_feature(data.us_10m.url, 'counties')

us_employment_map = alt.Chart(counties).mark_geoshape().encode(
    color=alt.Color('emp_combined:Q', legend=alt.Legend(title="Combined employment", format=".0%"))
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_counties_us, 'countyfips', ['emp_combined'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300,
    title="% change in total employment, relative to Jan. for 2/5/21"
)

st.write(us_employment_map)

if st.checkbox("Show US county employment data"):
    st.write(f'Dataset filtered for just the day {MONTH}/{DAY}/{YEAR} (M/D/Y) in the U.S.')
    df_counties_us

"""Counties in PA"""

# hover = alt.selection(type='single', on='mouseover', nearest=True, fields=['countyname', 'county_pop2019'])

hover = alt.selection_single(fields=['countyname'])

df_counties_pa = df_counties_us[df_counties_us['statename'] == "Pennsylvania"]

pa_employment_map = alt.Chart(counties).mark_geoshape().encode(
    color=alt.Color('emp_combined:Q', legend=alt.Legend(title="Combined employment", format=".0%"))
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_counties_pa, 'countyfips', ['emp_combined', 'countyname'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300,
    title="% change in total employment, relative to Jan. for 2/5/21"
).encode(
    tooltip=[alt.Text('countyname:N', title="County name"), alt.Text('emp_combined:Q', format=".0%", title="Change in total employment")]
)

st.write(pa_employment_map)

if st.checkbox("Show county metadata (used for filtering counties by state)"):
    counties_metadata

if st.checkbox("Show PA county employment data"):
    df_counties_pa

"""# Sources
 
* [_Track the Recovery_ (TTR) interactive frontend](https://tracktherecovery.org/)
* [_Track the Recovery_ datasets](https://github.com/OpportunityInsights/EconomicTracker)
* [_TTR_ data documentation](https://github.com/OpportunityInsights/EconomicTracker/blob/main/docs/oi_tracker_data_documentation.md)
* [_TTR_ data dictionary](https://github.com/OpportunityInsights/EconomicTracker/blob/main/docs/oi_tracker_data_dictionary.md)
"""
