import pandas as pd #import pandas to analyse and manipulate data

def load_data(file_path):
    """Takes the path of the file as argument, them read the sheets from the file and convert them into a dictionary DataFrames. key = sheet name : value = DataFrame of that sheet"""
    sheet_df = pd.read_excel(file_path, sheet_name=None)

    #Save the DataFrames into variables.
    structured_df = sheet_df['structured']
    unstructured_df = sheet_df['unstructured']

    #Convert column names to lower case.
    structured_df.columns = structured_df.columns.str.lower()

    #Iterate to each column in the structured frame and clean the data, ensuring all the values are strings data type and and filling (NaN) values.
    for col in structured_df.columns:
        structured_df[col] = structured_df[col].fillna('').astype(str)
        if structured_df[col].dtype == 'object':
            structured_df[col] = structured_df[col].str.strip().str.lower()

    #Clean the unstructured frame to ensure sonsistency.
    unstructured_df['content'] = unstructured_df['Contentent in unstructured file'].astype(str).str.strip().fillna('').str.lower()

    #Return the cleaned DataFrames.
    return structured_df, unstructured_df
