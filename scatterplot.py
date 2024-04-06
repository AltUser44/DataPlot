import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the dataset
url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv"
df = pd.read_csv(url)

# Create the choropleth map
map_fig = px.choropleth(df, locations="CODE",
                        color="GDP (BILLIONS)",
                        hover_name="COUNTRY",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title="2014 Global GDP")
map_fig.update_layout(paper_bgcolor="#333", font_color="white")

# Create the initial bar chart with a dark theme
bar_fig = px.bar(df, x='COUNTRY', y='GDP (BILLIONS)',
                 title="GDP by Country",
                 labels={'GDP (BILLIONS)': 'GDP in Billions', 'COUNTRY': 'Country'})
bar_fig.update_layout(yaxis_range=[0, 2000], xaxis={'categoryorder': 'total descending'}, paper_bgcolor="#333", font_color="white")

# Define the layout of the dashboard with a dark grey background
app.layout = html.Div([
    html.H1("2014 World GDP Visualization", style={'color': 'white'}),
    dcc.Graph(
        id='gdp-choropleth',
        figure=map_fig,
        config={"staticPlot": False}  # Enable interactivity
    ),
    dcc.Graph(
        id='gdp-bar-chart',
        figure=bar_fig
    )
], style={'backgroundColor': '#333', 'color': 'white', 'padding': '10px'})

# Callback to update the bar chart based on the map click
@app.callback(
    Output('gdp-bar-chart', 'figure'),
    [Input('gdp-choropleth', 'clickData')]
)
def update_bar_chart(clickData):
    country_selected = None
    if clickData is not None:
        country_selected = clickData['points'][0]['hovertext']

    # Set the color of the selected country's bar to red, others to blue
    colors = ['red' if country == country_selected else 'blue' for country in df['COUNTRY']]
    fig = px.bar(df, x='COUNTRY', y='GDP (BILLIONS)',
                 title="GDP by Country",
                 labels={'GDP (BILLIONS)': 'GDP in Billions', 'COUNTRY': 'Country'})
    fig.update_traces(marker_color=colors)
    fig.update_layout(yaxis_range=[0, 2000], xaxis={'categoryorder': 'total descending'}, paper_bgcolor="#333", font_color="white")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
