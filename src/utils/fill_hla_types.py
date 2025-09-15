# This file contains the fill_patient_per_hla_type function.

# Third party imports
import pandas as pd

# Built in imports
import os


def fill_hla_types_per_patient(output_path, folder_in_output_path):
    """
        Processes Excel files in the specified folder, extracting relevant HLA typing data
        for each patient from the sheets and consolidates this data into a new Excel file.

        For each Excel file in the provided folder, the function:
        1. Iterates over all sheets.
        2. Extracts data related to HLA typing (specifically for loci A, B, C, DQA1, DQB1, DRB1, etc.) 
        and stores the QC status for each chromosome copy.
        3. Flattens the extracted data into a single row per patient (sheet).
        4. Consolidates the rows into a new DataFrame.
        5. Removes any rows where the 'PATIENT_ID' is equal to "Sheet" (default sheets added by pandas).
        6. Writes the final DataFrame to a new Excel file with the specified folder name.

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
    output_path = output_path

    # Declare empty list
    rows = []

    # Iterate through all files in the folder
    for file_name in os.listdir(output_path):
        # Check if the file is an Excel file
        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            file_path = os.path.join(output_path, file_name)
            
            try:
                # Read the Excel file into a dictionary of DataFrames (all sheets)
                excel_data = pd.read_excel(file_path, sheet_name=None)

                # Iterate through sheets
                for sheet_name, df in excel_data.items():
                    
                    # Skip the empty sheet
                    if df.empty: continue
                    
                    # Flatten the sheet data into a single row
                    flattened_row = {
                        "PATIENT_ID": sheet_name,
                        "A_1":df[ (df['LOCUS']=="A") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "A_2":df[ (df['LOCUS']=="A") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "B_1":df[ (df['LOCUS']=="B") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "B_2":df[ (df['LOCUS']=="B") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "C_1":df[ (df['LOCUS']=="C") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "C_2":df[ (df['LOCUS']=="C") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "DQA1_1":df[ (df['LOCUS']=="DQA1") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "DQA1_2":df[ (df['LOCUS']=="DQA1") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "DQB1_1":df[ (df['LOCUS']=="DQB1") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "DQB1_2":df[ (df['LOCUS']=="DQB1") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "DRB1_1":df[ (df['LOCUS']=="DRB1") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "DRB1_2":df[ (df['LOCUS']=="DRB1") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "DPA1_1":df[ (df['LOCUS']=="DPA1") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "DPA1_2":df[ (df['LOCUS']=="DPA1") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "DPB1_1":df[ (df['LOCUS']=="DPB1") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "DPB1_2":df[ (df['LOCUS']=="DPB1") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "DRB3_1":df[ (df['LOCUS']=="DRB3") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "DRB3_2":df[ (df['LOCUS']=="DRB3") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "DRB4_1":df[ (df['LOCUS']=="DQA1") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "DRB4_2":df[ (df['LOCUS']=="DRB4") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "E_1":df[ (df['LOCUS']=="E") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "E_2":df[ (df['LOCUS']=="E") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "F_1":df[ (df['LOCUS']=="F") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "F_2":df[ (df['LOCUS']=="F") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                        "G_1":df[ (df['LOCUS']=="G") & (df["CHROMOSOME_COPY"]==int(1)) ].copy()["ALLELE"],
                        "G_2":df[ (df['LOCUS']=="G") & (df["CHROMOSOME_COPY"]==int(2)) ].copy()["ALLELE"],
                    }
                    rows.append(flattened_row)  
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")


    # Update the file by removing the row from data added by default
    consolidated_df = pd.DataFrame(rows)  # Create a consolidated DataFrame

    if consolidated_df.empty:
        rowData = []
        columnDefs = []
    else:
        consolidated_df = consolidated_df[consolidated_df["PATIENT_ID"] != "Sheet"].copy()  # Remove the default added sheet

        # Extract the boolean value from the series
        for column in consolidated_df.columns:
            consolidated_df[column] = consolidated_df[column].apply(lambda x: x.iloc[0] if isinstance(x, pd.Series) else x)
        rowData = consolidated_df.to_dict("records")
        columnDefs = [{"field": x, } for x in consolidated_df.columns]

        # Write to excel
        consolidated_df.to_excel(f"{output_path}\\{folder_in_output_path}\\{folder_in_output_path}.xlsx", index=False)  # Write to a new Excel file
        
        

    return rowData, columnDefs

