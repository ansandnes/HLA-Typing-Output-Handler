import dash
import dash_bootstrap_components as dbc

from src.core.layout import layout

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.title = "HLA-typing"  # Sets the browser tab title

# Define the app layout
app.layout = layout()


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)

