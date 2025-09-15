# This file contains the app layout

# Third party imports
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Local imports
from src.utils.load_data import load_data
from src.utils.qc_report import qc_report
from src.utils.filter_data import filter_data
from src.utils.final_table import final_table
from src.utils.download_report_table import generate_excel_download_link
from src.utils.data_descriptions import analysis_strategy, further_analysis_strategy
from src.utils.output_path import output_path, folder_in_output_path
from src.utils.fill_hla_types_per_patient import fill_hla_types_per_patient
from src.utils.fill_hla_types_per_patient_concatinated import fill_hla_types_per_patient_concatinated


def layout():
    """ Returns the app layout """
    return [ 
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("HLA TYPING REPORT", id="title1"),
                    html.H3("Upload the *R1_bestGuess_G.txt file from the HLA-LA output"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                        className="upload-field",
                        multiple=False  # True allows multiple files to be uploaded
                    ),
                    dbc.Accordion([
                        dbc.AccordionItem(
                            id="loaded-data",
                            children=[],
                            title="Loaded Data"
                        ),
                        # dbc.AccordionItem(
                        #     id="analysis-strategy",
                        #     children=[analysis_strategy],
                        #     title="Analysis Strategy"
                        # ),
                        dbc.AccordionItem(
                            id="qc-report-plot",
                            children=[],
                            title="Quality Control Report"
                        ),
                        # dbc.AccordionItem(
                        #     id="further-analysis-strategy",
                        #     children=[further_analysis_strategy],
                        #     title="Further Analysis Strategy"
                        # ),
                        dbc.AccordionItem(
                            id="filtered-data",
                            children=[],
                            title="Filtered Data"
                        ),
                        dbc.AccordionItem(
                            id="final-report-table",
                            children=[],
                            title="Final Report Table"
                        ),
                    ], always_open=True, style={"margin-bottom":"2rem"}),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Button("Download Final Report Table (.xlsx)", id="download-button", className="download-excel-btn"),
                    dbc.Alert(id="download-alert", is_open=False, dismissable=True, color="", children=[]),
                ])
            ]),
            # dbc.Row([
            #     dbc.Col([

            #         html.H3("HLA Types per Patient - Chromosome Copies Concatinated"),
            #         dbc.Accordion([
            #             dbc.AccordionItem([
            #                 dag.AgGrid(
            #                     id="ag-grid2",
            #                     rowData=[],
            #                     columnDefs=[],
            #                     defaultColDef={
            #                         "resizable": True, "sortable": True, "filter": True, "hide": False,
            #                         "flex": 1,  # Let columns grow
            #                         "minWidth": 200,  # Set minimum column width
            #                     },  # Default column properties
            #                     style={"height": "400px", "width": "100%"},  # Style grid dimensions
            #                     # exportDataAsCsv=True,
            #                     # csvExportParams={"allColumns":True, "fileName": "filtered_patients_hla_types.csv", "columnSeparator":","},
            #                 ),
            #             ], title="HLA Types per Patient - Chromosome Copies Concatinated"),
            #         ], always_open=True, style={"margin-bottom":"2rem"}),

            #         html.H3("HLA Types per Patient - Chromosome Copies Separated"),
            #         dbc.Accordion([
            #             dbc.AccordionItem([
            #                 dag.AgGrid(
            #                     id="ag-grid",
            #                     rowData=[],
            #                     columnDefs=[],
            #                     defaultColDef={
            #                         "resizable": True, "sortable": True, "filter": True, "hide": False,
            #                         "flex": 1,  # Let columns grow
            #                         "minWidth": 120,  # Set minimum column width
            #                     },  # Default column properties
            #                     style={"height": "400px", "width": "100%"},  # Style grid dimensions
            #                     # exportDataAsCsv=True,
            #                     # csvExportParams={"allColumns":True, "fileName": "filtered_patients_hla_types.csv", "columnSeparator":","},
            #                 ),
            #             ], title="HLA Types per Patient - Chromosome Copies Separated"),
            #         ], start_collapsed=True, always_open=True, style={"margin-bottom":"2rem"}),
            #     ])
            # ], style={"margin-bottom":"6rem"})
        ])
    ]


# Callback for upload-data
@callback(
    [Output(component_id="loaded-data", component_property="children")],
    [Input(component_id="upload-data", component_property="contents")],
    [State(component_id="upload-data", component_property="filename")],
    prevent_initial_call=True,
)
def load_data_to_accordion_item1(uploaded_data, filename):
    """  """
    return [load_data(uploaded_data, filename)]


# Callback for the Quality Control Report
@callback(
    [Output(component_id="qc-report-plot", component_property="children")],
    [Input(component_id="loaded-data", component_property="children")],
    [State(component_id="upload-data", component_property="filename")],
    prevent_initial_call=True,
)
def create_qc_report(data, filename):
    """  """

    # Create report plot
    report = qc_report(data, filename)

    return [report]


# Callback for filtered-data
@callback(
    [Output(component_id="filtered-data", component_property="children")],
    [Input(component_id="loaded-data", component_property="children")],
    prevent_initial_call=True,
)
def create_filter_data(uploaded_data):
    """  """
    return [filter_data(uploaded_data)]


# Callback for final-report-table
@callback(
    [Output(component_id="final-report-table", component_property="children")],
    [Input(component_id="loaded-data", component_property="children")],
    [State(component_id="upload-data", component_property="filename")],
    prevent_initial_call=True,
)
def create_final_table(uploaded_data, filename):
    """  """
    return [final_table(uploaded_data, filename)]


@callback(
    [Output(component_id="download-alert", component_property="children"),
    Output(component_id="download-alert", component_property="color"),
    Output(component_id="download-alert", component_property="is_open")],
    [Input(component_id="download-button", component_property="n_clicks")],
    [State(component_id="final-report-table", component_property="children"),
    State(component_id="upload-data", component_property="filename")],
    prevent_initial_call=True,
)
def download_excel(n_clicks, data, filename):

    if n_clicks:
        list_output = generate_excel_download_link(data, filename, output_path)

        # Extract data from output
        alert = list_output[0]
        color = list_output[1]
        # Set whether Alert component is visible or not.
        is_open = True

        return [alert, color, is_open] 

        
# @callback(
#     [
#         Output(component_id="ag-grid", component_property="rowData"),
#         Output(component_id="ag-grid", component_property="columnDefs"),
#         Output(component_id="ag-grid2", component_property="rowData"),
#         Output(component_id="ag-grid2", component_property="columnDefs")
#     ],
#     [Input(component_id="title1", component_property="children")],
#     prevent_initial_call=False,
# )
# def create_patient_hla_types(trigger):
#     """  """
    
#     # Load data from output_path
#     rowData1, columnDefs1 = fill_hla_types_per_patient(output_path, folder_in_output_path)  # Returns rowData and columnDefs
#     rowData2, columnDefs2 = fill_hla_types_per_patient_concatinated(output_path, folder_in_output_path)

#     return  [rowData1, columnDefs1, rowData2, columnDefs2]

