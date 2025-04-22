import pandas as pd
import mysql.connector
from dbconnection_project2 import dbwrite

file_path = "Cleaned_Bird_Monitoring_Data_Forest.xlsx"
df = pd.read_excel(file_path, sheet_name=None)  
columns_needed = ["Plot_Name", "Date", "Start_Time", "End_Time","Scientific_Name", "Common_Name"]
records = []

for sheet_name, sheet_df in df.items():
    if set(columns_needed).issubset(sheet_df.columns):
        selected_data = sheet_df[columns_needed] 
        selected_data["Date"] = selected_data["Date"].astype(str)

        selected_data["Start_Time"] = pd.to_datetime(selected_data["Start_Time"]).dt.time
        selected_data["End_Time"] = pd.to_datetime(selected_data["End_Time"]).dt.time
    
        records.extend(selected_data.values.tolist()) 

insert_query = """
    INSERT INTO bird_monitoring (site_name, sci_name, com_name, date, location_type, observer, temperature, humidity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
insert_query1 = """
    INSERT INTO forest_year (plot_name, date, start_time, end_time, sci_name, com_name)
    VALUES (%s, %s, %s, %s, %s, %s);
"""

if records:
    dbwrite(insert_query1, records)
    print("✅ Data inserted successfully!")
else:
    print("⚠ No data available for insertion.")

