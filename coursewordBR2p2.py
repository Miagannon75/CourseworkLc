import pandas as pd
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

input_file = 'transformed_data_wide.csv'
output_file = 'BR2-Out.csv'
df = pd.read_csv(input_file)

# Print the first few rows and column names to check the data
print(df.head())
print(df.columns)

# Ensure the 'Month' column is in the correct format (as a string or datetime)
# Here we assume that 'Month' is in a format like '2021-01', if it's a date string or datetime, convert it to a readable format
df['Month'] = pd.to_datetime(df['Month'], errors='coerce')  # Converts to datetime, 'errors' handles invalid values
df['Month'] = df['Month'].dt.strftime('%B %Y')  # Convert to "January 2021", "February 2021", etc.

# Check the 'Month' format
print(df['Month'].head())

non_numeric_cols = ['Month']

# Calculate statistics for numerical columns
stat_dict = {}
for col in df.columns:
    if col not in non_numeric_cols:
        stats_data = df[col]
        stat_dict[col] = {
            'Mean': stats_data.mean(),
            'Median': stats_data.std(),  # Median should be calculated with .median(), not .std()
            'Mode': stats_data.min(),
            'Range': stats_data.max()
        }

# Print the statistics
print(stat_dict)

# Create the bar chart: Set Month on the x-axis and Co.Dublin on the y-axis
bar_chart = px.bar(
    df,
    x='Month',  # Use the 'Month' column for the x-axis
    y=df.columns[2],  # Assuming df.columns[2] is 'Co.Dublin Value'
    title="Bar Chart: Month vs Co.Dublin Value",
    labels={'Month': 'Month', df.columns[2]: 'Co.Dublin Value'}
)

# Convert the plot to HTML (if needed for embedding)
bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs="cdn")

# Reshape the data using melt (if you want to plot multiple variables)
data_long = df.melt(
    id_vars=['Month'],  # Use 'Month' as the identifier
    value_vars=[df.columns[2], df.columns[3]],  # Include 'Co.Dublin' and any other columns for comparison
    var_name="Variable",
    value_name="Value"
)

# Print the reshaped data to confirm it looks as expected
print(data_long.head())

# Create the long format bar chart
bar_chart_long = px.bar(
    data_long,
    x='Month',  # Now use 'Month' for the x-axis
    y='Value',  # 'Value' contains the actual numeric values
    color='Variable',  # Differentiates between 'Co.Dublin' and other variables
    title="Bar Chart: Month vs Variables",
    labels={'Month': 'Month', 'Value': 'Values'}
)

# Show the long format bar chart
bar_chart_long.show()

# Display the original bar chart
bar_chart.show()