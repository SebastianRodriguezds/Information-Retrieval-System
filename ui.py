import tkinter as tk # Tkinter module for creating graphical user interfaces.
from tkinter import ttk, scrolledtext #ttk for theme widgets (Combobox) and scrolledtext for text widget
from searcher import search_results # function to perform the search.


def create_ui(structured_df, unstructured_df, ix):
    """function in charge of create the user interface"""
    # Initialize the main application window with an TK object.
    root = tk.Tk()
    
    #set size and title.
    root.geometry("1000x800")
    root.title("JULIA PENA Retrieval Information System") 

    # create the frame for the search input section.
    input_frame = tk.Frame(root)
    input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n") # instructions to place the frame.

    # label for the field and key word to search
    tk.Label(input_frame, text="Search Field:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
    tk.Label(input_frame, text="Key Word:").grid(row=1, column=0, padx=5, pady=8, sticky="w")

    # dropdwon menu to select the search field
    field_combobox = ttk.Combobox(input_frame, values=[
        'empid', 'firstname', 'lastname', 'department', 'startdate', 'exitdate', 
        'supervisor', 'ademail', 'employeestatus', 'division', 'dob', 'jobfunction'
    ])
    field_combobox.grid(row=0, column=1, padx=15, pady=8)
    field_combobox.set('select a field')

    # entry field for the keyword
    keyword_entry = tk.Entry(input_frame)
    keyword_entry.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

    # frame fot the buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    ################################################ # ################################################
    # Create the buttons and given functionaly and styles
    search_general_button = tk.Button(button_frame, text="GENERAL SEARCH", 
    command=lambda: search_results(ix, field_combobox.get(), keyword_entry.get(), "both", structured_df, unstructured_df, results_text))
    search_general_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    search_structured_button = tk.Button(button_frame, text="STRUCTURED SEARCH", 
    command=lambda: search_results(ix, field_combobox.get(), keyword_entry.get(), "structured", structured_df, unstructured_df, results_text))
    search_structured_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    search_unstructured_button = tk.Button(button_frame, text="UNSTRUCTURED SEARCH", 
    command=lambda: search_results(ix, field_combobox.get(), keyword_entry.get(), "unstructured", structured_df, unstructured_df, results_text))
    search_unstructured_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    clear_button = tk.Button(button_frame, text="Clear", 
                             command=lambda: clear_results(results_text))
    clear_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    ################################################ # ################################################

    # scrolled text widget to display results.
    results_text = scrolledtext.ScrolledText(root, width=80, height=30)
    results_text.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

    # config layout to make the windows responsive.
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    #start Tkinter event loop to run the application
    root.mainloop()


def clear_results(text_widget):
    """function to clear the content displayed in the text widget"""
    text_widget.delete(1.0, tk.END)
