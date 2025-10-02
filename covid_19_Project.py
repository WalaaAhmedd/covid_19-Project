# app_pretty.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("COVID-19 Data Analysis Project (Interactive Dashboard)")

# -------------------------------
# File Paths (Relative to script location)
folder_path = os.path.join(os.path.dirname(__file__), "data")  # فولدر data داخل الريبو

files = {
    "covid_clean": "covid_19_clean_complete.csv",
    "day_wise": "day_wise.csv",
    "country_latest": "country_wise_latest.csv",
    "usa_county": "usa_county_wise.csv"
}

# Load data
@st.cache_data
def load_data():
    covid_clean = pd.read_csv(os.path.join(folder_path, files["covid_clean"]))
    day_wise = pd.read_csv(os.path.join(folder_path, files["day_wise"]))
    country_latest = pd.read_csv(os.path.join(folder_path, files["country_latest"]))
    usa_county = pd.read_csv(os.path.join(folder_path, files["usa_county"]))
    
    covid_clean['Date'] = pd.to_datetime(covid_clean['Date'], errors='coerce')
    day_wise['Date'] = pd.to_datetime(day_wise['Date'], errors='coerce')
    usa_county['Date'] = pd.to_datetime(usa_county['Date'], errors='coerce')
    
    return covid_clean, day_wise, country_latest, usa_county

covid_clean, day_wise, country_latest, usa_county = load_data()

# -------------------------------
# Tabs for datasets
tabs = st.tabs(["Global Trends", "Country Snapshot", "Daily Cases", "US States Trends"])

# -------- Global Trends --------
with tabs[0]:
    st.subheader("Global COVID-19 Trends Over Time")
    global_ts = covid_clean.groupby("Date")[["Confirmed","Deaths","Recovered","Active"]].sum().reset_index()
    fig = px.line(global_ts, x="Date", y=["Confirmed","Deaths","Recovered","Active"],
                  title="Global COVID-19 Trends", labels={"value":"Cases","variable":"Metric"})
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    latest = global_ts.iloc[-1]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Confirmed", f"{int(latest['Confirmed']):,}")
    col2.metric("Deaths", f"{int(latest['Deaths']):,}")
    col3.metric("Recovered", f"{int(latest['Recovered']):,}")
    col4.metric("Active", f"{int(latest['Active']):,}")

# -------- Country Snapshot --------
with tabs[1]:
    st.subheader("Top 10 Countries")
    country_group = covid_clean.groupby("Country/Region")[["Confirmed","Deaths","Recovered","Active"]].max().reset_index()
    
    metric_choice = st.selectbox("Select Metric", ["Confirmed","Deaths","Active"])
    top10 = country_group.sort_values(metric_choice, ascending=False).head(10)
    fig = px.bar(top10, x=metric_choice, y="Country/Region", orientation='h', color=metric_choice,
                 title=f"Top 10 Countries by {metric_choice}", text=metric_choice)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

# -------- Daily Cases --------
with tabs[2]:
    st.subheader("Global Daily New Cases & Deaths")
    fig = px.line(day_wise, x="Date", y=["New cases","New deaths"], labels={"value":"Count","variable":"Metric"},
                  title="Daily New Cases & Deaths")
    st.plotly_chart(fig, use_container_width=True)

# -------- US States Trends --------
with tabs[3]:
    st.subheader("COVID-19 Trends in Major US States")
    state_ts = usa_county.groupby(['Province_State','Date'])[['Confirmed','Deaths']].sum().reset_index()
    major_states = st.multiselect("Select States", state_ts['Province_State'].unique(),
                                  default=["New York","California","Texas","Florida"])
    fig = px.line(state_ts[state_ts['Province_State'].isin(major_states)], x='Date', y='Confirmed',
                  color='Province_State', title="Confirmed Cases Over Time (US States)")
    st.plotly_chart(fig, use_container_width=True)
