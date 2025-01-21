import pandas as pd
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px

input_file = 'transformed_data_wide.csv'
output_file = 'BR2-Out.csv'
df = pd.read_csv(input_file)

print(df.head())
print(df.columns)

# If necessary, ensure the 'Month' column is in the correct format (e.g., as a string)
df['Month'] = df['Month'].astype(str)

non_numeric_cols = ['Month']

stat_dict = {}
for col in df.columns:
    if col not in non_numeric_cols:
        stats_data = df[col]
        stat_dict[col] = {
        'Mean': stats_data.mean(),
        'Median': stats_data.std(),
        'Mode': stats_data.min(),
        'Range': stats_data.max()
    
}
        
print(stat_dict)

bar_chart = px.bar(
    df,
    x=df.columns[1],
    y=df.columns[2],
    title="Bar Chart: Col 1 vs Col2",
    labels={df.columns[1]: "Month", df.columns[2]: "Co.Dublin Value"}
)
bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs="cdn")

data_long = df.melt(
    id_vars=[df.columns[1]],
    value_vars=[df.columns[2], df.columns[3]],
    var_name="Variable",
    value_name="Value"
)

print(data_long.head())

bar_chart_long = px.bar(
    data_long,
    x='Variable',
    y='Value',
    color='Variable',  # Differentiates between 'Co.Dublin' and other variables
    title="Bar Chart: Month vs Variables",
    labels={'Variable': 'Variable', 'Value': 'Values'}
)

bar_chart_long.show()


bar_chart.show()