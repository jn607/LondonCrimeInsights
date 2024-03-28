import pandas as pd
pd.set_option('display.max_columns', None)

historical_data_raw_df = pd.read_csv('/home/jn607/Projects/LondonCrimeInsights/data/raw_data/APR2010-FEB2022.csv')
recent_data_raw_df = pd.read_csv('/home/jn607/Projects/LondonCrimeInsights/data/raw_data/FEB2022-FEB2024.csv')

#general view
recent_data_raw_df
historical_data_raw_df

#View data types
historical_data_raw_df.dtypes[:60]
recent_data_raw_df.dtypes[:60]

#merge the dfs

