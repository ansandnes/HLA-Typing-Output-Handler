# This file contains function that downloads the final report to excel

# Third party imports
import pandas as pd

# Built in imports
import os
from openpyxl import Workbook

def generate_excel_download_link(report, filename, output_path):
    """
    Adds a sheet to an existing Excel file or creates a new file and adds the sheet.
    
    Parameters:
        report (dict): The data to write, in the format of a Dash DataTable's `data` property.
        filename (str): The base filename to extract sample and trial IDs.
        output_path (str): The directory where the Excel file is stored or created.

    Returns:
        str: Success message or error message.
    """
    try:
        # Extract sample and trial IDs
        sample_id = str(filename).split("_R1_")[0]
        trial_id = sample_id.split("_")[0]
        
        # Declare file_path
        file_path = os.path.join(output_path, f"{trial_id}_hla_typing_report.xlsx")

        # Convert report from dict to DataFrame
        report_df = pd.DataFrame.from_dict(report["props"]["data"])
        
        # Validate output path
        if not os.path.exists(file_path):
            # Set the full file path
            file_path = os.path.join(output_path, f"{trial_id}_hla_typing_report.xlsx")
        
    except Exception as e:
        file_path=""
        color="warning"  # Set color of alert label
        return [f"An error occurred: {str(e)}", color]
    
    try:
        # If the file path exists
        if os.path.exists(file_path):
            # Add sheet to existing file
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                report_df.to_excel(writer, sheet_name=sample_id, index=False)
            color="success"  # Set color of alert label
        else:
            # Create a new file. This will create a default first sheet.
            wb = Workbook()
            wb.save(file_path)

            # Add new sheet
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                report_df.to_excel(writer, sheet_name=sample_id, index=False)
            color="success"  # Set color of alert label
        
        return [f"Success! The sheet '{sample_id}' was added to the file: {file_path}", color]
    except Exception as e:
        color="warning"  # Set color of alert label
        return [f"An error occurred: {str(e)}", color]
    
