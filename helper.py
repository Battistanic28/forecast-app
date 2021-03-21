from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json


def forecast(filename, forecast_length):
    """Generates Facebook Prophet forecast based on input file and forecast length."""
    df = pd.read_csv(filename)
    df = df[df['ds'].notna()]

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=forecast_length)
    future.tail()
    forecast = m.predict(future)
    
    return forecast


def generate_dataset_JSON(dataset):
    """Generates plot JSON based on input dataset."""

    df = pd.read_csv(dataset)
    
    actual = go.Scatter(
        name = 'actuals',
        x = df['ds'],
        y = df['y'],
        mode='markers',
        line=dict(color='rgb(0,0,0)')
    )

    fig = go.Figure(actual)

    fig.update_layout(
    autosize=False,
    width=1300,
    height=800)
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def generate_forecast_JSON(dataset, forecast_length):
    """Generates forecast JSON based on input dataset."""

    df = pd.read_csv(dataset)
    fc = forecast(dataset, forecast_length)

    yhat = go.Scatter(
        name = 'forecast',
        x = fc['ds'],
        y = fc['yhat'],
        mode='lines',
        line=dict(color='rgb(31, 119, 180)')
    )

    yhat_upper = go.Scatter(
        name='Upper Bound',
        x=fc['ds'],
        y=fc['yhat_upper'],
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False     
    )

    yhat_lower = go.Scatter(
        name='Lower Bound',
        x=fc['ds'],
        y=fc['yhat_lower'],
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False
    )  

    actual = go.Scatter(
        name = 'actuals',
        x = fc['ds'],
        y = df['y'],
        mode='markers',
        line=dict(color='rgb(0,0,0)')
    )

    fig = go.Figure(actual)

    fig.add_trace(yhat)
    fig.add_trace(yhat_upper)
    fig.add_trace(yhat_lower)

    fig.update_layout(
    autosize=False,
    width=1300,
    height=800)

    forecast_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return forecast_json
