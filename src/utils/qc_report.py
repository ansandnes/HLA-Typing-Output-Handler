# This file contains the Quality Control Report plot

# Third party imports
import pandas as pd
from dash import dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Local imports
from src.utils.hovertemplate import hovertemplate1, hovertemplate2

def qc_report(data0, filename) -> dcc.Graph:
    """  """
    # Extract the data from the data object and set datatypes
    data = pd.DataFrame.from_dict(data0["props"]["data"])
    data["Chromosome"] = data["Chromosome"].astype(int)
    data["Locus"] = data["Locus"].astype(str)
    data["AverageCoverage"] = data["AverageCoverage"].astype(float)
    data["Q1"] = data["Q1"].astype(float)
    data["Q2"] = data["Q2"].astype(float)
    data["proportionkMersCovered"] = data["proportionkMersCovered"].astype(float)
    
    # Extract sample name
    sample = str(filename).split("_R1")[0]

    # Create figure

    # Create a subplot
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=["Chromosome Copy 1", "Chromosome Copy 2", "", ""],
        x_title="Locus",
        horizontal_spacing=0.05,
        vertical_spacing=0.1,
        shared_xaxes=False,
        shared_yaxes=False,
    )

    # Update layout
    fig.update_layout(
        title=f"Quality Control Report of {sample}",
        # xaxis_title="Locus",
        yaxis_title="Average Coverage",
        yaxis3_title="Quality Score",
        # yaxis1_type="log",
        showlegend=True,
        template="plotly_white",
        height=600,
        width=1200,
        # annotations=annotations,
        legend=dict(
            orientation='h',  # Horizontal legend
            x=0.5,  # Position the legend in the center
            xanchor='center',  # Anchors the legend to the center of x
            y=-0.2,  # Position the legend below the plot
            yanchor='bottom',  # Anchors the legend to the bottom of y
        ),
        hoverlabel=dict(
            # bgcolor='white',  # Background color of the hover label
            bordercolor='white',  # Set the border color to match the background (removes border)
            font=dict(
                size=14,  # Font size of the hover text
                color="black"
            ),
        )
    )

    # Declare hoverdata for Chromosome copy 1 and 2
    customdata1=list(
        zip(
            data[data["Chromosome"]==int(1)]["Chromosome"],
            data[data["Chromosome"]==int(1)]["Allele"],
            data[data["Chromosome"]==int(1)]["AverageCoverage"],
            data[data["Chromosome"]==int(1)]["Q1"],
            data[data["Chromosome"]==int(1)]["proportionkMersCovered"],
        )
    )
    # Declare hoverdata
    customdata2=list(
        zip(
            data[data["Chromosome"]==int(2)]["Chromosome"],
            data[data["Chromosome"]==int(2)]["Allele"],
            data[data["Chromosome"]==int(2)]["AverageCoverage"],
            data[data["Chromosome"]==int(2)]["Q1"],
            data[data["Chromosome"]==int(2)]["proportionkMersCovered"],
        )
    )

    # Row 1 - Average Coverage
    for i in range(2):

        if int(i) == int(0):
            showlegend = True
            customdata = customdata1
            hovertemplate = hovertemplate1
        else:
            showlegend = False
            customdata = customdata2
            hovertemplate = hovertemplate2
        
        fig.add_trace(
            go.Bar(
                x=data[data["Chromosome"]==int(i+1)]["Locus"],
                y=data[data["Chromosome"]==int(i+1)]["AverageCoverage"],
                marker=dict(color="skyblue"),
                name="Average Coverage",
                showlegend=showlegend,
                opacity=0.8,
                customdata=customdata,
                hovertemplate=hovertemplate,
                text=round(data[data["Chromosome"]==int(i+1)]["AverageCoverage"], ndigits=2),
            ),
            row=1, col=i+1,
        )

    # Row 2 - Q1
    for i in range(2):

        if int(i) == int(0):
            showlegend = True
            customdata = customdata1
            hovertemplate = hovertemplate1
        else:
            showlegend = False
            customdata = customdata2
            hovertemplate = hovertemplate2

        fig.add_trace(
            go.Scatter(
                x=data[data["Chromosome"]==int(i+1)]["Locus"],
                y=data[data["Chromosome"]==int(i+1)]["Q1"],
                marker=dict(color="green"),
                name="Q1",  # Quality Score 1
                showlegend=showlegend,
                opacity=0.5,
                customdata=customdata,
                hovertemplate=hovertemplate,
            ),
            row=2, col=i+1,
        )

    # Row 2 - proportionkMersCovered
    for i in range(2):
        
        if int(i) == int(0):
            showlegend = True
            customdata = customdata1
            hovertemplate = hovertemplate1
        else:
            showlegend = False
            customdata = customdata2
            hovertemplate = hovertemplate2

        fig.add_trace(
            go.Scatter(
                x=data[data["Chromosome"]==int(i+1)]["Locus"],
                y=data[data["Chromosome"]==int(i+1)]["proportionkMersCovered"],
                marker=dict(color="orange"),
                name="proportionkMersCovered",
                showlegend=showlegend,
                opacity=0.5,
                customdata=customdata,
                hovertemplate=hovertemplate,
            ),
                row=2, col=i+1,
        )

    # Wrap the plot inside a Graph component
    return dcc.Graph(
        figure=fig,
        config={
            'displayModeBar': True,  # Show the mode bar (zoom, pan, etc.)
            'scrollZoom': True,      # Enable zooming with mouse scroll
            'displaylogo': False,    # Hide the Plotly logo
            'editable': False        # Make the graph non-editable
        }
    )

