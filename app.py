from flask import Flask, flash, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os

from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json


# ******************** APP CONFIG **********************
ALLOWED_EXTENSIONS = {'CSV'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '123ABC'
app.config['FILE_UPLOADS'] = '/Users/nickbattista/Desktop/html-plot/static/file_uploads'


# ******************** DATA UPLOAD AND PLOT RENDER **********************
@app.route("/")
def homepage_redirect():
    """Redirect user to homepage."""
    return redirect('/upload_file')


@app.route("/upload_file", methods=["GET", "POST"])
def upload_csv():
    """Upload dataset."""
    if request.method == 'POST':
        if request.files:
            file = request.files['filename']
            file.save(os.path.join(app.config['FILE_UPLOADS'], file.filename))
            return redirect(f"/render_plot/{file.filename}")
    return render_template('upload.html')


@app.route("/render_plot/<filename>", methods=["GET", "POST"])
def render_plot(filename):
    """Render plot in HTML."""

    df = pd.read_csv(f"static/file_uploads/{filename}")
    fig = px.line(df, x = 'ds', y = 'y', title='Data')

    fig.update_layout(
    autosize=False,
    width=1300,
    height=800)
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Summarize dataset statistics
    min = round(df['y'].min(),2)
    max = round(df['y'].max(),2)
    mean = round(df['y'].mean(),2)
    std =  round(df['y'].std(),2)
    
    return render_template('render_plot.html', plot_json=plot_json, filename=filename, min=min, max=max, mean=mean, std=std)



# ******************** FORECAST **********************
@app.route("/generate_forecast/<filename>", methods=["POST"])
def generate_forecast(filename):
    """Generate forecast."""
    df = pd.read_csv(f"static/file_uploads/{filename}")
    df = df[df['ds'].notna()]

    m = Prophet()
    m.fit(df)

    forecast_length = int(request.form['future'])
    future = m.make_future_dataframe(periods=forecast_length)
    future.tail()
    forecast = m.predict(future)

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

    fig.update_layout(
    autosize=False,
    width=1300,
    height=800)

    forecast_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('review_forecast.html', forecast_json=forecast_json)


# ******************** DATA EXPORT **********************
@app.route("/export_data/<filename>")
def export_data(filename):
    """Export forecast data."""
    filename = filename
    df = pd.read_csv('/Users/nickbattista/Desktop/html-plot/static/{filename}.csv')
    df.to_csv(f"/Users/nickbattista/Downloads/{filename}.csv")

