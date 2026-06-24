from pathlib import Path

def save_dataframe_to_csv(data_df, filename, arms, conformation, temp_condition, salt_concentration):
    """
    Saves the provided DataFrame to a CSV file with the specified filename.
    
    Parameters:
    data_df (pd.DataFrame): The DataFrame to be saved.
    filename (str): The name of the CSV file to save the DataFrame to.
    """

    folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files")
    
    # Create the compiled_data folder if it doesn't already exist
    folder.mkdir(parents=True, exist_ok=True) 

    file_path = folder / filename
    
    data_df.to_csv(file_path, index=False)

    return "INFO: DataFrame saved to " + filename