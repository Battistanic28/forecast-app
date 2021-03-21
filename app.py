from flask import Flask, flash, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from helper import forecast, generate_dataset_JSON, generate_forecast_JSON
import os


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
    
    dataset = f"{app.config['FILE_UPLOADS']}/{filename}"
    plot_json = generate_dataset_JSON(dataset)
    
    return render_template('render_plot.html', plot_json=plot_json, filename=filename)


# ******************** FORECAST **********************
@app.route("/generate_forecast/<filename>", methods=["POST"])
def render_forecast(filename):
    """Generate forecast and forecast JSON."""

    dataset = f"{app.config['FILE_UPLOADS']}/{filename}"
    forecast_length = int(request.form['future'])
    forecast_json = generate_forecast_JSON(dataset, forecast_length)

    return render_template('review_forecast.html', forecast_json=forecast_json)
    

# ******************** DATA EXPORT **********************
@app.route("/export_data/<filename>")
def export_data(filename):
    """Export forecast data."""
    filename = filename
    df = pd.read_csv('/Users/nickbattista/Desktop/html-plot/static/{filename}.csv')
    df.to_csv(f"/Users/nickbattista/Downloads/{filename}.csv")

