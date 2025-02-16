import pandas as pd
#import csv
#from datetime import datetime
import numpy as np
#import pygal
#import matplotlib.pyplot as plt
from flask import Flask, render_template

import plotly.express as px

df = pd.read_csv('Data.csv')

df['Month'] = pd.to_datetime(df['Month'] + ' 01', format='%Y %B %d')
df.sort_values(by='Month', inplace=True)
df.columns = df.columns.str.strip().str.lower()
df_pivoted = df.pivot_table(index='month', 
                            columns='county', 
                            values='value', 
                            aggfunc='mean')


df_pivoted.columns = [f"{col} pass rate" for col in df_pivoted.columns]
df_pivoted.reset_index(inplace=True)
df_pivoted['month'] = df_pivoted['month'].dt.strftime('%d-%m-%Y')
df_pivoted.to_csv('cleaned_driving_test_pass_rate_pivoted.csv', index=False)

numeric_cols = df_pivoted.columns[1:]  # All columns except 'Date' should be numeric
#for col in numeric_cols:
    #data[col] = pd.to_numeric(data[col], errors='coerce')

# Compute statistics for numeric columns
stats_dictionary = {}

for col in numeric_cols:
    stats_data = df_pivoted[col].dropna()  # Drop NA values for stats calculations
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
