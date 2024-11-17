from data_loader import load_data #import data_loader function from data_loader module.
from indexer import create_index #import create_index function from indexer module.
from ui import create_ui #import create_ui function to diplay user interface.

def main():
    """main function that runs the application"""
    file_path = 'structured.xlsx' # define the file path to the excel file.

    # call load_data function to load and clean data from the file, the function returns two Data Frame, one for the structured data and other one for unstructured data.
    structured_df, unstructured_df = load_data(file_path)

    #The function takes the data frames as argu. and them create the index.
    ix = create_index(structured_df, unstructured_df)

    #This function is in charge of crate and display the ui.
    create_ui(structured_df, unstructured_df, ix)

#check if the script is being run directly, if so, its runs the main function.
if __name__ == "__main__":
    main()