import pandas as pd
pd.set_option('display.max_columns', None)

df_historical_data_raw = pd.read_csv('/home/jn607/Projects/LondonCrimeInsights/data/raw_data/APR2010-FEB2022.csv')
df_recent_data_raw = pd.read_csv('/home/jn607/Projects/LondonCrimeInsights/data/raw_data/FEB2022-FEB2024.csv')

#general view
df_recent_data_raw
df_historical_data_raw

#View unique values to check everything will map
unique_values_hist = df_historical_data_raw.iloc[:,0].drop_duplicates()
print(unique_values_hist)
unique_values_rec = df_recent_data_raw.iloc[:,0].drop_duplicates()
print(unique_values_rec)

unique_values_hist = df_historical_data_raw.iloc[:,1].drop_duplicates()
print(unique_values_hist)
unique_values_rec = df_recent_data_raw.iloc[:,1].drop_duplicates()
print(unique_values_rec)

#Identify non-matching values in the minor text
matching_values = ~unique_values_rec.isin(unique_values_hist)
print(matching_values.sum()) 


#0 differences so Merge the dfs
df_combined = pd.merge(df_historical_data_raw, df_recent_data_raw, how='outer', on=['MajorText', 'MinorText', 'LookUp_BoroughName'])

