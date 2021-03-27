# Forecast App

Forecast App is an application designed to provide a user friendly interface to the Facebook Prophet forecasting procedure. Forecast App provides the functionality to,
1. Import a user dataset.
2. Render a starting plot based on user data.
3. Enter a forecast "future date frame" (i.e. 365 days).
4. Generate a forecast.
5. Export forecasted data plot and/or csv file.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all forecast-app requirements.

```bash
pip install -r requirements.txt
```

## Demo

![Forecast App Demo](/static/images/demo.gif)


## Usage

#### File upload:
![Sample File](/static/images/sample.png)
- Dataset files should be formatted in accordance to the example above.
- The "ds" and "y" headers are a requirement at this stage in development.
- Download a sample file [here](/static/mean_temps.csv).

#### Forecast length:
The input value for the forecast "future range" should be represented in number of days.

#### Data export:
Currently there are two options for data export.
- Forecast data (csv only)
- Forecast plot (jpeg only)

