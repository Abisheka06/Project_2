import pandas as pd
from dbconnection_project2 import dbwrite

file_path = "Cleaned_Bird_Monitoring_GRASSLAND.xlsx"
df = pd.read_excel(file_path, sheet_name=None)  
columns_needed = ["Plot_Name", "Observer", "ID_Method", "Wind", "Scientific_Name", "Common_Name"]
records = []

for sheet_name, sheet_df in df.items():
    print(f"Processing sheet: {sheet_name}")

    if sheet_df.empty:
        print(f"⚠ Skipping empty sheet: {sheet_name}")
        continue
    if set(columns_needed).issubset(sheet_df.columns):
        selected_data = sheet_df[columns_needed] 
        records.extend(selected_data.values.tolist())
    else:
        print(f"⚠ Skipping sheet {sheet_name} (missing required columns)")

insert_query = """
    INSERT INTO bird_monitoring_grassland (plot_name, observer, id_method, wind, sci_name, com_name)
    VALUES (%s, %s, %s, %s, %s, %s);
"""
insert_query1 = """
    INSERT INTO grassland_year (plot_name, date, start_time, end_time, sci_name, com_name)
    VALUES (%s, %s, %s, %s, %s, %s);
"""
if records:  
    dbwrite(insert_query, records)
    print("✅ Data inserted successfully!")
else:
    print("⚠ No data available for insertion.")
