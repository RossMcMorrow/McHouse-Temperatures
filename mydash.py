
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests


MainDataSet = pd.read_csv("FinalData.csv")
#MainDataSet = pd.read_csv("C:/Users/rmcmorrow/Google Drive/Masters/Course/Data Analtyics and Visulisation/Project/FinalData/FinalData.csv")
MainDataSet.index =  pd.to_datetime(MainDataSet['Date'] , format = '%d/%m/%Y %H:%M')
df = MainDataSet.drop(['Unnamed: 0', 'Date'], axis=1)
years = pd.DatetimeIndex(df.index).year.unique()
years = [str(x) for x in years]
Dyears = { i : years[i] for i in range(0, len(years) ) }
the_year = 2016
run_df = df[(df.index > '1/01/{} 00:00'.format(str(years[0]))) & (df.index <= '11/01/{} 00:00'.format(str(the_year )))]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

############################### Declare  DF and Figs #######################################################
wind = run_df['wddir'].value_counts().to_frame()
wind = wind.sort_index(axis=0, level=None, ascending=True, )
thedate = run_df.index
discipt = {'wdsp': 'Wind Speed', 'wddir': 'Wind Direction in Degrees', 'wetb': 'WetBulb Temperature',
           'dewpt': 'Dew Point', \
           'rhum': 'Relative Humididty', 'Sitting_Room': 'Inside Temperature', 'BoilerOn': 'Boiler On', \
           'Sp_Temperature': 'Stat Set Point', 'temp': 'Outside Temperature'}

fig = go.Figure()
selected = ['temp', 'Sitting_Room']
for i in selected:
    y0 = run_df['{}'.format(i)]
    thename = i
    fig.add_trace(go.Scatter(x=thedate, y=y0, mode='lines', name=discipt.get(i))),

fig2 = go.Figure()
fig2.add_trace(go.Barpolar(r=wind.wddir, marker_color='rgb(33,208,57)'))
fig2.update_layout(title='Wind Speed Distribution', font_size=16, legend_font_size=16, polar_angularaxis_rotation=90, )

fig3 = go.Figure()
y03 = run_df['Sitting_Room'].subtract(run_df['temp'], fill_value=1)

y03[y03 < 0] = 0

fig3.add_trace(go.Scatter(x=thedate, y=y03, mode='lines', name='Temperature Diffierance', fill='tozeroy', \
                          fillcolor='#FF7E00', line=dict(color='firebrick', width=1)))

data = requests.get(
    "http://api.openweathermap.org/data/2.5/weather?lat=54.281688&lon=-8.480222&appid=27f70634bcb390ac526971b077f7acfd")
dataJ = data.json()
Wdis = dataJ["weather"][0]['description']
cTemp = round(dataJ['main']['temp'] - 273.15)
cWindsp = round(dataJ['wind']['speed'])
cWinddir = round(dataJ['wind']['deg'])

########################### Dashboard Layout ################################################################################
app.layout = html.Div([
    html.Div([html.H3('Ross McMorrow - S00002161 Interactive Dashboard', style={'border': '1px solid #cfcfcf', \
                                                                                'text-align': 'center',
                                                                                'background-color': '#0e508a',
                                                                                'margin-top': '0px',
                                                                                'margin-bottom': '0px',
                                                                                'color': 'white'})]),
    html.Div(children=[
        html.Div(children=[
            html.H4('Temperature Differential', style={'border': '1px solid #cfcfcf', 'background-color': '#1373c7fa', \
                                                       'margin-top': '0px', 'margin-bottom': '0px', 'color': 'white'}),
            dcc.Graph(id='diff-chart', figure=fig3, style={'border': '1px solid #cfcfcf'})
        ], style={'text-align': 'center', 'display': 'inline-block', 'width': '35%'}),

        html.Div(children=[
            html.H4('Main Graph', style={'border': '1px solid #cfcfcf', 'background-color': '#1373c7fa',
                                         'margin-top': '0px', 'color': 'white', 'margin-bottom': '0px'}),
            dcc.Graph(id='example-graph', figure=fig, style={'border': '1px solid #cfcfcf'}),
        ], style={'text-align': 'center', 'display': 'inline-block', 'width': '65%'}),

    ]),

    html.Div(children=[
        dcc.Slider(id='year-slider', min=0, max=len(years) - 1, step=None, marks=Dyears, value=3, ),
        html.Label('Choose Perameters', style={'font-weight': 'bold', 'text-align': 'center'}),
        dcc.Dropdown(id="measure-select", options=[
            {'label': 'Inside Temperature', 'value': 'Sitting_Room'},
            {'label': 'Outside Temperature', 'value': 'temp'},
            {'label': 'Boiler On', 'value': 'BoilerOn'},
            {'label': 'Wind Speed', 'value': 'wdsp'},
            {'label': 'WetBulb Temp', 'value': 'wetb'},
            {'label': 'Dew Point', 'value': 'dewpt'},
            {'label': 'Relative Humididty', 'value': 'rhum'},
            {'label': 'Stat Set Point', 'value': 'Sp_Temperature'},
            {'label': 'Wind Direction', 'value': 'wddir'},
        ],
                     value=['temp', 'Sitting_Room', ],
                     multi=True, style={'width': '100%', 'text-align': 'center'}),
    ], style={'margin-top': '20px'}),

    html.Div(children=[
        html.H4('Wind-Rose Chart', style={'width': '100%', 'text-align': 'center', 'margin-left': '0', \
                                          'display': 'block', 'background': '#e5ecf6', 'height': '42px',
                                          'margin': '0px 0px 0px 0px',
                                          'padding-top': '18px', 'background': '#e5ecf6', 'height': '42px',
                                          'padding-top': '18px'}),

        dcc.Graph(id='rose-chart', figure=fig2, style={'width': '100%', 'display': 'inline-block', 'margin-left': '0',
                                                       'border': '1px solid #cfcfcf',
                                                       'border-radius': '2px', 'height': '456.995px',
                                                       'background': '#f7f7f7',
                                                       }), ], style={'text-align': 'center', \
                                                                     'display': 'inline-block', 'width': '45%'}),

    html.Div(children=[
        html.Div([html.H4('The Current Weather', style={'width': '100%', 'text-align': 'center', 'margin-left': '0', \
                                                        'display': 'block', 'background': '#e5ecf6', 'height': '42px',
                                                        'margin': '0px 0px 0px 0px',
                                                        'padding-top': '18px', 'background': '#e5ecf6',
                                                        'height': '42px', 'padding-top': '18px'})]),
        html.Div([
            html.H4(""),
            html.H6("It is Currently", style={'margin-left': '20px', 'text-align': 'left'}), html.H4(Wdis, style={ \
                'font-weight': '800', 'font-size': '30px'}),

            html.H6("Current Temperature", style={'margin-left': '20px', 'text-align': 'left'}), html.H4(cTemp, style={ \
                'font-weight': '800', 'font-size': '30px'}),
            html.H6("Current Wind Speed", style={'margin-left': '20px', 'text-align': 'left'}), html.H4(cWindsp, style={ \
                'font-weight': '800', 'font-size': '30px'}),
            html.H6("Current Wind Direction in Degrees", style={'margin-left': '20px', 'text-align': 'left'}),
            html.H4(cWinddir, style={ \
                'font-weight': '800', 'font-size': '30px'}), ], style= \
            {'border': '1px solid #cfcfcf', 'padding-top': '19px', 'height': '436px' \
 \
             }),

    ], style={'text-align': 'center', \
              'border': '1px solid #cfcfcf', 'position': 'absolute', \
              'display': 'inline-block', 'width': '54%', }),

], style={'border': '1px solid #cfcfcf'})


############################# CallsBack #######################################################################

@app.callback(
    [Output('example-graph', 'figure'),
     Output('rose-chart', 'figure'),
     Output('diff-chart', 'figure')],
    [Input('year-slider', 'value'),
     Input('measure-select', 'value')]
)

########################## CallBack Function #################################################################
def mainGraph(yearin, selected1):
    newYear = Dyears.get(yearin)
    run_df = df[(df.index > '11/01/{} 00:00'.format(str(years[0]))) & (df.index <= '11/01/{} 00:00'.format(newYear))]
    wind = run_df['wddir'].value_counts().to_frame()
    wind = wind.sort_index(axis=0, level=None, ascending=True, )

    # print(yearin,selected1)
    thedate = run_df.index
    selected = selected1
    fig = go.Figure()
    for i in selected:
        if i == 'BoilerOn':
            # print('y')
            y0 = run_df['{}'.format(i)] // 5
        else:
            # print('N')
            y0 = run_df['{}'.format(i)]
        thename = i
        fig.add_trace(go.Scatter(x=thedate, y=y0, mode='lines', name=discipt.get(i))),

    fig2 = go.Figure()
    fig2.add_trace(go.Barpolar(r=wind.wddir, marker_color='rgb(33,208,57)'))
    fig2.update_layout(title='Wind Speed Distribution', font_size=16, legend_font_size=16,
                       polar_angularaxis_rotation=90, )

    fig3 = go.Figure()
    y03 = run_df['Sitting_Room'].subtract(run_df['temp'], fill_value=1)

    y03[y03 < 0] = 0

    fig3.add_trace(go.Scatter(x=thedate, y=y03, mode='lines', name='Temperature Diffierance', \
                              fill='tozeroy', fillcolor='#FF7E00', line=dict(color='firebrick', width=1)))

    return fig, fig2, fig3

######################################################################################################
if __name__ == '__main__':
    app.run_server(debug=False)
