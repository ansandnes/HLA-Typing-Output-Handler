# This file contains the fill_hla_types_per_patient_concatinated function.

# Third party imports
import pandas as pd

# Built in imports
import os


def fill_hla_types_per_patient_concatinated(output_path, folder_in_output_path):
    """
        Processes Excel files in the specified folder, extracting relevant HLA typing data
        for each patient from the sheets and consolidates this data into a new Excel file.

        For each Excel file in the provided folder, the function:
        1. Iterates over all sheets.
        2. Extracts data related to HLA typing (specifically for loci A, B, C, DQA1, DQB1, DRB1, etc.) 
        and stores the QC status for each chromosome copy.
        3. Modify data to contain concatinated alleles by chromosome copies.
        4. Flattens the extracted data into a single row per patient (sheet).
        5. Consolidates the rows into a new DataFrame.
        6. Removes any rows where the 'PATIENT_ID' is equal to "Sheet" (default sheets added by pandas).
        7. Writes the final DataFrame to a new Excel file with the specified folder name.

        The resulting Excel file will contain data with columns for each of the HLA loci and their respective QC pass statuses.
        
        Parameters:
        -----------
        output_path : str
            The directory path where the input Excel files are located and where the output file will be saved.
        
        folder_in_output_path : str
            The subfolder within `output_path` where the processed Excel file will be saved.

        Returns:
        --------
        rowData : list of dicts
            The data for the rows in the new consolidated Excel file, ready for use in a table (e.g., Dash Ag-Grid).
        
        columnDefs : list of dicts
            The column definitions to configure the DataTable in Dash, based on the columns in the consolidated DataFrame.

        Notes:
        ------
        - The function handles multiple Excel files and consolidates data from different sheets into one output file.
        - The function skips empty sheets and handles any errors encountered while processing files gracefully.
        - The output Excel file will be saved in the specified subfolder under `output_path`.
    """

    # Load data
    output_path =f"{output_path}\\{folder_in_output_path}"

    # Declare empty list and df
    rows = []
    df = pd.DataFrame()

    # Iterate through all files in the folder
    for file_name in os.listdir(output_path):
        # Check if the file is an Excel file
        if file_name.endswith(f"{folder_in_output_path}.xlsx") or file_name.endswith(f"{folder_in_output_path}.xls"):
            file_path = os.path.join(output_path, file_name)
            
            try:
                # Read the Excel file into a dictionary of DataFrames (all sheets)
                excel_data = pd.read_excel(file_path, sheet_name=None)

                # Iterate through sheets
                for sheet_name, df in excel_data.items():
                    
                    # Skip the empty sheet
                    if df.empty: continue
                    
                    # Modify the df to show concatinated allele values
                    df["A"] = df["A_1"] + "_" + df["A_2"]  # Concatinate alleles for both chromosome copies
                    df = df.drop(columns=["A_1","A_2"])  # Remove old columns
                    df["B"] = df["B_1"] + "_" + df["B_2"]
                    df = df.drop(columns=["B_1","B_2"])
                    df["C"] = df["C_1"] + "_" + df["C_2"]
                    df = df.drop(columns=["C_1","C_2"])
                    df["DQA1"] = df["DQA1_1"] + "_" + df["DQA1_2"]
                    df = df.drop(columns=["DQA1_1","DQA1_2"])
                    df["DQB1"] = df["DQB1_1"] + "_" + df["DQB1_2"]
                    df = df.drop(columns=["DQB1_1","DQB1_2"])
                    df["DRB1"] = df["DRB1_1"] + "_" + df["DRB1_2"]
                    df = df.drop(columns=["DRB1_1","DRB1_2"])
                    df["DPA1"] = df["DPA1_1"] + "_" + df["DPA1_2"]
                    df = df.drop(columns=["DPA1_1","DPA1_2"])
                    df["DPB1"] = df["DPB1_1"] + "_" + df["DPB1_2"]
                    df = df.drop(columns=["DPB1_1","DPB1_2"])
                    df["DRB3"] = df["DRB3_1"] + "_" + df["DRB3_2"]
                    df = df.drop(columns=["DRB3_1","DRB3_2"])
                    df["DRB4"] = df["DRB4_1"] + "_" + df["DRB4_2"]
                    df = df.drop(columns=["DRB4_1","DRB4_2"])
                    df["E"] = df["E_1"] + "_" + df["E_2"]
                    df = df.drop(columns=["E_1","E_2"])
                    df["F"] = df["F_1"] + "_" + df["F_2"]
                    df = df.drop(columns=["F_1","F_2"])
                    df["G"] = df["G_1"] + "_" + df["G_2"]
                    df = df.drop(columns=["G_1","G_2"]) 
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")


    # Update the file by removing the row from data added by default
    concatinated_df = df  # Create a consolidated DataFrame

    if concatinated_df.empty:
        rowData = []
        columnDefs = []
    else:
        concatinated_df = concatinated_df[concatinated_df["PATIENT_ID"] != "Sheet"].copy()  # Remove the default added sheet

        # # Extract the boolean value from the series
        # for column in concatinated_df.columns:
        #     concatinated_df[column] = concatinated_df[column].apply(lambda x: x.iloc[0] if isinstance(x, pd.Series) else x)

        rowData = concatinated_df.to_dict("records")
        columnDefs = [{"field": x, } for x in concatinated_df.columns]

        # Write to excel
        # concatinated_df.to_excel(f"{output_path}\\{folder_in_output_path}\\{folder_in_output_path}_concatinated.xlsx", index=False)  # Write to a new Excel file
        
        

    return rowData, columnDefs

