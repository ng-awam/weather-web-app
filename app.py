#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import datetime
from plotly.subplots import make_subplots

import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt

# In[22]:


import plotly.graph_objs as go



# In[23]:


end_date = datetime.datetime.today().strftime('%Y-%m-%d')


# In[ ]:





# ### Read latest historical and forecast data

# In[16]:

weather_state_scaled_precip1 = pd.read_csv('https://raw.githubusercontent.com/ng-awam/weather-web-app/main/precip.csv',index_col=0)
weather_state_scaled_precip1.index = pd.to_datetime(weather_state_scaled_precip1.index)
weather_state_scaled_precip1 = weather_state_scaled_precip1.rename(columns = {'Date.1' : 'Date'})
weather_state_scaled_precip1.index.name = None







# In[18]:


weather_state_scaled_precip_region = weather_state_scaled_precip1.groupby(['Region','Date']).mean().reset_index()

weather_state_scaled_precip1.index = weather_state_scaled_precip1['Date']
weather_state_scaled_precip_region.index = weather_state_scaled_precip_region['Date']


# In[ ]:





# In[24]:


regions = weather_state_scaled_precip_region['Region'].unique()
fig_precip = make_subplots(rows=1,cols=1)
for i in range(len(regions)):
    temp = weather_state_scaled_precip_region[weather_state_scaled_precip_region['Region'] == regions[i]]

    temp1 = temp.rolling(7).mean().dropna(subset=['precip_norm'])
    fig_precip.add_trace(go.Scatter(x=temp1.index, y= temp1['precip_norm'],name=regions[i]),row=1,col=1)

fig_precip.add_vline(x=end_date, line_width=3, line_dash="dash", line_color="black")
fig_precip.update_layout(height=600,width=900,
    title='7 day average of Normalized precipitation (kg/m2) - US Regions ')
fig_precip.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.2,
    xanchor="right",
    x=0.9
))


# In[25]:


weather_state_scaled_ws1 = pd.read_csv('https://raw.githubusercontent.com/ng-awam/weather-web-app/main/ws.csv',index_col=0)
weather_state_scaled_ws1.index = pd.to_datetime(weather_state_scaled_ws1.index)
weather_state_scaled_ws1 = weather_state_scaled_ws1.rename(columns = {'Date.1' : 'Date'})
weather_state_scaled_ws1.index.name = None








# In[27]:


weather_state_scaled_ws_region = weather_state_scaled_ws1.groupby(['Region','Date']).mean().reset_index()

weather_state_scaled_ws1.index = weather_state_scaled_ws1['Date']
weather_state_scaled_ws_region.index = weather_state_scaled_ws_region['Date']


# In[28]:


regions = weather_state_scaled_ws_region['Region'].unique()
fig_ws = make_subplots(rows=1,cols=1)
for i in range(len(regions)):
    temp = weather_state_scaled_ws_region[weather_state_scaled_ws_region['Region'] == regions[i]]

    temp1 = temp.rolling(7).mean().dropna(subset=['ws_norm'])
    fig_ws.add_trace(go.Scatter(x=temp1.index, y= temp1['ws_norm'],name=regions[i]),row=1,col=1)

fig_ws.add_vline(x=end_date, line_width=3, line_dash="dash", line_color="black")
fig_ws.update_layout(height=600,width=900,
    title='7 day average of Normalized wind speed (m/s) - US Regions ')
fig_ws.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.2,
    xanchor="right",
    x=0.9
))


# In[29]:


weather_state_scaled_temp1 = pd.read_csv('https://raw.githubusercontent.com/ng-awam/weather-web-app/main/temp.csv',index_col=0)
weather_state_scaled_temp1.index = pd.to_datetime(weather_state_scaled_temp1.index)
weather_state_scaled_temp1 = weather_state_scaled_temp1.rename(columns = {'Date.1' : 'Date'})
weather_state_scaled_temp1.index.name = None




# In[ ]:





# In[30]:


weather_state_scaled_temp_region = weather_state_scaled_temp1.groupby(['Region','Date']).mean().reset_index()

weather_state_scaled_temp1.index = weather_state_scaled_temp1['Date']
weather_state_scaled_temp_region.index = weather_state_scaled_temp_region['Date']


# In[31]:


regions = weather_state_scaled_temp_region['Region'].unique()
fig_temp = make_subplots(rows=1,cols=1)
for i in range(len(regions)):
    temp = weather_state_scaled_temp_region[weather_state_scaled_temp_region['Region'] == regions[i]]

    temp1 = temp.rolling(7).mean().dropna(subset=['temp_norm'])
    fig_temp.add_trace(go.Scatter(x=temp1.index, y= temp1['temp_norm'],name=regions[i]),row=1,col=1)
fig_temp.add_vline(x=end_date, line_width=3, line_dash="dash", line_color="black")
fig_temp.update_layout(height=600,width=900,
    title='7 day average of Normalized Temperature (degree C) - US Regions ')
fig_temp.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.2,
    xanchor="right",
    x=0.9
))


# ### Build choropleth maps

# In[34]:


weather_state_forecast_scaled_precip = pd.read_csv('https://raw.githubusercontent.com/ng-awam/weather-web-app/main/precip_forecast.csv',index_col=0)




df_map_precip = weather_state_forecast_scaled_precip.copy()
df_map_precip.precip_norm=df_map_precip.precip_norm.mask(df_map_precip.precip_norm.lt(0),0)


# In[38]:


fig_map1 = px.choropleth(
    data_frame=df_map_precip,
    locationmode='USA-states',
    locations='State',
    scope="usa",
    color='precip_norm',
    hover_data=['precip_norm'],
    color_continuous_scale=px.colors.sequential.Blues,
    labels={'precip_norm': 'Precipitaion (kg/m2)'},
    title = "Evolution of normalized precipitation (kg/m2) forecast",
    animation_frame = "forecast_day"
)






# In[39]:


weather_state_forecast_scaled_ws = pd.read_csv('https://raw.githubusercontent.com/ng-awam/weather-web-app/main/ws_forecast.csv',index_col=0)

df_map_ws = weather_state_forecast_scaled_ws.copy()
df_map_ws.ws_norm=df_map_ws.ws_norm.mask(df_map_ws.ws_norm.lt(0),0)


# In[ ]:





# In[40]:


fig_map2 = px.choropleth(
    data_frame=df_map_ws,
    locationmode='USA-states',
    locations='State',
    scope="usa",
    color='ws_norm',
    hover_data=['ws_norm'],
    color_continuous_scale=px.colors.sequential.Greens,
    labels={'ws_norm': 'Wind speed (m/s)'},
    title = "Evolution of normalized wind speed (m/s) forecast",
    animation_frame = "forecast_day"
)







# In[41]:


weather_state_forecast_scaled_temp = pd.read_csv('https://raw.githubusercontent.com/ng-awam/weather-web-app/main/temp_forecast.csv',index_col=0)

df_map_temp = weather_state_forecast_scaled_temp.copy()
df_map_temp.temp_norm=df_map_temp.temp_norm.mask(df_map_temp.temp_norm.lt(0),0)


# In[42]:


fig_map3 = px.choropleth(
    data_frame=df_map_temp,
    locationmode='USA-states',
    locations='State',
    scope="usa",
    color='temp_norm',
    hover_data=['temp_norm'],
    color_continuous_scale=px.colors.sequential.Reds,
    labels={'temp_norm': 'Temp (C)'},
    title = "Evolution of normalized temperature (C) forecast",
    animation_frame = "forecast_day"
)

alerts = pd.read_csv('https://raw.githubusercontent.com/ng-awam/weather-web-app/main/alerts.csv',index_col=0)

alerts['State'] = 'US_' + alerts['State']


states_dd = [{"label" : "Alabama", "value" : "US_AL"},
                            {"label" : "Alaska", "value" : "US_AK"},
                            {"label" : "Arizona", "value" : "US_AZ"},
                            {"label" : "Arkansas", "value" : "US_AR"},
                            {"label" : "California", "value" : "US_CA"},
                            {"label" : "Colorado", "value" : "US_CO"},
                            {"label" : "Connecticut", "value" : "US_CT"},
                            {"label" : "Delaware", "value" : "US_DE"},
                            {"label" : "District of Columbia", "value" : "US_DC"},
                            {"label" : "Florida", "value" : "US_FL"},
                            {"label" : "Georgia", "value" : "US_GA"},
                            {"label" : "Hawaii", "value" : "US_HI"},
                            {"label" : "Idaho", "value" : "US_ID"},
                            {"label" : "Illinois", "value" : "US_IL"},
                            {"label" : "Indiana", "value" : "US_IN"},
                            {"label" : "Iowa", "value" : "US_IA"},
                            {"label" : "Kansas", "value" : "US_KS"},
                            {"label" : "Kentucky", "value" : "US_KY"},
                            {"label" : "Louisiana", "value" : "US_LA"},
                            {"label" : "Maine", "value" : "US_ME"},
                            {"label" : "Maryland", "value" : "US_MD"},
                            {"label" : "Massachusetts", "value" : "US_MA"},
                            {"label" : "Michigan", "value" : "US_MI"},
                            {"label" : "Minnesota", "value" : "US_MN"},
                            {"label" : "Mississippi", "value" : "US_MS"},
                            {"label" : "Missouri", "value" : "US_MO"},
                            {"label" : "Montana", "value" : "US_MT"},
                            {"label" : "Nebraska", "value" : "US_NE"},
                            {"label" : "Nevada", "value" : "US_NV"},
                            {"label" : "New Hampshire", "value" : "US_NH"},
                            {"label" : "New Jersey", "value" : "US_NJ"},
                            {"label" : "New Mexico", "value" : "US_NM"},
                            {"label" : "New York", "value" : "US_NY"},
                            {"label" : "North Carolina", "value" : "US_NC"},
                            {"label" : "North Dakota", "value" : "US_ND"},
                            {"label" : "Ohio", "value" : "US_OH"},
                            {"label" : "Oklahoma", "value" : "US_OK"},
                            {"label" : "Oregon", "value" : "US_OR"},
                            {"label" : "Pennsylvania", "value" : "US_PA"},
                            {"label" : "Rhode Island", "value" : "US_RI"},
                            {"label" : "South Carolina", "value" : "US_SC"},
                            {"label" : "South Dakota", "value" : "US_SD"},
                            {"label" : "Tennessee", "value" : "US_TN"},
                            {"label" : "Texas", "value" : "US_TX"},
                            {"label" : "Utah", "value" : "US_UT"},
                            {"label" : "Vermont", "value" : "US_VT"},
                            {"label" : "Virginia", "value" : "US_VA"},
                            {"label" : "Washington", "value" : "US_WA"},
                            {"label" : "West Virginia", "value" : "US_WV"},
                            {"label" : "Wisconsin", "value" : "US_WI"},
                            {"label" : "Wyoming", "value" : "US_WY"}]


# In[44]:


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Weather data dashboard", style={'text-align': 'center'}),
    
    
    dcc.Tabs([dcc.Tab(label='Alerts', children=[     
        html.Br(),
        dcc.Dropdown(id="slct_state_alerts",
                 options=states_dd,
                 multi=False,
                 value='US_AK',
                 style={'width': "40%"},
                 searchable=True
                 ),
        html.Br() ,                                       
        dt.DataTable(id='alert_table', 
                     columns=[{'id': c, 'name': c} for c in alerts.columns.values],
                    style_cell_conditional=[
                                            {
                                                'if': {'column_id': c},
                                                'textAlign': 'left'
                                            } for c in ['Date', 'Region']
                                        ],
                                        style_data={
                                            'color': 'black',
                                            'backgroundColor': 'white',
                                            'whiteSpace': 'normal',
                                            'height': 'auto'
                                        },
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(220, 220, 220)',
                                            }
                                        ],
                                        style_header={
                                            'backgroundColor': 'rgb(210, 210, 210)',
                                            'color': 'black',
                                            'fontWeight': 'bold'
                                        }),
        html.Br()                                         
]),
        dcc.Tab(label='Precipitation', children=[dcc.Graph(id="precip_region",figure=fig_precip  , 
                                                           style={'display': 'inline-block'}),
        dcc.Graph(id="precip_forecast",figure=fig_map1, style={'display': 'inline-block'}),
        
        html.Br(),
        dcc.Dropdown(id="slct_state1",
                 options=states_dd,
                 multi=False,
                 value='US_NY',
                 style={'width': "40%"},
                 searchable=True
                 ),
    
        dcc.Graph(id='my_state_graph1', figure={}),
        html.Br()

]),
        
        dcc.Tab(label='Temperature', children=[dcc.Graph(id="temp_region",figure=fig_temp  , 
                                                           style={'display': 'inline-block'}),
        dcc.Graph(id="temp_forecast",figure=fig_map3, style={'display': 'inline-block'}),
                                               
        html.Br(),
        dcc.Dropdown(id="slct_state2",
                 options=states_dd,
                 multi=False,
                 value='US_NY',
                 style={'width': "40%"},
                 searchable=True
                 ),
                                               
        dcc.Graph(id='my_state_graph2', figure={}),
        html.Br()                                         
]),
        
        dcc.Tab(label='Wind Speed', children=[dcc.Graph(id="ws_region",figure=fig_ws  , 
                                                           style={'display': 'inline-block'}),
        dcc.Graph(id="ws_forecast",figure=fig_map2, style={'display': 'inline-block'}),
                                               
        html.Br(),
        dcc.Dropdown(id="slct_state3",
                 options=states_dd,
                 multi=False,
                 value='US_NY',
                 style={'width': "40%"},
                 searchable=True
                 ),
                                               
        dcc.Graph(id='my_state_graph3', figure={}),
        html.Br()                                         
]),
        
])
])

@app.callback(
    Output('alert_table', 'data'),
    [Input('slct_state_alerts', 'value') ] )
def display_table(state):
    dff = alerts[alerts.State==state]
    return dff.to_dict('records')

@app.callback(Output(component_id='my_state_graph1', component_property='figure'),
    [Input(component_id='slct_state1', component_property='value')])

def update_graph(option_slctd1):
    
    df = weather_state_scaled_precip1[weather_state_scaled_precip1['Location'] == option_slctd1][['precip_norm','precip_norm_up',
                                                                                         'precip_norm_mean']]
    
    fig = make_subplots(rows=1,cols=1)
    fig.add_trace(go.Scatter(x=df.index, y= df['precip_norm'],name='Normalized precipitation'),row=1,col=1) 
    fig.add_trace(go.Scatter(x=df.index, y= df['precip_norm_up'],name='Normalized precipitation - Mean + 2STD'),row=1,col=1) 
    fig.add_trace(go.Scatter(x=df.index, y= df['precip_norm_mean'],name='Normalized precipitation - 30day mean'),row=1,col=1)
    fig.add_vline(x=end_date, line_width=3, line_dash="dash", line_color="black")
    fig.update_layout(height=600,width=900,
        title='Normalized precipitation (kg/m2)')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="right",
        x=0.9
    ))
    
    return fig

@app.callback(Output(component_id='my_state_graph2', component_property='figure'),
    [Input(component_id='slct_state2', component_property='value')])

def update_graph(option_slctd1):
    
    df = weather_state_scaled_temp1[weather_state_scaled_temp1['Location'] == option_slctd1][['temp_norm','temp_norm_up',
                                                                                         'temp_norm_mean','temp_norm_down']]
    fig1 = make_subplots(rows=1,cols=1)
    fig1.add_trace(go.Scatter(x=df.index, y= df['temp_norm'],name='Normalized Temp (C)'),row=1,col=1) 
    fig1.add_trace(go.Scatter(x=df.index, y= df['temp_norm_up'],name='Normalized Temp (C) - Mean + 2STD'),row=1,col=1)  
    fig1.add_trace(go.Scatter(x=df.index, y= df['temp_norm_mean'],name='Normalized Temp (C) - 30day mean'),row=1,col=1)
    fig1.add_trace(go.Scatter(x=df.index, y= df['temp_norm_down'],name='Normalized Temp (C) - Mean - 2STD'),row=1,col=1)
    fig1.add_vline(x=end_date, line_width=3, line_dash="dash", line_color="black")
    fig1.update_layout(height=600,width=900,
        title='Normalized Temperature (C)')
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="right",
        x=0.9
    ))
    
    return fig1

@app.callback(Output(component_id='my_state_graph3', component_property='figure'),
    [Input(component_id='slct_state3', component_property='value')])

def update_graph(option_slctd1):
    
    df = weather_state_scaled_ws1[weather_state_scaled_ws1['Location'] == option_slctd1][['ws_norm','ws_norm_up',
                                                                                         'ws_norm_mean']]
    fig1 = make_subplots(rows=1,cols=1)
    fig1.add_trace(go.Scatter(x=df.index, y= df['ws_norm'],name='Normalized wind speed (m/s)'),row=1,col=1) 
    fig1.add_trace(go.Scatter(x=df.index, y= df['ws_norm_up'],name='Normalized wind speed (m/s) - Mean + 2STD'),row=1,col=1)  
    fig1.add_trace(go.Scatter(x=df.index, y= df['ws_norm_mean'],name='Normalized wind speed (m/s) - 30day mean'),row=1,col=1)
    fig1.add_vline(x=end_date, line_width=3, line_dash="dash", line_color="black")
    fig1.update_layout(height=600,width=900,
        title='Normalized wind speed (m/s)')
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="right",
        x=0.9
    ))
    
    return fig1


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)


