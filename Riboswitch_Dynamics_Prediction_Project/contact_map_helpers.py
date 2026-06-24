import pandas as pd
import numpy as np
from oxDNA_analysis_tools.contact_map import contact_map
from oxDNA_analysis_tools.UTILS.RyeReader import describe

def calculate_contact_map(traj_filepath, top_filepath):

    """
    Uses oxDNA analysis tools to calculate the average contact map for the averaged trajectory data.
    Saves the contact maps as an svg and records data in a configuration file.
    
    Args:

        traj_filepath (str): file path to the trajectory data that you want to calculate the contact map for-- this is a the parsed + averaged trajectory
        top_filepath (str): file path to the topology file

    Returns:

        contact_map_df (pd.DataFrame): dataframe containing the average contact map values for the trajectory
    
    """

    top_info, traj_info = describe(top_filepath, traj_filepath)

    cm = contact_map(traj_info, top_info)

    # gets the upper triangle of the contact matrix - since it is symmetric
    indecies = np.triu_indices_from(cm, k=0)
    vals = cm[indecies] #extract correpsonding values
    
    #calculate the mean
    mean = np.mean(vals)

    return mean

    
