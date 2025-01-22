import os
print(os.getcwd())
import numpy as np

import pandas as pd

#df = pd.read_csv('/Users/mgannon/Downloads/Coursework2.csv')
df = pd.read_csv('courseworkcode3.csv')

data = pd.read_csv('transformed_data_wide.csv')

# Check the unique values in the 'Month' column to ensure they are correctly formatted
print(data['Month'].unique())

# Strip any leading/trailing spaces from the 'Month' column (if there are any)
data['Month'] = data['Month'].str.strip()

# Convert 'Month' column to a categorical type with an ordered category
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)


data['Date'] = pd.to_datetime(data['Year'] + ' ' + data['Month_Name'], format='%Y %B')
# Now sort the data by 'Month'
data.sort_values('Month', inplace=True)

df_pivot = df.pivot_table(
    index=['Month', ],  
    columns='County',            
    values='VALUE',                
)
df_pivot.columns = [f'{col} Value' for col in df_pivot.columns] 
df_pivot.reset_index(inplace=True)

print(df_pivot)

df_pivot.to_csv('transformed_data_wide2.csv', index=False)

print(os.getcwd())

import pandas as pd

df = df.drop('Driving Test Categories', axis=1)

#df = pd.read_csv('/Users/miagannon/Documents/Coursework2.csv')
df = pd.read_csv('courseworkcode3.csv')
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

numeric_cols = ['Co. Donegal Value','Co. Dublin Value','Co. Galway Value']
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

