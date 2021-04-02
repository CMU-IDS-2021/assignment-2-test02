import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

st.title("Let's analyze some COVID Data!")

# TODO add caching so we load the data only once w/ [at]st.cache
def load_data(url):
    return pd.read_csv(url)

# Filter by PA state only, and add `date` column in date-time for altair
def clean(df):
    PA_FIPS = 42
    df_pa = df[df['statefips'] == PA_FIPS]
    cols = ['year', 'month', 'day']
    df_pa['date'] = pd.to_datetime(df_pa[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1))
    return df_pa

# Covid, state, daily
covid_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/COVID%20-%20State%20-%20Daily.csv?raw=true"

# employment, state, daily
jobs_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/Employment%20-%20State%20-%20Daily.csv?raw=true"

df_covid = load_data(covid_url)

df_jobs = load_data(jobs_url)

st.write("# COVID cases per state, daily")

st.write(df_covid)

"""One sample COVID vis for PA only: (PA state FIPS is 42)"""

df_covid_pa = clean(df_covid)

st.write(df_covid_pa)

covid_chart = alt.Chart(df_covid_pa).mark_line().encode(
    x='date:T',
    y='new_case_count:Q',
).properties(
    width=600, height=400,
    title="Number of new cases in PA over time (Feb 2020-Mar 2021)"
).interactive()

"""(New confirmed COVID-19 cases, seven day moving average.)"""

st.write(covid_chart)

st.write("# Employment per state, daily")

st.write(df_jobs)

"""One sample employment vis for PA only:"""

df_jobs_pa = clean(df_jobs)

st.write(df_jobs_pa)

jobs_chart = alt.Chart(df_jobs_pa).mark_line().encode(
    x='date:T',
    y='emp_combined:Q'
).properties(
    width=600, height=400,
    title="Employment level for all workers in PA over time (Feb 2020-Mar 2021)"
).interactive()

st.write(jobs_chart)

"""# Employment per county, daily, shown in the US for one day"""

# employment, county, daily
county_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/Employment%20-%20County%20-%20Daily.csv?raw=true"

df_county = load_data(county_url)

"""Daily employment data by county"""

YEAR = 2020
MONTH = 5
DAY = 14

df_county = df_county[df_county['year'] == YEAR]
df_county = df_county[df_county['month'] == MONTH]
df_county = df_county[df_county['day'] == DAY]

st.write(f'Dataset filtered for just the day {MONTH}/{DAY}/{YEAR} (M/D/Y)')

df_county

counties = alt.topo_feature(data.us_10m.url, 'counties')

map = alt.Chart(counties).mark_geoshape().encode(
    color='emp_combined:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_county, 'countyfips', ['emp_combined'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300,
    title="Employment level for all workers in the US per county for 5/14/2020"
)

st.write(map)

"""Data key: https://github.com/OpportunityInsights/EconomicTracker/blob/main/docs/oi_tracker_data_dictionary.md"""

"""Sources:

https://tracktherecovery.org/

https://opportunityinsights.org/paper/tracker/

https://github.com/OpportunityInsights/EconomicTracker

https://opportunityinsights.org/wp-content/uploads/2020/06/tracker-summary.pdf

https://tracktherecovery.org/?nosplash=true

https://github.com/OpportunityInsights/EconomicTracker/blob/main/docs/oi_tracker_data_dictionary.md
"""
