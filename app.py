from flask import Flask, flash, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os

from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly

import pandas as pd
import plotly
import plotly.express as px
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
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('render_plot.html', plot_json=plot_json, filename=filename)



# ******************** FORECAST **********************
@app.route("/generate_forecast/<filename>", methods=["POST"])
def generate_forecast(filename):
    """Generate forecast."""
    df = pd.read_csv(f"static/file_uploads/{filename}")
    df = df[df['ds'].notna()]

    m = Prophet()
    m.fit(df)

    forecast_length = int(request.form['future'])
    print(forecast_length)
    future = m.make_future_dataframe(periods=forecast_length)
    future.tail()

    forecast = m.predict(future)
    fig = px.line(forecast, x = 'ds', y = 'yhat', title='Data')

    forecast_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('review_forecast.html', forecast_json=forecast_json)


# ******************** DATA EXPORT **********************
@app.route("/export_data/<filename>")
def export_data(filename):
    """Export forecast data."""
    filename = "yosemite_temps"
    df = pd.read_csv('/Users/nickbattista/Desktop/html-plot/static/file_uploads/example_yosemite_temps.csv')
    df.to_csv(f"/Users/nickbattista/Downloads/{filename}.csv")