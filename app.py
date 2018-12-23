
# coding: utf-8

# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
    
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df = df[df['UNIT'] == "Current prices, million euro"]
df = df[~df['GEO'].str.contains('Euro')]
locs = df['GEO'].unique()
kpis = df['NA_ITEM'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'xaxis-column',
                options = [{'label': i, 'value': i} for i in kpis],
                value = 'Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle={'display': 'inline-block'}
            ),
        ],
        style = {'width': '48%', 'display': 'inline-block', 'padding': 10}),

        html.Div([
            dcc.Dropdown(
                id = 'yaxis-column',
                options = [{'label': i, 'value': i} for i in kpis],
                value = 'Value added, gross'
            ), 
        ],style = {'width': '48%', 'float': 'right', 'display': 'inline-block','padding': 10})
    ]),

    dcc.Graph(id = 'indicator-graphic'),

    dcc.Slider(
        id = 'year--slider',
        min = df['TIME'].min(),
        max = df['TIME'].max(),
        value = df['TIME'].max(),
        step = None,
        marks = {str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    html.H1('\n'),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'country',
                options = [{'label': i, 'value': i} for i in locs],
                value = 'Bulgaria'
            ),
            
        ],
        style = {'width': '48%', 'display': 'inline-block', 'padding': 15}),

        html.Div([
            dcc.Dropdown(
                id = 'yaxis-column-b',
                options = [{'label': i, 'value': i} for i in kpis],
                value = 'Gross domestic product at market prices'
            ),
            
        ],style = {'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': 15})
    ]),
    dcc.Graph(id = 'indicator-graphic-b')
    
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('xaxis-type', 'value')])

def refreshgr(xaxis_column_name, yaxis_column_name,
                 year_value, xaxis_type):
    df2 = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x = df2[(df2['NA_ITEM'] == xaxis_column_name) &(df2['GEO'] == str(i) )]['Value'],
            y = df2[(df2['NA_ITEM'] == yaxis_column_name) &(df2['GEO'] == str(i))]['Value'],
            text = df2[df2['GEO'] == str(i)]['GEO'],
            mode = 'markers',
            marker = {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name = i[:20]
            
        )for i in df2.GEO.unique()
                ],
        'layout': go.Layout(
            xaxis = {
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log' 
            },
            yaxis = {
                'title': yaxis_column_name,
                'type': 'linear' 
            },
            margin = {'l': 90, 'b': 90, 't': 70, 'r': 50},
            hovermode = 'closest',
            title = 'Overview of EU countries'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic-b', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis-column-b', 'value')])

def refreshgr2(country_name, yaxis_column_b_name,):
    df2 = df[df['GEO'] == country_name]
    
    return {
        'data': [go.Scatter(
            x = df2[df2['NA_ITEM'] == yaxis_column_b_name]['TIME'],
            y = df2[df2['NA_ITEM'] == yaxis_column_b_name]['Value'],
            text = df2[df2['NA_ITEM'] == yaxis_column_b_name]['Value'],
            mode = 'lines'
            
            
        )],
        'layout': go.Layout(
            xaxis = {
                'title': 'YEAR',
                'type': 'linear' 
            },
            yaxis = {
                'title': yaxis_column_b_name,
                'type': 'linear' 
            },
            margin = {'l': 90, 'b': 90, 't': 70, 'r': 50},
            hovermode = 'closest',
            title = 'Overview of selected EU country'
        )
    }


if __name__ == '__main__':
    app.run_server()

