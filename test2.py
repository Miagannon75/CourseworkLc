import os
import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('Courseworkcode3.csv')

# Rename columns to make them more understandable
df.columns = ['Category', 'Year-Month', 'County', 'Test Category', 'Unit', 'Value']

# Drop irrelevant columns that are not needed for the analysis
df = df.drop(['Category', 'Test Category', 'Unit'], axis=1)

# Ensure 'Year-Month' column is split into 'Year' and 'Month'
df[['Year', 'Month']] = df['Year-Month'].str.split(' ', n=1, expand=True)

# Convert 'Year' to int and 'Month' to a categorical variable with the correct order
df['Year'] = df['Year'].astype(int)

# Month order for sorting
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Combine Year and Month into a 'Date' column for sorting
df['Date'] = pd.to_datetime(df['Year'].astype(str) + ' ' + df['Month'].astype(str), format='%Y %B')

# Sort by 'Date'
df = df.sort_values(by='Date')

# Drop 'Year-Month' column and reset the index
df = df.drop(['Year-Month'], axis=1).reset_index(drop=True)

# Pivot the table: Month as the index, County as columns, and Value as the values
df_pivot = df.pivot_table(
    index='Date',           # Date as the index
    columns='County',       # County becomes columns
    values='Value',         # Values are taken from the 'Value' column
    aggfunc='mean'          # If there are multiple rows for the same month and county, take the average
)

# Rename the columns to include 'Value' at the end of each county name
df_pivot.columns = [f'{col} Value' for col in df_pivot.columns]

# Reset index so 'Date' becomes a column
df_pivot.reset_index(inplace=True)

# Ensure the Date column is in 'YYYY-MM-DD' format for display
df_pivot['Date'] = df_pivot['Date'].dt.strftime('%Y-%m-%d')

# Check the structure of the pivoted DataFrame
print("Pivot Table Structure:")
print(df_pivot.head())  # Print the first few rows to inspect

# Save the pivoted DataFrame to a new CSV
df_pivot.to_csv('transformed_data_wide.csv', index=False)

# Reload the transformed data to ensure the CSV is correct
data = pd.read_csv('transformed_data_wide.csv')

# Convert numeric columns to numeric, coercing errors (in case there are missing values or non-numeric entries)
numeric_cols = df_pivot.columns[1:]  # All columns except 'Date' should be numeric
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Compute statistics for numeric columns
stats_dictionary = {}

for col in numeric_cols:
    stats_data = data[col].dropna()  # Drop NA values for stats calculations
    stats_dictionary[col] = {
        'Mean': stats_data.mean(),
        'Median': stats_data.median(),
        'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
        'Range': stats_data.max() - stats_data.min()
    }

# Print the stats
print("Statistics Dictionary:")
print(stats_dictionary)

# Create DataFrame from the stats dictionary
stats_df = pd.DataFrame(stats_dictionary).transpose()
print("Statistics DataFrame:")
print(stats_df)
