
# Third party imports
import pandas as pd
from dash import dash_table
# Built in imports
import base64

def load_data(contents, filename) -> dash_table.DataTable:
    """  """

    if contents is None:
        return "No file uploaded yet."

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'text' in content_type or filename.endswith('.txt'):
            # Process TXT file
            decoded_text = decoded.decode('utf-8')
            lines = decoded_text.splitlines()
            columns = lines[0].split('\t')

            data=[]
            for line in lines[1:]:
                # Split the line based on a delimiter or custom logic
                fields = line.strip().split('\t')
                data.append(fields)

            df = pd.DataFrame(data=data, columns=columns)
            return dash_table.DataTable(
                data=df.to_dict("records"),
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
        else:
            return "Unsupported file format."
    except Exception as e:
        return [f"An error occurred while processing the file: {str(e)}"]



