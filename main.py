import os
import pandas as pd
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

#Read each xlsx sheet
file_path = 'structured.xlsx'

#Read every sheet in a Data Frame Dictionary
sheet_df = pd.read_excel(file_path, sheet_name=None)

#Config pandas to show all the rows
pd.set_option('display.max_rows', None)

#Access to each sheet
structured_df = sheet_df['structured']
unstructured_df = sheet_df['unstructured']

#Return an empty string if the data is None and clean withe spaces.
structured_df.columns = structured_df.columns.str.lower()
for col in structured_df.columns:
    structured_df[col] = structured_df[col].fillna('').astype(str)
    if structured_df[col].dtype == 'object':
        structured_df[col] = structured_df[col].str.strip().str.lower()

# print(structured_df)
unstructured_df['content'] = unstructured_df['Contentent in unstructured file'].astype(str).str.strip().fillna('').str.lower()

# # print(unstructured_df)
# print(structured_df.columns)

#Define the shema of Whoosh to index
schema = Schema(
    content=TEXT(stored=True),
    department=TEXT(stored=True),
    empid=TEXT(stored=True),
    firstname=TEXT(stored=True),
    lastname=TEXT(stored=True),
    startdate=TEXT(stored=True),
    exitdate=TEXT(stored=True),
    supervisor=TEXT(stored=True),
    ademail=TEXT(stored=True),
    employeestatus=TEXT(stored=True),
    division=TEXT(stored=True),
    dob=TEXT(stored=True),
    jobfunction=TEXT(stored=True),
)

index_dir = "index_dir"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

#Create index
ix = create_in(index_dir, schema)

writer = ix.writer()
for i, text in enumerate(unstructured_df['content']):
    writer.add_document(content=text)

for i, row in structured_df.iterrows():
    writer.add_document(
        empid=str(row['empid']),  # Asegúrate de que este valor es correcto
        firstname=row['firstname'],
        lastname=row['lastname'],
        department=str(row['department']),
        startdate=str(row['startdate']) if pd.notna(row['startdate']) else '',
        exitdate=str(row['exitdate']) if pd.notna(row['exitdate']) else '',
        supervisor=row['supervisor'],
        ademail=row['ademail'],
        employeestatus=row['employeestatus'],
        division=row['division'],
        dob=str(row['dob']) if pd.notna(row['dob']) else '',
        jobfunction=row['jobfunction']
    )
writer.commit()

# print(unstructured_df)


def search(user_field, user_word):
    valid_fields = ['content', 'empid', 'firstname', 'lastname', 'department', 'startdate', 'exitdate', 'supervisor', 'ademail', 'employeestatus', 'division', 'dob', 'jobfunction']
    if user_field not in valid_fields:
      print(f"El campo '{user_field}' no es válido. Por favor, ingresa un campo válido.")
    else:
       print("yes")

    with ix.searcher() as searcher:
         query_unstructured = QueryParser("content", ix.schema).parse(user_word)
         query_structured = QueryParser(user_field, ix.schema).parse(user_word)

         result_unstruc = searcher.search(query_unstructured)
         result_struc = searcher.search(query_structured)
          
        #  show result
         print(f"Resultados de la búsqueda para '{user_word}' en los datos no estructurados: ")
         for result in result_unstruc:
          print(f"Content: {result['content']}")
          print('-' * 80)

         print(f"Resultados de la búsqueda para '{(user_word)}' en los datos estructurados:")

         for result in result_struc:
          print(f"Employee ID: {result['empid']}")
          print(f"Name: {result['firstname']} {result['lastname']}")
          print(f"Department: {result['department']}")
          print(f"Job Function: {result['jobfunction']}")
          print(f"Start Date: {result['startdate']}")
          print(f"Exit Date: {result['exitdate']}")
          print('-' * 80)

user_query = str(input("Porque buscar?: "))
query_keyword = str(input("que palabra?: "))

search(user_query, query_keyword)