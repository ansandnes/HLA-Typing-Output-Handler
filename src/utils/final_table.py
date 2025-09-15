# This file contains the filter_data function

# Third party imports
import pandas as pd
from dash import dash_table


def final_table(data, filename) -> dash_table.DataTable:
    """  """

    # Extract sample name
    sample = str(filename).split("_R1")[0]

    # Extract the data from the data object and set datatypes
    data = pd.DataFrame.from_dict(data["props"]["data"])
    data["Chromosome"] = data["Chromosome"].astype(int)
    data["Locus"] = data["Locus"].astype(str)
    data["AverageCoverage"] = data["AverageCoverage"].astype(float)
    data["Q1"] = data["Q1"].astype(float)
    data["Q2"] = data["Q2"].astype(float)
    data["proportionkMersCovered"] = data["proportionkMersCovered"].astype(float)

    # Further analysis on the HLA types in question

    min_average_coverage = 2  # ambiguous value

    # Show data where (Q1 is not 1) AND (proportionkMersCovered is not 1)
    failed_qc = data[ (data["Q1"]!=float(1.0)) | (data["proportionkMersCovered"]!=int(1)) ].copy()
    failed_qc["QC_PASSED"] = (failed_qc["Q1"].astype(float) == float(1.0)) & (failed_qc["AverageCoverage"].astype(float) > min_average_coverage)  # If Q1 is not 1 and if AverageCoverage < 2, set False
    failed_qc = failed_qc[failed_qc["QC_PASSED"]==False]  # Filter to contain only the HLA types to fail the QC
    
    # Create final report
    report = data.loc[:,["Locus", "Chromosome", "Allele"]]  # create sub df
    report.columns = report.columns.str.upper() # rename columns to upper case
    report["CHROMOSOME_COPY"] = report["CHROMOSOME"]
    report = report.drop(columns="CHROMOSOME")
    report["CLASS"] = [2 if len(x) > 1 else 1 for x in report['LOCUS']]
    report['PATIENT_ID']=sample
    report['QC_PASSED'] = ~report["LOCUS"].isin(failed_qc["Locus"])  # Add a column representing quality control result
    report['QC_PASSED'] = report['QC_PASSED'].astype(str)  # Convert to string so excel doesn't translate to danish

    # Shuffle columns
    report = report[["PATIENT_ID", "LOCUS", "CLASS", "ALLELE", "CHROMOSOME_COPY", "QC_PASSED"]]
    
    return dash_table.DataTable(
        data=report.to_dict("records"),
        style_table={
            'width': '100%',
            'height': '100%',
            'borderRadius':'0.5rem',
            'overflowX': 'auto',
            'overflowY': 'auto',
            'maxHeight': '90vh',  # Optional: limit the height to the viewport
        },
        style_cell={
            'textAlign': 'center',
            'padding': '5px',
            'fontSize': '14px',
        },
        style_header={
            'height':'2rem',
            'backgroundColor': 'lightgray',
            'fontWeight': 'bold',
            'fontSize':'18'
        },
        style_data={
            'backgroundColor': 'white',
        }    
    )
