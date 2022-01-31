from pandas import DataFrame


def convert_dates_to_string(df: DataFrame):
    """Converts dates to strings for ease of display in the front end

            Parameters:
                df (DataFrame): The Pandas DataFrame to have its \
                                dates converted
            Returns:
                df (DataFrame): The Pandas DataFrame with dates \
                                now held as strings

    """
    for column in df:
        if df.dtypes[column] in ['datetime64[ns]', 'object']:
            df[column] = df[column].astype(str)
            df[column] = df[column].replace('nan', '')
    return df


def convert_decimal_to_float(df: DataFrame):
    """
    Converts decimals to floats so they can be transmitted \
    within the JSON response

            Parameters:
                df (DataFrame): The Pandas DataFrame to have \
                                its decimals converted
            Returns:
                df (DataFrame): The Pandas DataFrame with \
                                decimals now held as floats

    """
    for column in df:
        if df.dtypes[column] in ['object']:
            # try:
            df[column] = df[column].astype(float)
            # except:
            #     pass
    return df
