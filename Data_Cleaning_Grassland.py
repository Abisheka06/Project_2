import pandas as pd

# ✅ Load the Excel file (update the filename)
file_path = "Bird_Monitoring_Data_GRASSLAND.xlsx"
df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets

cleaned_sheets = {}

for sheet, data in df.items():
    print(f"🔍 Processing sheet: {sheet}")
    
    # ✅ Step 1: Strip column names to remove extra spaces
    data.columns = data.columns.str.strip()

    # ✅ Step 2: Print column names for debugging
    print("Columns in sheet:", list(data.columns))

    # ✅ Step 3: Rename columns if necessary (manual correction)
    rename_dict = {
        " Date ": "Date",
        " Observer ": "Observer",
    }
    data.rename(columns=lambda x: x.strip(), inplace=True)  # Trim spaces
    data.rename(columns=rename_dict, inplace=True)  # Rename if needed

    # ✅ Step 4: Drop rows with missing "Date" and "Observer"
    required_columns = ["Date", "Observer"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        print(f"⚠️ Missing columns in {sheet}: {missing_columns}. Skipping row drop.")
    else:
        data.dropna(subset=required_columns, inplace=True)

    # ✅ Step 5: Remove duplicates and empty rows
    data.drop_duplicates(inplace=True)
    data.dropna(how="all", inplace=True)  # Drop fully empty rows

    cleaned_sheets[sheet] = data  # Store cleaned sheet

# ✅ Save cleaned data to a new Excel file
output_file = "Cleaned_Bird_Monitoring_Grassland.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for sheet, cleaned_data in cleaned_sheets.items():
        cleaned_data.to_excel(writer, sheet_name=sheet, index=False)

print(f"✅ Data cleaning complete! Cleaned file saved as {output_file}")
