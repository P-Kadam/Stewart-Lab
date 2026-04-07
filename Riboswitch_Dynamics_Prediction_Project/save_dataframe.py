
def save_dataframe_to_csv(data_df, filename):
    """
    Saves the provided DataFrame to a CSV file with the specified filename.
    
    Parameters:
    data_df (pd.DataFrame): The DataFrame to be saved.
    filename (str): The name of the CSV file to save the DataFrame to.
    """
    
    data_df.to_csv(filename, index=False)

    return "INFO: DataFrame saved to " + filename