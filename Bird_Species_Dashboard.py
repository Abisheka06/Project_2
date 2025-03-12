import streamlit as st

import pandas as pd

from dbconnection_project2 import dbread

from dbconnection_project2 import dbreadWithColumnNames

from dbconnection_project2 import dbwrite

import matplotlib.pyplot as plt

with st.sidebar:
        add_text=st.markdown("""
                # Toggle between screens to access more data.
        """)

page = st.sidebar.selectbox("Navigate", ["Home", "Seasonal Trends", "Temperature Vs Humidity", "Most Commonly Observed Birds"])

# Page content
if page == "Home":
    st.title('🐦🦜🦅Bird Monitoring: Forest and Grassland')
    st.title('Unquie Birds')

    row1 = st.columns(3)

    tile1 = row1[0].container(height=120)
    tile2 = row1[1].container(height=120)

    tile1.text("Total number of birds in Forest")
    tile2.text("Total number of birds in Grassland")

    value= dbread("select count(distinct sci_name) from bird_monitoring")

    if value:
        txt1=value[0][0]

    tile1.text(txt1)

    value1= dbread("select count(distinct sci_name) from bird_monitoring_grassland")

    if value1:
        txt2=value1[0][0]

    tile2.text(txt2)

    with st.sidebar:
        add_text=st.markdown("""
            # Search Birds by Name
            # Forest
        """)

        query = "select distinct sci_name from bird_monitoring"
        rows=dbread(query)
        column_data = []
        for row in rows:
            column_data.append(row[0])

        add_name=st.selectbox("Select Bird",column_data)

        data,column_names=dbreadWithColumnNames("select bf.sci_name,bf.observer,bf.site_name from bird_monitoring as bf inner join forest_year as fy on bf.id = fy.id WHERE bf.sci_name = '"+add_name+"'")


    st.title("About: "+add_name)
    df = pd.DataFrame(data, columns=column_names)

    st.dataframe(df,width=800,height=400)

    with st.sidebar:
        add_text=st.markdown("""
            # Search Birds by Name
            # Grassland
        """)

        query = "select distinct sci_name from bird_monitoring_grassland"
        rows=dbread(query)
        column_data = []
        for row in rows:
            column_data.append(row[0])

        add_name1=st.selectbox("Select Bird",column_data)

        data1,column_names1=dbreadWithColumnNames("select bg.sci_name,bg.observer,bg.plot_name from bird_monitoring_grassland as bg inner join grassland_year as gy on bg.id = gy.id WHERE bg.sci_name = '"+add_name1+"'")


    st.title("About: "+add_name1)
    df1 = pd.DataFrame(data1, columns=column_names1)

    st.dataframe(df1,width=800,height=400)
    

elif page == "Seasonal Trends":
    st.title('☀️❄️Seasonal Trends')

    # Fetch Data from Database
    forest_year = pd.DataFrame(dbread("SELECT date, sci_name, com_name FROM forest_year"), 
                               columns=['Date', 'Scientific Name', 'Common Name'])
    grassland_year = pd.DataFrame(dbread("SELECT date, sci_name, com_name FROM grassland_year"), 
                                  columns=['Date', 'Scientific Name', 'Common Name'])
    bird_monitoring = pd.DataFrame(dbread("SELECT date, temperature, humidity, sci_name, com_name FROM bird_monitoring"), 
                                   columns=['Date', 'Temperature', 'Humidity', 'Scientific Name', 'Common Name'])
    bird_monitoring_grassland = pd.DataFrame(dbread("SELECT plot_name, sci_name, com_name FROM bird_monitoring_grassland"), 
                                             columns=['Plot Name', 'Scientific Name', 'Common Name'])

    # Handle Empty or Null Data
    forest_year.dropna(inplace=True)
    grassland_year.dropna(inplace=True)

    # Convert Date Columns to Datetime Format
    forest_year['Date'] = pd.to_datetime(forest_year['Date'], errors='coerce')
    grassland_year['Date'] = pd.to_datetime(grassland_year['Date'], errors='coerce')

    # Extract Month for Seasonal Trends
    forest_year['Month'] = forest_year['Date'].dt.month
    grassland_year['Month'] = grassland_year['Date'].dt.month

    # Count Sightings per Month
    forest_trend = forest_year['Month'].value_counts().sort_index()
    grassland_trend = grassland_year['Month'].value_counts().sort_index()

    #  Plotting the Graph
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(forest_trend.index, forest_trend.values, marker='o', label='Forest')
    ax.plot(grassland_trend.index, grassland_trend.values, marker='s', label='Grassland')

    # Adding Labels and Legend
    ax.set_title("Bird Sightings Trend by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Sightings")
    ax.legend()

    # Display the Plot in Streamlit
    st.pyplot(fig)

elif page == "Temperature Vs Humidity":
    st.header("🌡 Temperature vs Humidity")
    bird_monitoring = pd.DataFrame(dbread("SELECT date, temperature, humidity, sci_name, com_name FROM bird_monitoring"), 
                                   columns=['Date', 'Temperature', 'Humidity', 'Scientific Name', 'Common Name'])
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(bird_monitoring['Temperature'], bird_monitoring['Humidity'], color='green', alpha=0.5)
    ax.set_title("Temperature vs Humidity")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Humidity (%)")
    st.pyplot(fig)

else:
    st.header("🦜 Most Commonly Observed Birds")
    forest_year = pd.DataFrame(dbread("SELECT date, sci_name, com_name FROM forest_year"), 
                               columns=['Date', 'Scientific Name', 'Common Name'])
    grassland_year = pd.DataFrame(dbread("SELECT date, sci_name, com_name FROM grassland_year"), 
                                  columns=['Date', 'Scientific Name', 'Common Name'])
    common_birds_forest = forest_year['Common Name'].value_counts().head(10)
    common_birds_grassland = grassland_year['Common Name'].value_counts().head(10)

    fig, ax = plt.subplots(1, 2, figsize=(25, 10))

    # Forest
    ax[0].barh(common_birds_forest.index, common_birds_forest.values, color='orange')
    ax[0].set_title("Top 10 Birds in Forest")
    ax[0].invert_yaxis()

    # Grassland
    ax[1].barh(common_birds_grassland.index, common_birds_grassland.values, color='skyblue')
    ax[1].set_title("Top 10 Birds in Grassland")
    ax[1].invert_yaxis()

    st.pyplot(fig)


    
        





    