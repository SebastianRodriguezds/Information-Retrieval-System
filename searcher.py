from rapidfuzz import fuzz, process # 'fuzz' to check similarity in strings.
from whoosh.qparser import QueryParser # 'QuereyParser' for parsing search queries te be used with Whoosh search engine.
import tkinter  as tk

def search_results(ix, user_field, user_word, search_type, structured_df, unstructured_df, text_widget):
    # valid fields to search in structured data
    valid_fields = ['content', 'empid', 'firstname', 'lastname', 'department', 'startdate', 'exitdate', 'supervisor', 'ademail', 'employeestatus', 'division', 'dob', 'jobfunction']

    #validate the user field selection.
    if search_type == "structured" and user_field not in valid_fields or user_field == "":
        text_widget.insert("Error", f"THE FIELD '{user_field}' IS INVALID. PLEASE, SELECT A VALID FIELD.")
        return

    # display a title for the reuslts and the choosen word.
    text_widget.insert(tk.END, f"\n RESULT OF THE SEARCH FOR '{user_word}' IN {search_type} DATA SETS:\n")

    # collection of objects to avoid duplicates in related results. 
    shown_keys = set()

    # search for the result using whoosh index
    with ix.searcher() as searcher:
        
        if search_type in ["UNSTRUCTURED", "BOTH"]:
            #query unstructured data with a tolerance of ~1 fuzzy matching.
            query_unstructured = QueryParser("content", ix.schema).parse(f"{user_word}~1")
            results_unstructured = searcher.search(query_unstructured)
            text_widget.insert(tk.END, "UNSTRUCTURED DATA:\n") # insert the reuslts in the widgget.
            for result in results_unstructured:
                result_text = result['content'].strip().lower()
                text_widget.insert(tk.END, f"Content: {result['content']}\n")
                text_widget.insert(tk.END, '-' * 80 + '\n')
                shown_keys.add(result_text)

        #query structured data with a tolerance of ~1 fuzzy matching using user_field
        if search_type in ["STRUCTURED", "BOTH"]:
            query_structured = QueryParser(user_field, ix.schema).parse(f"{user_word}~1")
            results_structured = searcher.search(query_structured)
            text_widget.insert(tk.END, "STRUCTURED DATA:\n")

            for result in results_structured:
                #extract relevant fields from structured data.
                emp_id = result['empid']
                full_name = f"{result['firstname']} {result['lastname']}".strip().lower()

                text_widget.insert(tk.END, f"Employee ID: {emp_id}\n")
                text_widget.insert(tk.END, f"Name: {result['firstname']} {result['lastname']}\n")
                text_widget.insert(tk.END, f"Department: {result['department']}\n")
                text_widget.insert(tk.END, f"Job Function: {result['jobfunction']}\n")
                text_widget.insert(tk.END, '-' * 80 + '\n')
                
                #add the key and name to shown_keys to avoid display duplicates.
                shown_keys.add(emp_id)
                shown_keys.add(full_name)

    # Show related results.
    text_widget.insert(tk.END, "\nRELATED RESULTS:\n")
    # Combine relevant columns from structured and unstructured data into a list
    all_data = (
        structured_df['firstname'].dropna().tolist() + 
        structured_df['lastname'].dropna().tolist() + 
        unstructured_df['content'].dropna().tolist()
    )

    # Extract top 10 related results based on fuzzy matching (using partial ratio score) from all data
    related_results = process.extract(user_word, all_data, scorer=fuzz.partial_ratio, limit=10)

    for related_text, score, _ in related_results:
        if score > 80: #only consider results with a score grater than 80 for relevance.
            related_text_lower = related_text.lower()
            # only diplay result that dosen't been shown.
            if related_text_lower not in shown_keys:
                shown_keys.add(related_text_lower)

                 # Search and display matching structured data based on the related text
                related_structured = structured_df[
                    (structured_df['firstname'].str.contains(related_text, case=False, regex=False)) |
                    (structured_df['lastname'].str.contains(related_text, case=False, regex=False))
                ]
                for _, row in related_structured.iterrows(): # Loop through the rows in related structured data
                    if row['empid'] not in shown_keys: # if wasn't displayed in the structured or unstructured that means is realated so display it.
                        text_widget.insert(tk.END, f"Employee ID: {row['empid']}\n")
                        text_widget.insert(tk.END, f"Name: {row['firstname']} {row['lastname']}\n")
                        text_widget.insert(tk.END, f"Department: {row['department']}\n")
                        text_widget.insert(tk.END, '-' * 80 + '\n')

                         # Add employee ID to shown_keys to avoid duplicates
                        shown_keys.add(row['empid'])
                # Search and display matching unstructured data based on the related text
                related_unstructured = unstructured_df[
                    unstructured_df['content'].str.contains(related_text, case=False, regex=False)
                ]
                for _, row in related_unstructured.iterrows():   # Loop through related unstructured data
                    if row['content'] not in shown_keys:
                        text_widget.insert(tk.END, f"Content: {row['content']}\n")
                        text_widget.insert(tk.END, '-' * 80 + '\n')
                        # Add employee ID to shown_keys to avoid duplicates
                        shown_keys.add(row['content'])