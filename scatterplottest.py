import csv
from datetime import datetime
import pandas as pd
import numpy as np
#import pygal
#import matplotlib.pyplot as plt
from flask import Flask, render_template

import plotly.express as px

# Input and output file names
input_file = 'transformed_data_wide.csv'
output_file = 'BR2-Out.csv'
data = pd.read_csv(input_file,na_values=['no data'],encoding='utf-8')
data.to_csv(input_file, index=False)


#numeric_cols = ['wkno','value1','value2']
non_numeric_cols = ['Month']
stat_dict = {}

for col in data.columns:
    if col not in non_numeric_cols:
        stats_data = data[col]
        stat_dict[col] = {
            'Mean': stats_data.mean(),
            'median': stats_data.median(),
            #'Mode': stats_data.mode().iloc(0) if not stats_data.mode().empty else np.nan,
            'Range': stats_data.max() - stats_data.min()
            }
#print(stat_dict)

stats_df = pd.DataFrame(stat_dict).transpose()
print(stats_df)

bar_chart_dublin = px.bar(
    data,
    x='Month',
    y=data.columns[1],
    title="Bar Chart: Month vs Co.Dublin Value",
    labels={'Month': 'Month', data.columns[2]: 'Co.Dublin Value'}
)

bar_chart_galway = px.bar(
    data,
    x='Month',
    y=data.columns[2],
    title="Bar Chart: Month vs Co.Galway Value",
    labels={'Month': 'Month', data.columns[3]: 'Co.Galway Value'}

)

bar_chart_kildare = px.bar(
    data,
    x='Month',
    y=data.columns[3],
    title="Bar Chart: Month vs Co.Kildare Value",
    labels={'Month': 'Month', data.columns[3]: 'Co.Kildare Value'}

)

bar_chart_dublin_html = bar_chart_dublin.to_html(full_html=False, include_plotlyjs="cdn")
bar_chart_galway_html = bar_chart_galway.to_html(full_html=False, include_plotlyjs="cdn")
bar_chart_kildare_html = bar_chart_kildare.to_html(full_html=False, include_plotlyjs="cdn")


data_long = data.melt(
    id_vars=[data.columns[0]],
    value_vars=[data.columns[1], data.columns[2], data.columns[3]],
    var_name="Variable",
    value_name="Value"
)
           
line_chart = px.line(
    data_long,
    x='Month',
    y='Value',
    color="Variable",
    title="Line Chart: Column 1 Vs Column 2",
    labels={                 # Update the labels
        'Month': "Month", 
        'Value': "Values", 
        'Variable': "Categories"
    }
)
line_chart_html = line_chart.to_html(full_html=False, include_plotlyjs="cdn")

data_long_scatter = data.melt(
    id_vars=["Month"],
    value_vars=[data.columns[1], data.columns[2], data.columns[3]],  # Make sure column 4 is Co.Kildare
    var_name="County",
    value_name="Value"
)

# Create scatter plot with different colors for Dublin, Galway, and Kildare
scatter_plot = px.scatter(
    data_long_scatter,
    x='Month',
    y='Value',
    color='County',  # Color by County column
    title="Scatter Plot: Dublin, Galway, and Kildare Values",
    labels={'Month': 'Month', 'Value': 'Values', 'County': 'County'}
)

# Convert scatter plot to HTML
scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")

bar_chart_kildare.show()
bar_chart_dublin.show()
bar_chart_galway.show()
line_chart.show()
scatter_plot.show()

@app.route('/')
def index():
    return render_template(
        'index.html',
        bar_chart=bar_chart_html,
        line_chart=line_chart_html,
        scatter_chart=scatter_plot_html
    )

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5001,debug=False)