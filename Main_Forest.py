import pandas as pd
import mysql.connector
from dbconnection_project2 import dbwrite

# Load the Excel file
file_path = "Cleaned_Bird_Monitoring_Data_Forest.xlsx"
df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets into a dictionary

# Columns to extract
columns_needed = ["Plot_Name", "Date", "Start_Time", "End_Time","Scientific_Name", "Common_Name"]

# Create an empty list to store selected data
records = []

# Loop through each sheet and extract only required columns
for sheet_name, sheet_df in df.items():
    if set(columns_needed).issubset(sheet_df.columns):  # Ensure all columns exist in the sheet
        selected_data = sheet_df[columns_needed] # Select only needed columns
        selected_data["Date"] = selected_data["Date"].astype(str)

        selected_data["Start_Time"] = pd.to_datetime(selected_data["Start_Time"]).dt.time
        selected_data["End_Time"] = pd.to_datetime(selected_data["End_Time"]).dt.time
    
        records.extend(selected_data.values.tolist())  # Convert to list of lists

insert_query = """
    INSERT INTO bird_monitoring (site_name, sci_name, com_name, date, location_type, observer, temperature, humidity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
insert_query1 = """
    INSERT INTO forest_year (plot_name, date, start_time, end_time, sci_name, com_name)
    VALUES (%s, %s, %s, %s, %s, %s);
"""

# Insert data using dbwrite function
if records:  # Check if there is data to insert
    dbwrite(insert_query1, records)
    print("✅ Data inserted successfully!")
else:
    print("⚠ No data available for insertion.")

