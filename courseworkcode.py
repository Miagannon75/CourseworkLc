
import os
print(os.getcwd())
import numpy as np

import pandas as pd

#df = pd.read_csv('/Users/mgannon/Downloads/Coursework2.csv')
df = pd.read_csv('Coursework2.csv')

df_pivot = df.pivot_table(
    index=['Month', ],  
    columns='County',            
    values='VALUE',                
)
df_pivot.columns = [f'{col} Value' for col in df_pivot.columns] 
df_pivot.reset_index(inplace=True)

print(df_pivot)

df_pivot.to_csv('transformed_data_wide.csv', index=False)

print(os.getcwd())

import pandas as pd

df = df.drop('Driving Test Categories', axis=1)

#df = pd.read_csv('/Users/miagannon/Documents/Coursework2.csv')
df = pd.read_csv('Coursework2.csv')
df_pivot = df.pivot_table(
    index=['Month'], 
    columns='County',              
    values='VALUE',                
)

df_pivot.columns = [f'{col} Value' for col in df_pivot.columns] 
df_pivot.reset_index(inplace=True)

print(df_pivot)

df_pivot.to_csv('transformed_data_wide.csv', index=False)

data = pd.read_csv('transformed_data_wide.csv')

numeric_cols = ['Co. Dublin Value','Co. Galway Value','Co. Kildare Value']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors= 'coerce')

#non_numeric_cols = ['Month']

stats_dictionary = {}

for col in numeric_cols:
    stats_data = data[col].dropna()
        #stats_data = data[col]
    stats_dictionary[col] = {
        'Mean': stats_data.mean(),
        'Median': stats_data.median(),
        'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
        'Range': stats_data.max() - stats_data.min()
        }
    
print(stats_dictionary)

stats_df = pd.DataFrame(stats_dictionary).transpose()
print(stats_df)
"""
import plotly.express as px

bar_chart = px.bar(
    data,
    x=data.columns[0],
    y=data.columns[1],
    title="Bar Chart:",
    labels={data.columns[0]: "Month", data.columns[1]: "Value"}
)
bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs="cdn")

data_long = data.melt(
    id_vars=[data.columns[0]]
    value_vars=[data.columns[1], data.columns[2], data.columns[3]],
    var_anem="Variable",
    value_name="Value"
)
"""