
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

def analyse_missing_values(df):
    """
    Analyses missing values from df.

    Parameters:
    df (DataFrame): The pandas DataFrame with data.

    Returns:
    Count of rows and columns that have at least one null value and the related percentage.
    """
    missing_rows = df.isnull().any(axis=1).sum()
    missing_columns = df.isnull().any(axis=0).sum()
    total_rows, total_columns = df.shape
    print(f"Missing rows: {missing_rows} out of {total_rows} ({missing_rows/total_rows*100:.2f}%)")
    print(f"Missing columns: {missing_columns} out of {total_columns} ({missing_columns/total_columns*100:.2f}%)")

def aggregate_years(df, year_columns, non_time_columns):
    """
    Aggregates monthly data into yearly data.

    Parameters:
    df (DataFrame): The pandas DataFrame with monthly data.
    year_columns (list): List of years to aggregate data for.

    Returns:
    DataFrame: A new DataFrame with data aggregated by year.
    """
    df_yearly = pd.DataFrame()
    for year in year_columns:
        cols_for_year = [col for col in df.columns if col.startswith(year)]
        df_yearly[year] = df[cols_for_year].sum(axis=1)
    df_yearly[non_time_columns] = df[non_time_columns]
    return df_yearly[non_time_columns + sorted(year_columns)]

def detect_outliers(df, numeric_columns):
    """
    Detects outliers in the numeric columns of a DataFrame using the Interquartile Range (IQR) method.

    Parameters:
    df (DataFrame): The pandas DataFrame to analyze for outliers.
    numeric_columns (list): List of column names in df that are numeric.

    Returns:
    tuple: 
        - DataFrame containing only the rows identified as outliers in numeric columns.
        - Series indicating the count of outliers in each numeric column.
    """
    Q1 = df[numeric_columns].quantile(0.25)
    Q3 = df[numeric_columns].quantile(0.75)
    IQR = Q3 - Q1

    outlier_condition = ((df[numeric_columns] < (Q1 - 1.5 * IQR)) | (df[numeric_columns] > (Q3 + 1.5 * IQR)))
    outliers = outlier_condition.any(axis=1)
    outliers_df = df[outliers]
    outliers_count = outlier_condition.sum()

    return outliers_df, outliers_count

# Set display options
pd.set_option('display.max_columns', None)

# File paths
historical_data_path = '/home/jn607/Projects/LondonCrimeInsights/data/raw_data/APR2010-FEB2022.csv'
recent_data_path = '/home/jn607/Projects/LondonCrimeInsights/data/raw_data/FEB2022-FEB2024.csv'

# Read and inspect data
df_historical_data_raw = read_and_inspect(historical_data_path, ['MajorText', 'MinorText'])
df_recent_data_raw = read_and_inspect(recent_data_path, ['MajorText', 'MinorText'])

# Merge the dataframes
df_crime_monthly = pd.merge(df_historical_data_raw, df_recent_data_raw, how='outer',on=['MajorText', 'MinorText', 'LookUp_BoroughName'])

# Inspect the merged data
print("Shape:", df_crime_monthly.shape)
print("Info:")
print(df_crime_monthly.info())

# Missing values analysis
print("Monthly df:")
analyse_missing_values(df_crime_monthly)

# Aggregate data into yearly
non_time_columns = ['MajorText', 'MinorText', 'LookUp_BoroughName']
years = sorted(set(col[:4] for col in df_crime_monthly.columns if col.isdigit()))
df_crime_yearly = aggregate_years(df_crime_monthly, years, non_time_columns)

# Display the first few rows of the yearly data
print(df_crime_yearly.head())

# Missing values analysis for yearly data
print("Yearly df:")
analyse_missing_values(df_crime_yearly)

# outlier analysis
numeric_cols = df_crime_monthly.select_dtypes(include=['number']).columns.tolist()
outliers_df, outliers_count = detect_outliers(df_crime_monthly, numeric_cols)

print("Outliers detected in each numeric column:\n", outliers_count)
print("\nRows with outliers in numeric columns:\n", outliers_df)
