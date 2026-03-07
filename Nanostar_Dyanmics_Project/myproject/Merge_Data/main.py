import pandas as pd

def merge_data(dfs, temperatures, salt, filename):
    """
    Merge multiple dataframes into a single long-format dataframe.

    Parameters:
        dfs (list of pd.DataFrame): list of dataframes (columns = theta1, theta2, ...)
        temperatures (list of str): labels for each dataframe (temperature conditions)
        salt (list of str) : labels for each df (monovalent salt concentration)

    Returns:
        pd.DataFrame: columns = ['Temperature','Salt', 'Theta', 'Value']
    """
    merged_list = []

    for df, temp, salt in zip(dfs, temperatures, salt):
        # Melt to long format
        df_long = df.melt(var_name='Theta', value_name='Angle')
        # Add temperature column
        df_long['Temperature'] = temp
        df_long['Salt'] = salt
        merged_list.append(df_long)

    # Concatenate all into one dataframe
    df_all = pd.concat(merged_list, ignore_index=True)

    df_all = df_all[['Temperature', 'Salt', 'Theta', 'Angle']]

    df_all.to_csv(f"{filename}.csv", index=False)

    return df_all
