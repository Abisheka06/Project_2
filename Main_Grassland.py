import pandas as pd
from dbconnection_project2 import dbwrite

# Load the Excel file
file_path = "Cleaned_Bird_Monitoring_GRASSLAND.xlsx"
df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets into a dictionary

# Columns to extract
columns_needed = ["Plot_Name", "Observer", "ID_Method", "Wind", "Scientific_Name", "Common_Name"]

# Create an empty list to store selected data
records = []

# Loop through each sheet and extract only required columns
for sheet_name, sheet_df in df.items():
    print(f"Processing sheet: {sheet_name}")

    # Skip empty sheets
    if sheet_df.empty:
        print(f"⚠ Skipping empty sheet: {sheet_name}")
        continue

    # Check if required columns exist
    if set(columns_needed).issubset(sheet_df.columns):
        selected_data = sheet_df[columns_needed]  # Select only needed columns
       # selected_data["Date"] = pd.to_datetime(selected_data["Date"]).dt.date

        # ✅ Convert Start_Time and End_Time to Time only (remove Timestamp)
       # selected_data["Start_Time"] = pd.to_datetime(selected_data["Start_Time"]).dt.time
       # selected_data["End_Time"] = pd.to_datetime(selected_data["End_Time"]).dt.time

        # Convert to list of lists
        records.extend(selected_data.values.tolist())
    else:
        print(f"⚠ Skipping sheet {sheet_name} (missing required columns)")

# Print extracted data for verification
print(f"Extracted {len(records)} rows.")

# SQL Insert Query
insert_query = """
    INSERT INTO bird_monitoring_grassland (plot_name, observer, id_method, wind, sci_name, com_name)
    VALUES (%s, %s, %s, %s, %s, %s);
"""
insert_query1 = """
    INSERT INTO grassland_year (plot_name, date, start_time, end_time, sci_name, com_name)
    VALUES (%s, %s, %s, %s, %s, %s);
"""

# Insert data using dbwrite function
if records:  # Check if there is data to insert
    dbwrite(insert_query, records)
    print("✅ Data inserted successfully!")
else:
    print("⚠ No data available for insertion.")
