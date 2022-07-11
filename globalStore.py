import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, callback, Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

path = 'Superstore'
store_file = os.path.join(path, 'ProjSuperstore.csv')
store_filedf = pd.read_csv(store_file)

# print ('++++++ Global Store Table +++++')
# print(store_filedf.info())


app.layout = html.Div(children=[
    html.H1('Global Super Store Sales'),   
    dcc.Dropdown(id='store_dropdown', 
        options = [
            # {'label': i, 'value': i} for i in store_filedf['Product_Name'].unique()
            {'label': 'Product Category', 'value': 'Category'},
            {'label': 'Product Sub-category', 'value': 'Sub_Category'},
            {'label': 'Product Segment', 'value': 'Segment'},
            {'label': 'Shipping Mode', 'value': 'Ship_Mode'},
            {'label': 'Region', 'value': 'Region'},
            {'label': 'City', 'value': 'City'}
              
    ],
      value = "Category",
      multi = False,
      clearable = False,
      style = {"width": "50%"}
    ),


    dcc.Graph(
        id='bar_graph',
    )
    ])

@app.callback(
    Output('bar_graph', 'figure'),
    # State('product-dropdown', 'value'),
    # State('category-dropdown', 'value'),
    Input(component_id='store_dropdown',  component_property='value')

)

def update_graph(store_dropdown):
    dff = store_filedf 

    piechart=px.pie(
            data_frame=dff,
            names=store_dropdown,
            hole=.3,
            )

    return (piechart)

if __name__ == '__main__':
    app.run_server(debug=True)