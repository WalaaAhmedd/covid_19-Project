import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("COVID-19 Dashboard Test")

# Load a CSV
df = pd.read_csv("covid_19_clean_complete.csv")

# Show a table
st.subheader("Sample Data")
st.dataframe(df.head())

# Make a chart
st.subheader("Top 10 Countries - Confirmed Cases")
cases_by_country = df.groupby("Country/Region")["Confirmed"].max().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8,5))
cases_by_country.plot(kind="bar", color="orange", ax=ax)
plt.xticks(rotation=45)
plt.ylabel("Confirmed Cases")

st.pyplot(fig)
