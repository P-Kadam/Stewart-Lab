import numpy as np
import pandas as pd
from pathlib import Path

def read_energy_file(energy_filepath):

    """
    Reads the energy file as a list of 4 arrays that separate the dt, PE, KE, and TE values

    Args:
    
        energy_filepath (string): path to the energy file that needs to be read

    Returns:

        (list) of 4 arrays containing dt, PE, KE, and TE values from the energy file

    """
    
    store_dt = []
    store_PE = []
    store_KE = []
    store_TE = []

    store_entry = []

    with open(energy_filepath, 'r') as energy_file:
        for line in energy_file:
            temp_line = line.strip()
            store_entry += temp_line.split()

    for i in range(len(store_entry)):
        if i % 4 == 0:
            store_dt.append(float(store_entry[i]))
        elif (i - 1) % 4 == 0:
             store_PE.append(float(store_entry[i]))
        elif (i - 2) % 4 == 0:
             store_KE.append(float(store_entry[i]))
        else:
             store_TE.append(float(store_entry[i]))

    # energy_df = pd.DataFrame({"dt" : np.array(store_dt), 
    #                           "Potential Energy (SU)" : np.array(store_PE),
    #                           "Kinetic Energy (SU)" : np.array(store_KE),
    #                           "
                              
    return [np.array(store_dt), np.array(store_PE), np.array(store_KE), np.array(store_TE)]



def parse_energies(energy_entries, parsed_energy_filename, arms, conformation, temp_condition, salt_concentration):

    """
    Removes initial unequilibrated portion of the averaged energy dataframe and saves the parsed energy values as a new csv file

    Args:

        energy_entries (list): list of 4 arrays containing dt, PE, KE, and TE values from the energy file
        parsed_energy_filename (string): name to save parsed energy file under

    Returns:

        parsed_energy_df (pd.DataFrame): dataframe containing the parsed energy values

    """

    dt, PE, KE, TE = energy_entries

    parsed_energy_df = pd.DataFrame({"dt" : dt[6667: ],
                                     "Potential Energy (SU)" : PE[6667: ],
                                     "Kinetic Energy (SU)" : KE[6667: ],
                                     "Total Energy (SU)" : TE[6667: ]
                                    })

    folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_energy_files")
    
    # Create the compiled_data folder if it doesn't already exist
    folder.mkdir(parents=True, exist_ok=True) 
    filename = f"parsed_energy_{parsed_energy_filename}.csv"
    file_path = folder / filename

    parsed_energy_df.to_csv(file_path, index=False)
    
    return parsed_energy_df


def average_energy_files(parsed_energy_dfs, averaged_energy_filename, arms, conformation, temp_condition, salt_concentration):

    """
    Calculates the average of the energy values across multiple parsed energy dataframes and 
    saves the averaged energy values as a new csv file

    Args:

        energy_files (list): list containing all the energy files that need to be averaged

    Returns:

        averaged_energy_df (pd.DataFrame): dataframe containing the averaged energy values

    """

    avg_dt = np.array([])
    avg_PE = np.array([])
    avg_KE = np.array([])
    avg_TE = np.array([])

    entries = [ [df["dt"], 
                 df["Potential Energy (SU)"],
                 df["Kinetic Energy (SU)"],
                 df["Total Energy (SU)"]]
                 for df in parsed_energy_dfs]
    
    avg_dt, avg_PE, avg_KE, avg_TE = [sum(vals) / len(vals) for vals in zip(*entries)]

    #if you only want the energy values just return this data frame
    averaged_energy_df = pd.DataFrame({"dt" : avg_dt, 
                              "Potential Energy (SU)" : avg_PE, 
                              "Kinetic Energy (SU)" : avg_KE, 
                              "Total Energy (SU)" : avg_TE})
    
    folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files")
    
    # Create the compiled_data folder if it doesn't already exist
    folder.mkdir(parents=True, exist_ok=True) 
    filename = f"averaged_energy_{averaged_energy_filename}"
    file_path = folder / filename

    averaged_energy_df.to_csv(file_path, index=False)

    return averaged_energy_df

def count_lines(filepath):
    """
    Counts the number of lines in a file.

    Args:
        filepath (str): The path to the file.

    Returns:
        int: The number of lines in the file, or None if the file does not exist.
    """
    try:
        with open(filepath, 'r') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return None