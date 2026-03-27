import numpy as np
import pandas as pd

def calc_RMSD(averaged_dfs, data_df, arms, conformation, temp_condition, salt_concentration):

    """
    Calculates the RMSD

    Args:
    
        averaged_dfs (list): list of averaged data frames corresponding to each simulation timepoint --> returned from prep_trajectory_data function
        data_df (pd.DataFrame): Dataframe containing all the feature-engineered data
        arms (int): integer number of arms
        conformation (str): string indicating the conformation
        temp_condition (str): string indicating the temperature condition
        salt_concentration (str): string indicating the salt concentration
        

    Returns:

        pd.DataFrame of the RMSD values with the index corresponding to the timept within the simulation
    """

    reference_frame = averaged_dfs[0]

    temp_rmsd_store = []

    for tp_df in averaged_dfs:

        diff = tp_df - reference_frame

        x = (diff['X']) ** 2
        y = (diff['Y']) ** 2
        z = (diff['Z']) ** 2

        sum_series = x + y + z
        
        rmsd = np.sqrt(sum_series.sum() / len(tp_df))

        temp_rmsd_store.append(rmsd)

    #account for simulation units -- 1 SU = 0.8518 nm = 8.518 Å
    

    data_df['RMSD (Å)'] = temp_rmsd_store

    data_df['RMSD (Å)'] *= 8.518

    data_df.to_csv(f"{arms}NS_{conformation}_{temp_condition}_{salt_concentration}_test.csv")
    
    return data_df
    