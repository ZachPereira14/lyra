import pandas as pd
import os

def load_data(filename, clean=False):
    """
    Load data from a CSV or Excel file into a Pandas DataFrame and extract column values as lists.

    Parameters:
    filename (str): Path to the CSV or Excel file to load.
    clean (bool, optional): Whether to perform data cleaning on the loaded DataFrame. Default is False.

    Returns:
    tuple or None: If successful, returns a tuple (DataFrame, column_lists). If an error occurs (e.g., file not found,
    parsing error), prints an error message and returns None.

    ******************************************************************************
    *                                                                             *
    * Example usage of column_lists:                                              *
    *                                                                             *
    * data, column_lists = load_data('data.xlsx', clean=True)                     *
    *                                                                             *   
    * # Access column values using column_lists dictionary                        *   
    * Source_AMag_T1 = column_lists['Source_AMag_T1']                             *
    *                                                                             *
    ******************************************************************************
    """
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filename)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(filename)
        elif filename.endswith('.tbl'):
            # Assuming the .tbl file is tab-separated
            df = pd.read_csv(filename, delimiter='\t')
        else:
            print(f"Error: Unsupported file format for '{filename}'. Supported formats are CSV and Excel.")
            return None
        
        if clean:
            df = clean_data(df,filename)
        
        # Extract column values into lists
        column_lists = {col: df[col].tolist() for col in df.columns}
        
        return df, column_lists
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    
    except pd.errors.ParserError as e:
        print(f"Error parsing '{filename}': {e}")
        return None

def clean_data(df, df_name="DataFrame"):
    """
    Clean the input DataFrame by removing rows with missing values (NaN).

    Parameters:
    df (DataFrame): Input DataFrame containing data to be cleaned.

    Returns:
    DataFrame: Cleaned DataFrame with rows containing any NaN values removed.

    """
    # Check if 'BJD_TDB' column exists in the DataFrame
    if 'BJD_TDB' not in df.columns:
        raise KeyError("Column 'BJD_TDB' not found in DataFrame.")

    # Implement data cleaning steps as needed
    # Example: Handling missing values or outliers
    df_clean = df.dropna()

    # Print message if no NaN values were found
    if df_clean.shape == df.shape:
        print(f"No NaN values found in {df_name}.")

    return df_clean

def aavso_conv(input_file_path, star_name, band ='Vis.'):
    """
    Convert photometry data files for use in the AAVSO VStar program.

    This function processes photometry data files by reading input files in
    various formats (CSV, TAB-separated, or Excel), transforming the data
    according to predefined mappings, and saving the result in a standardized
    format suitable for use in the AAVSO VStar program. The output file will
    be saved in the same directory as the input file with '_aavso_converted.txt'
    appended to the original filename. Current setup is geared to support output 
    AstroimageJ file formats

    Parameters:
        input_file_path (str): The path to the input file. This can be a CSV,
                               TAB-separated, or Excel file format.
        star_name (str): The name of the target star, which will be included
                         in the 'Star Name' column of the output file.
        band (str): The photometric band utalized during the observation. Defaults to 'Vis.'. 
                    This value will be used in the 'Band' column of the output file.
    """
    
    # Define the column mappings
    label_mapping = {
        'J.D.-2400000': 'JD',
        'Source_AMag_T1': 'Magnitude',
        'Source_AMag_Err_T1': 'Uncertainty',
        'Band': 'Band',
        'AIRMASS': 'Airmass',
        # Add more mappings as needed
    }

    # Define the output columns in the desired order
    output_columns = [
        'JD', 'Magnitude', 'Uncertainty', 'HQuncertainty', 'Band', 'Observer Code', 
        'Comment Code(s)', 'Comp Star 1', 'Comp Star 2', 'Charts', 'Comments', 
        'Transformed', 'Airmass', 'Validation Flag', 'Cmag', 'Kmag', 'HJD', 
        'Star Name', 'Observer Affiliation', 'Measurement Method', 
        'Grouping Method', 'ADS Reference', 'Digitizer', 'Credit'
    ]

    try:
        # Determine the file extension
        file_extension = os.path.splitext(input_file_path)[1].lower()
        
        # Read the data based on the file extension
        if file_extension == '.csv':
            data = pd.read_csv(input_file_path)
        elif file_extension == '.tbl':
            data = pd.read_csv(input_file_path, delimiter='\t')
        elif file_extension in ['.xlsx', '.xls']:
            data = pd.read_excel(input_file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Rename columns based on the mapping
        data.rename(columns=label_mapping, inplace=True)

        # Add any columns not in the mapping and fill with NaN (for blank values)
        for column in output_columns:
            if column not in data.columns:
                data[column] = pd.NA

        # Set default values for specific columns
        data['Band'] = band
        data['Validation Flag'] = 'V'
        data['Star Name'] = star_name

        # Reorder columns to match the output columns
        data = data[output_columns]

        # Determine output file path
        base_name, _ = os.path.splitext(input_file_path)
        output_file_path = f"{base_name}_aavso_converted.txt"

        # Save the transformed data to a text file
        data.to_csv(output_file_path, sep='\t', index=False)

        print(f"Success: Data has been transformed and saved to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    '''Example usage:
    
    input_file_path = r"C:\Users\Zachary\Desktop\Observatory\v0865-lyr_master - Copy.xlsx"  # Adjust the path and format accordingl
    star_name = "V0865 lyr"
    aavso_conv(input_file_path, star_name)
    
    '''