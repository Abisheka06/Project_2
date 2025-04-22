import pandas as pd


file_path = "Bird_Monitoring_Data_FOREST.xlsx" 
df = pd.read_excel(file_path, sheet_name=None) 

cleaned_sheets = {}

for sheet, data in df.items():
    print(f"Processing sheet: {sheet}")
    data.columns = data.columns.str.strip()
    data.dropna(how="all", inplace=True) 
    data.dropna(axis=1, how="all", inplace=True)  
    required_columns = ["Date", "Observer"] 
    data.dropna(subset=required_columns, inplace=True)  
    data.drop_duplicates(inplace=True)
    data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    cleaned_sheets[sheet] = data
output_file = "Cleaned_Bird_Monitoring_Data.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for sheet, cleaned_data in cleaned_sheets.items():
        cleaned_data.to_excel(writer, sheet_name=sheet, index=False)

print(f"✅ Data cleaning complete! Cleaned file saved as {output_file}")
