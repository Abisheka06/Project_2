import pandas as pd

# ✅ Step 1: Read the Excel File
file_path = "Bird_Monitoring_Data_FOREST.xlsx"  # Replace with actual file path
df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets as a dictionary

cleaned_sheets = {}

for sheet, data in df.items():
    print(f"Processing sheet: {sheet}")
    
    # ✅ Step 2: Remove leading/trailing spaces from column names
    data.columns = data.columns.str.strip()

    # ✅ Step 3: Drop completely empty rows and columns
    data.dropna(how="all", inplace=True)  # Drop rows that are completely empty
    data.dropna(axis=1, how="all", inplace=True)  # Drop empty columns

    # ✅ Step 4: Drop rows where critical columns are missing (e.g., "Date", "Observer")
    required_columns = ["Date", "Observer"]  # Change based on dataset
    data.dropna(subset=required_columns, inplace=True)  

    # ✅ Step 5: Remove duplicates
    data.drop_duplicates(inplace=True)

    # ✅ Step 6: Trim whitespace from all string values
    data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # ✅ Store cleaned sheet
    cleaned_sheets[sheet] = data

# ✅ Step 7: Save cleaned data to a new Excel file
output_file = "Cleaned_Bird_Monitoring_Data.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for sheet, cleaned_data in cleaned_sheets.items():
        cleaned_data.to_excel(writer, sheet_name=sheet, index=False)

print(f"✅ Data cleaning complete! Cleaned file saved as {output_file}")
