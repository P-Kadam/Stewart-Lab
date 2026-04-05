import numpy as np
import pandas as pd

def read_energy_file(energy_filepath):

    """
    Reads the energy file as a list of 4 arrays that separate the dt, PE, KE, and TE values

    Args:
    
        energy_filepath (string): path to the energy file that needs to be read

    Returns:

        (list) of 4 arrays containing dt, PE, KE, and TE values from the energy file

    """
    
    #open the energy file and specify to read it
    energy_file = open(energy_filepath, 'r')

    store_dt = []
    store_PE = []
    store_KE = []
    store_TE = []

    store_entry = []
    
    for line in energy_file:
        temp_line = line.strip()
        store_entry += temp_line.split()

    energy_file.close()

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



def parse_energies(energy_entries, parsed_energy_filename):

    """
    Removes initial 10% of the averaged energy dataframe and saves the parsed energy values as a new csv file

    Args:

        energy_entries (list): list of 4 arrays containing dt, PE, KE, and TE values from the energy file
        parsed_energy_filename (string): name to save parsed energy file under

    Returns:

        parsed_energy_df (pd.DataFrame): dataframe containing the parsed energy values

    """

    dt, PE, KE, TE = energy_entries

    parsed_energy_df = pd.DataFrame({"dt" : dt[1001: ],
                                     "Potential Energy (SU)" : PE[1001: ],
                                     "Kinetic Energy (SU)" : KE[1001: ],
                                     "Total Energy (SU)" : TE[1001: ]
                                    })

    parsed_energy_df.to_csv(f"parsed_energy_{parsed_energy_filename}.csv")
    
    return parsed_energy_df


def average_energy_files(parsed_energy_dfs, averaged_energy_filename):

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

    averaged_energy_df.to_csv(f"averaged_energy_{averaged_energy_filename}.csv")

    return averaged_energy_df
    