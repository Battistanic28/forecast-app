from flask import Flask, render_template, redirect

from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly

import pandas as pd
import plotly
import plotly.express as px
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = '123ABC'

@app.route("/")
def upload_csv():
    """Upload dataset."""
    return render_template('upload.html')


@app.route("/render_plot")
def render_plot():
    """Render plot in HTML."""
    df = pd.read_csv('example_peyton.csv')
    fig = px.line(df, x = 'ds', y = 'y', title='Peyton Data')
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # fig.show()

    return render_template('render_plot.html', plot_json=plot_json)


@app.route("/review_forecast")
def review_forecast():
    """Review forecast."""
    df = pd.read_csv('example_peyton.csv')
    df = df[df['ds'].notna()]

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    fig = m.plot(forecast)
    forecast_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('review_forecast.html', forecast_json=forecast_json)

