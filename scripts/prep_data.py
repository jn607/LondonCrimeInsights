
import pandas as pd

def read_and_inspect(file_path, columns_to_inspect):
    """
    Reads data from a CSV file and prints unique values of specified columns.

    Parameters:
    file_path (str): The path to the CSV file.
    columns_to_inspect (list): List of columns to print unique values for.

    Returns:
    DataFrame: A pandas DataFrame of the read data.
    """
    df = pd.read_csv(file_path)
    for column in columns_to_inspect:
        print(f"Unique values in {column}:")
        print(df[column].drop_duplicates())
    return df

# Set display options
pd.set_option('display.max_columns', None)

# File paths
historical_data_path = '/Users/joshnolan/programmingProjects/CrimeInsights/LondonCrimeInsights/data/raw_data/APR2010-FEB2022.csv'
recent_data_path = '/Users/joshnolan/programmingProjects/CrimeInsights/LondonCrimeInsights/data/raw_data/FEB2022-FEB2024.csv'

# Read and inspect data
df_historical_data_raw = read_and_inspect(historical_data_path, ['MajorText', 'MinorText'])
df_recent_data_raw = read_and_inspect(recent_data_path, ['MajorText', 'MinorText'])

# Merge the dataframes
df_crime_monthly = pd.merge(df_historical_data_raw, df_recent_data_raw, how='outer',on=['MajorText', 'MinorText', 'LookUp_BoroughName'])

df_crime_monthly.to_csv('/Users/joshnolan/programmingProjects/CrimeInsights/LondonCrimeInsights/data/bronze_data/bronze_crime_monthly.csv', index=False)


