import pandas as pd
import numpy as np
from pathlib import Path

def calc_COM_nonuniform_structure(averaged_dfs, arms, conformation, temp_condition, salt_concentration):

    """
    Calculates the center of mass of an irregular RNA structure (not a nanostar)

    Args:

    averaged_dfs (list): list of averaged data frames corresponding to each simulation timepoint --> returned from prep_trajectory_data function
    arms (int): integer number of arms

    Returns:

        pd.DataFrames that contain center of mass coordinates, with each index corresponding to the timepoint in the trajectory

    """

    folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files")
    if not (folder / "COM_df.csv").is_file():
        print("☑️ INFO: COM calculation initiated!")

        timept_COM_coords = []

        NT_mass = 315.56

        mass_summation = NT_mass * len(averaged_dfs[0])

        # For each timepoint in the list of dataframes
        for tp_df in averaged_dfs:

            #Temporary list that will hold the data values
            temp_COM_list = []

            # multiply the positional value with the mass value-- defined as a constant NT_mass and get the summation
            # divide the summation by the summation of the mass values (mass * num of NTs)        
            x = ((tp_df['X'] * NT_mass).sum()) / mass_summation
            y = ((tp_df['Y'] * NT_mass).sum()) / mass_summation
            z = ((tp_df['Z'] * NT_mass).sum()) / mass_summation     
                
            #store COM coordinates in a list-- index of the list corresponds with the timepoint (stored as a list)
            timept_COM_coords.append([x, y, z])


        # Use list of coordinates to create a df for the trajectory
        COM_df = pd.DataFrame(timept_COM_coords)
        
    
        #add column names
        COM_df.columns = ['X', 'Y', 'Z']
        COM_df.to_csv(folder / "COM_df.csv", index=False)
        print("☑️INFO: Center of mass has been calculated for each timepoint in the trajectory.")

    else:
        print("☑️INFO: COM file already exists.")
        print("\n")
        COM_df = pd.read_csv(folder / "COM_df.csv")

    # return the COM list
    return COM_df