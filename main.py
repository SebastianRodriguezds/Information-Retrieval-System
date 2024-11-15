import pandas as pd

#Read each xlsx sheet
file_path = 'structured.xlsx'

#Read every sheet in a Data Frame Dictionary
sheet_df = pd.read_excel(file_path, sheet_name=None)

#Config pandas to show all the rows
# pd.set_option('display.max_rows', None)

#Access to each sheet
structured_df = sheet_df['structured']
unstructured_df = sheet_df['unstructured']

# #Clean white spaces at the begining and at the end of the columns and conver to lower case to avoid problems with upper and lower case in Headers.
structured_df.columns = structured_df.columns.str.strip().str.lower()

#Return an empty string if the data is None and clean withe spaces.
for col in structured_df.columns:
  structured_df[col] = structured_df[col].fillna('')
  if structured_df[col].dtype == 'object':
        structured_df[col] = structured_df[col].str.strip()
  
print(unstructured_df)
print(structured_df)
