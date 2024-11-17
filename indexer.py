#Import necessary libraries for file operations, indexing, and qurying
import os
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import QueryParser
import pandas as pd


def create_index(structured_df, unstructured_df, index_dir="index_dir"):
    """function to create the index using structured and unstructured"""
    # Define the schema for the Whoosh index, specifying the fields to be indexed.
    # Each field is defined as a TEXT field with 'stored=True', meaning the content will be stored in the index.
    schema = Schema(
        content=TEXT(stored=True), # Unstructured content field
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

    # Check is the index directory exists otherwise create it.
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    # Create the Whoosh index using the schema and the specified direcotry
    ix = create_in(index_dir, schema)

    # Open a writer to add documents to the index
    writer = ix.writer()

    # Index the unstructured by iterating through the 'content' column.
    for i, text in enumerate(unstructured_df['content']):
        writer.add_document(content=text) # add each piece of content to the index.

    # Index structured by iterating through the rows of the structured dataframe
    for i, row in structured_df.iterrows():
        writer.add_document(
            empid=str(row['empid']),
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

    # Commit the writer to finalize and store the documents in the index.
    writer.commit()
    
    #return the index object, wich can be used for querying the data.
    return ix
