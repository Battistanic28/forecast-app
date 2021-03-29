from flask import Flask, flash, render_template, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from helper import forecast, read_dataset, generate_dataset_JSON, generate_forecast_JSON
import os
import pandas as pd


# ******************** APP CONFIG **********************
ALLOWED_EXTENSIONS = {'CSV'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '123ABC'
app.config['FILE_UPLOADS'] = '/Users/nickbattista/Desktop/html-plot/static/client/file_uploads'
app.config['CLIENT_FILES'] = '/Users/nickbattista/Desktop/html-plot/static/client/file_downloads'

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
    
    file = f"{app.config['FILE_UPLOADS']}/{filename}"
    df = read_dataset(file)
    plot_json = generate_dataset_JSON(df)

    min = str(round(df['y'].min(),2))
    max = str(round(df['y'].max(),2))
    mean = str(round(df['y'].mean(),2))
    std = str(round(df['y'].std(),2))
    
    return render_template('render_plot.html', plot_json=plot_json, filename=filename, min=min, max=max, mean=mean, std=std)


# ******************** FORECAST **********************
@app.route("/generate_forecast/<filename>", methods=["POST"])
def render_forecast(filename):
    """Generate forecast and forecast JSON."""

    name = os.path.splitext(filename)[0]
    file = f"{app.config['FILE_UPLOADS']}/{filename}"

    forecast_length = int(request.form['future'])
    df = read_dataset(file)
    fc = forecast(df, forecast_length, filename)

    forecast_json = generate_forecast_JSON(df, fc, name)
    
    min = str(round(fc['yhat'].min(),2))
    max = str(round(fc['yhat'].max(),2))
    mean = str(round(fc['yhat'].mean(),2))
    std = str(round(fc['yhat'].std(),2))

    return render_template('review_forecast.html', name=name, filename=filename, forecast_json=forecast_json, min=min, max=max, mean=mean, std=std)
    

# ******************** EXPORT **********************
@app.route("/export/<filename>")
def get_data(filename):
    """Export client data."""
    export = send_from_directory(app.config['CLIENT_FILES'], filename=filename, as_attachment=True)
    return export
