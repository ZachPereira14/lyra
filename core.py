import pandas as pd
from .data import load_data, clean_data

def process_dfs(dataframes, period, clean=False, div = True):
    """
    Process multiple DataFrames:
    - Normalize BJD time column.
    - Plot Source_AMag_T1 against BJD_normalized for each DataFrame.
    - Return list of processed DataFrames, BJD_normalized first and last values for each.

    Parameters:
    dataframes (list): List of tuples where each tuple contains (filename, label).
    period (float): Period of orbit of target
    clean (bool, optional): Whether to perform data cleaning on the loaded DataFrame. Default is False.

    Returns:
    list: List of tuples containing (processed DataFrame, first BJD_normalized value, last BJD_normalized value, label_str).
    """
    processed_data = []

    for name_str, label_str in dataframes:
        try:
            # Call load_data function to load DataFrame from file
            result = load_data(name_str, clean=clean)
            if result is None:
                continue

            df, column_lists = result
            df, first_value, last_value = norm(df, label_str, period, div)

            processed_data.append((df, first_value, last_value, label_str))  # Include label_str in processed_data tuple
        except Exception as e:
            print(f"Error processing {name_str}: {e}")

    return processed_data


def norm(df, label_str, period, div = True):
    """
    Helper function to process a single DataFrame:
    - Normalize BJD time column.
    - Plot Source_AMag_T1 against BJD_normalized.
    - Return DataFrame, BJD_normalized first and last values.

    Parameters:
    df (DataFrame): Input DataFrame containing BJD_TDB and Source_AMag_T1 columns.
    label_str (str): Label for the dataset.
    div (bool): Whether to normalize by dividing by the period. Defaults to True.

    Returns:
    DataFrame: Processed DataFrame.
    float: First BJD_normalized value.
    float: Last BJD_normalized value.
    """

    # Check if 'BJD_TDB' column exists in the DataFrame
    if 'BJD_TDB' not in df.columns:
        raise KeyError("Column 'BJD_TDB' not found in DataFrame.")

    try:
        if div == True:
            df['BJD_normalized'] = (df['BJD_TDB'] % period) / period
            return df, df['BJD_normalized'].iloc[0], df['BJD_normalized'].iloc[-1]
        else:
            df['BJD_normalized'] = (df['BJD_TDB'] % period) 
            return df, df['BJD_normalized'].iloc[0], df['BJD_normalized'].iloc[-1]
    except Exception as e:
        print(f"Error processing DataFrame: {e}")
        return None, None, None
