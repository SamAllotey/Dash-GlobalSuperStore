import os
from tokenize import group
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
    html.H1('GLOBAL SUPER STORE SALES ANALYSIS',  
    style = {"text-align": "center", "font-size":"100%", "color":"black"}), 
    dcc.Dropdown(id='store_dropdown', 
        options = [
            {'label': 'Best Selling & Most Profitable Category', 'value': 'Category'},
            {'label': 'Best Selling & Most Profitable Sub-Category', 'value': 'Sub_Category'},
            {'label': 'Top Selling Sub-category', 'value': 'Sub_Category'},
            {'label': 'Most Profitable Customer Segment', 'value': 'Segment'},
            {'label': 'Preferred Shipping Mode', 'value': 'Ship_Mode'},
            {'label': 'Most Profitable Region', 'value': 'Region'},
            {'label': 'City with highest number of sales', 'value': 'City'}          
    ],
    value = "Category",
      
      clearable = True,
      style = {"width": "50%"}
    ),


    dcc.Graph(
        id='bar_graph',
    )
    ])

@app.callback(
    Output(component_id='bar_graph', component_property='figure'),
    Input(component_id='store_dropdown',  component_property='value')
)


def update_graph(store_dropdown):
    dff = store_filedf 
    if store_dropdown == None:
        dff= store_filedf[store_filedf['Category'] == 'category']
        dff = store_filedf.groupby('Category').Profit_Margin.sum().reset_index()    
        pchart=px.pie(
            data_frame = dff, 
            names = store_dropdown, 
            hole=.3,
            width=800,                         
            height=600)
        return pchart
    elif store_dropdown == 'City':
        dff = store_filedf 
        dff= best_selling_pivot = pd.pivot_table(store_filedf[['City','Sales_Count']],
                                    index=['City'], aggfunc='count')
        best_selling_pivot=best_selling_pivot.reset_index()
        best_selling_pivot.sort_values(by=['Sales_Count'],ascending=False)
        figr = px.bar(store_filedf, x = 'City', y = 'Profit_Margin',
        title = "Bar graph for sales by City" , color = 'City')
        return figr
    else:
        store_dropdown == 'Category'
        dff = store_filedf 
        best_selling_pivot = pd.pivot_table(store_filedf[['Category','Sales','Profit_Margin','Product_Name']],
                    index=['Category','Profit_Margin','Product_Name'], aggfunc='sum')
        best_selling_pivot=best_selling_pivot.reset_index()
        best_selling_pivot.sort_values(by = ['Profit_Margin'],ascending=False).sort_values(by='Sales',ascending=False)
        pchart=px.pie(
                    data_frame = dff, 
                    names = store_dropdown, 
                    hole=.3,
                    template='presentation',   
                    width=800,                         
                    height=600)
                # pio.show(pchart)
        return pchart

if __name__ == '__main__':
    app.run_server(debug=True)
