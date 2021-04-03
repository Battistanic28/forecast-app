import app

from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import json


def read_dataset(dataset):
    """Read input dataset csv."""

    df = pd.read_csv(dataset)

    return df


def forecast(dataset, forecast_length, filename):
    """Generates Facebook Prophet forecast based on input file and forecast length."""
    df = dataset
    df = df[df['ds'].notna()]

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=forecast_length)
    future.tail()
    forecast = m.predict(future)

    forecast.to_csv(f"tmp/client_downloads/forecast_{filename}")

    return forecast


def generate_forecast_JSON(df, fc, name):
    """Generates forecast data based on input dataset."""

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
    width=1000,
    height=700)

    fig.write_image(f"tmp/client_downloads/{name}.png")
    forecast_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return forecast_json


def generate_dataset_JSON(df):
    """Generates plot JSON based on input dataset."""

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
    width=1000,
    height=700)
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
