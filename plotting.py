from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json

forecast = pd.read_csv("static/file_uploads/PredictOutput.csv")
df = pd.read_csv("static/file_uploads/therms.csv")
df = df[df['ds'].notna()]


yhat = go.Scatter(
    name = 'forecast',
    x = forecast['ds'],
    y = forecast['yhat'],
    mode='lines',
    line=dict(color='rgb(31, 119, 180)')
)

yhat_upper = go.Scatter(
    name='Upper Bound',
    x=forecast['ds'],
    y=forecast['yhat_upper'],
    mode='lines',
    marker=dict(color="#444"),
    line=dict(width=0),
    showlegend=False     
)

yhat_lower = go.Scatter(
    name='Lower Bound',
    x=forecast['ds'],
    y=forecast['yhat_lower'],
    marker=dict(color="#444"),
    line=dict(width=0),
    mode='lines',
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty',
    showlegend=False
)  

actual = go.Scatter(
    name = 'actuals',
    x = forecast['ds'],
    y = df['y'],
    mode='markers',
    line=dict(color='rgb(0,0,0)')
)

fig = go.Figure(actual)

fig.add_trace(yhat)
fig.add_trace(yhat_upper)
fig.add_trace(yhat_lower)