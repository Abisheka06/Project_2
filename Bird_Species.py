import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Database Connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='project2'
)

# Function to get data from a table
def fetch_data(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(data)

# Load Data
forest_year = fetch_data("SELECT date, sci_name, com_name FROM forest_year")
grassland_year = fetch_data("SELECT date, sci_name, com_name FROM grassland_year")
bird_monitoring = fetch_data("SELECT date, temperature, humidity, sci_name, com_name FROM bird_monitoring")
bird_monitoring_grassland = fetch_data("SELECT plot_name, sci_name, com_name FROM bird_monitoring_grassland")

# Rename Columns
forest_year.columns = ['Date', 'Scientific Name', 'Common Name']
grassland_year.columns = ['Date', 'Scientific Name', 'Common Name']
bird_monitoring.columns = ['Date', 'Temperature', 'Humidity', 'Scientific Name', 'Common Name']
bird_monitoring_grassland.columns = ['Plot Name', 'Scientific Name', 'Common Name']

# Convert Date Columns to Datetime
forest_year['Date'] = pd.to_datetime(forest_year['Date'])
grassland_year['Date'] = pd.to_datetime(grassland_year['Date'])
bird_monitoring['Date'] = pd.to_datetime(bird_monitoring['Date'])

# Page Title
st.title("🦜 Bird Monitoring Dashboard (Forest & Grassland)")

# --- 1. Seasonal Trends ---
st.header("📅 Seasonal Trends")
fig, ax = plt.subplots(figsize=(10, 5))

forest_year['Month'] = forest_year['Date'].dt.month
grassland_year['Month'] = grassland_year['Date'].dt.month

forest_trend = forest_year['Month'].value_counts().sort_index()
grassland_trend = grassland_year['Month'].value_counts().sort_index()

ax.plot(forest_trend.index, forest_trend.values, marker='o', label='Forest')
ax.plot(grassland_trend.index, grassland_trend.values, marker='s', label='Grassland')

ax.set_title("Bird Sightings Trend by Month")
ax.set_xlabel("Month")
ax.set_ylabel("Number of Sightings")
ax.legend()

st.pyplot(fig)

# --- 2. Temperature vs Humidity ---
st.header("🌡 Temperature vs Humidity")
fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(bird_monitoring['Temperature'], bird_monitoring['Humidity'], color='green', alpha=0.5)
ax.set_title("Temperature vs Humidity")
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Humidity (%)")

st.pyplot(fig)

# --- 3. Most Common Birds ---
st.header("🦜 Most Commonly Observed Birds")
common_birds_forest = forest_year['Common Name'].value_counts().head(10)
common_birds_grassland = grassland_year['Common Name'].value_counts().head(10)

fig, ax = plt.subplots(1, 2, figsize=(15, 5))

# Forest
ax[0].barh(common_birds_forest.index, common_birds_forest.values, color='orange')
ax[0].set_title("Top 10 Birds in Forest")
ax[0].invert_yaxis()

# Grassland
ax[1].barh(common_birds_grassland.index, common_birds_grassland.values, color='skyblue')
ax[1].set_title("Top 10 Birds in Grassland")
ax[1].invert_yaxis()

st.pyplot(fig)

# --- 4. Bird Activity by Time of Day ---
st.header("⏱ Bird Activity by Time of Day")
bird_monitoring['Hour'] = bird_monitoring['Date'].dt.hour

fig, ax = plt.subplots(figsize=(10, 5))
bird_monitoring['Hour'].value_counts().sort_index().plot(kind='bar', color='purple', ax=ax)

ax.set_title("Bird Activity Based on Time of Day")
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Number of Sightings")
st.pyplot(fig)

# --- 5. Unique Bird Species ---
st.header("🦅 Unique Bird Species")
forest_unique_species = forest_year['Scientific Name'].nunique()
grassland_unique_species = grassland_year['Scientific Name'].nunique()

st.write(f"✅ **Unique Species in Forest:** {forest_unique_species}")
st.write(f"✅ **Unique Species in Grassland:** {grassland_unique_species}")

# Close Connection
conn.close()
