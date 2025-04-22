import pandas as pd


file_path = "Bird_Monitoring_Data_GRASSLAND.xlsx"
df = pd.read_excel(file_path, sheet_name=None) 

cleaned_sheets = {}

for sheet, data in df.items():
    
   
    data.columns = data.columns.str.strip()

    rename_dict = {
        " Date ": "Date",
        " Observer ": "Observer",
    }
    data.rename(columns=lambda x: x.strip(), inplace=True) 
    data.rename(columns=rename_dict, inplace=True)

    required_columns = ["Date", "Observer"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        print(f"⚠️ Missing columns in {sheet}: {missing_columns}. Skipping row drop.")
    else:
        data.dropna(subset=required_columns, inplace=True)
    data.drop_duplicates(inplace=True)
    data.dropna(how="all", inplace=True) 
    cleaned_sheets[sheet] = data  

output_file = "Cleaned_Bird_Monitoring_Grassland.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for sheet, cleaned_data in cleaned_sheets.items():
        cleaned_data.to_excel(writer, sheet_name=sheet, index=False)

print(f"✅ Data cleaning complete! Cleaned file saved as {output_file}")
