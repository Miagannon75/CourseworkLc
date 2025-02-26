import pandas as pd
#import csv
#from datetime import datetime
import numpy as np
#import pygal
import matplotlib.pyplot as plt
from flask import Flask, render_template

import plotly.express as px

app = Flask(__name__)

data = pd.read_csv('Data.csv')

data['Month'] = pd.to_datetime(data['Month'] + ' 01', format='%Y %B %d')
data.sort_values(by='Month', inplace=True)
data.columns = data.columns.str.strip().str.lower()
data_pivoted = data.pivot_table(index='month', 
                            columns='county', 
                            values='value', 
                            aggfunc='mean')


data_pivoted.columns = [f"{col} pass rate" for col in data_pivoted.columns]
data_pivoted.reset_index(inplace=True)
data_pivoted['month'] = data_pivoted['month'].dt.strftime('%d-%m-%Y')
data_pivoted.to_csv('cleaneddata.csv', index=False)

numeric_cols = data_pivoted.columns[1:]  # All columns except 'Date' should be numeric
#for col in numeric_cols:
    #data[col] = pd.to_numeric(data[col], errors='coerce')
data = pd.read_csv('cleaneddata.csv')
# Compute statistics for numeric columns
stats_dictionary = {}


for col in numeric_cols:
    stats_data = data_pivoted[col].dropna()  # Drop NA values for stats calculations
    stats_dictionary[col] = {
        'Mean': stats_data.mean(),
        'Median': stats_data.median(),
        'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
        'Range': stats_data.max() - stats_data.min()
    }

#print("Statistics Dictionary:")
#print(stats_dictionary)

stats_df = pd.DataFrame(stats_dictionary).T

# Write the stats DataFrame to a CSV file
stats_df.to_csv('driving_test_pass_rate_statistics.csv', index=True)

# Print the statistics DataFrame for verification
print("Statistics DataFrame:")
print(stats_df)

# Create DataFrame from the stats dictionary
bar_chart_dublin = px.bar(
    data_pivoted,
    x='month',
    y='Co. Dublin pass rate',
    title="Bar Chart: Month vs Co.Dublin Value",
    labels={'month': 'month', 'Co. Dublin pass rate' : 'Co. Dublin pass rate'}
)

bar_chart_galway = px.bar(
    data_pivoted,
    x='month',
    y='Co. Galway pass rate',
    title="Bar Chart: Month vs Co.Galway Value",
    labels={'month': 'month', 'Co. Galway pass rate': 'Co. Galway pass rate'}

)

bar_chart_donegal = px.bar(
    data_pivoted,
    x='month',
    y='Co. Donegal pass rate',
    title="Bar Chart: Month vs Co.Donegal Value",
    labels={'month': 'month', 'Co. Donegal pass rate': 'Co. Donegal pass rate'}

)

bar_chart_dublin_html = bar_chart_dublin.to_html(full_html=False, include_plotlyjs="cdn")
bar_chart_galway_html = bar_chart_galway.to_html(full_html=False, include_plotlyjs="cdn")
bar_chart_donegal_html = bar_chart_donegal.to_html(full_html=False, include_plotlyjs="cdn")

data_long = data.melt(
    id_vars=['month'],
    value_vars=[col for col in data.columns if col !='month'],
    var_name="Variable",
    value_name="Value"
)
           
line_chart = px.line(
    data_long,
    x='month',
    y='Value',
    color="Variable",
    title="Line Chart: Column 1 Vs Column 2",
    labels={                 # Update the labels
        'month': "month", 
        'Value': "pass rates", 
        'Variable': "Counties" 
    }
)
line_chart_html = line_chart.to_html(full_html=False, include_plotlyjs="cdn")

scatter_plot = px.scatter(
    data_pivoted,
    x='Co. Dublin pass rate',
    y='Co. Galway pass rate',
    title="Dublin vs Galway pass rates",
    labels={data.columns[3]: "Values"}
)
scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")

data_long_scatter = data.melt(
    id_vars=["month"],
    value_vars=[data.columns[1], data.columns[2], data.columns[3]],  # Make sure column 4 is Co.Kildare
    var_name="County",
    value_name="Value"
)

scatter_plot_2 = px.scatter(
    data_long_scatter,
    x='month',
    y='Value',
    color='County',  # Color by County column
    title="Scatter Plot: Dublin, Galway, and Donegal Values",
    labels={'month': 'Month', 'Value': 'Values', 'County': 'County'}
)

# Convert scatter plot to HTML
scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")


scatter_plot_2_html = scatter_plot_2.to_html(full_html=False, include_plotlyjs="cdn")

"""
bar_chart_dublin.show()
bar_chart_galway.show()
bar_chart_donegal.show()
line_chart.show()
scatter_plot.show()
scatter_plot_2.show()
"""

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

suggestions_list = []

@app.route('/')
def index():
    return render_template(
        'index.html',
        bar_chart_dublin=bar_chart_dublin_html,
        bar_chart_galway=bar_chart_galway_html,
        bar_chart_donegal=bar_chart_donegal_html,
        line_chart=line_chart_html,
        scatter_plot=scatter_plot_html,
        scatter_plot_2=scatter_plot_2_html
    )
@app.route('/data_form', methods=['GET', 'POST'])
def data_form():
    if request.method == 'POST':
        # Get the data from the form
        county = request.form.get('county')
        month = request.form.get('month')
        pass_rate = request.form.get('pass_rate')

        # Validate the data
        if county and month and pass_rate:
            # Store the data
            data_collection.append({
                'county': county,
                'month': month,
                'pass_rate': pass_rate
            })
            return jsonify({"status": "success", "message": "Data added successfully!"})
        else:
            return jsonify({"status": "error", "message": "All fields are required!"})

    return render_template('data_form.html')

# Route to get the collected data (GET)
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data_collection)

# Route to show summarized data (summary page)
@app.route('/summary', methods=['GET'])
def summary():
    return render_template('summary.html', data=data_collection)

    df = pd.DataFrame(data_collection)
    if not df.empty:
        summary_data = df.groupby(['county', 'month']).agg({'pass_rate': ['mean', 'count']}).reset_index()
    else:
        summary_data = None
    return render_template('summary.html', summary_data=summary_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
