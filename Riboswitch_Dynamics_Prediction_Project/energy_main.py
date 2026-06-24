from energy_helpers import read_energy_file, parse_energies, average_energy_files
from pathlib import Path
import pandas as pd

def process_energies(energy_filepaths, parsed_energy_filenames, averaged_energy_filename, data_df, arms, conformation, temp_condition, salt_concentration):
    """
    Reads in energy files, parses the energy values, averages the energy values across multiple files, and adds the averaged energy values to an existing dataframe

    Args:
        energy_filepaths (list): list containing all the energy files that need to be averaged
        parsed_energy_filenames (list): list of names to save the parsed energy files under
        averaged_energy_filename (string): name to save the averaged energy file under
        data_df (pd.DataFrame): existing dataframe to add the averaged energy values to

    Returns:
        data_df (pd.DataFrame): dataframe with averaged energy values added as new columns
    """

    folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation")
    
    if not folder / f"/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_energy_files/parsed_energy_{parsed_energy_filenames[2]}.csv".is_file() or len(folder / f"/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_energy_files/parsed_energy_{parsed_energy_filenames[0]}.csv") != len(folder / f"/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_energy_files/parsed_energy_{parsed_energy_filenames[1]}.csv") or len(folder / f"/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_energy_files/parsed_energy_{parsed_energy_filenames[0]}.csv") != len(folder / f"/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_energy_files/parsed_energy_{parsed_energy_filenames[2]}.csv"):
        print(f"☑️ INFO: parse + average energy files.")

        parsed_energy_dfs = []
        
        for i, energy_filepath in enumerate(energy_filepaths):

            energy_entries = read_energy_file(energy_filepath)
            parsed_energy_dfs.append(parse_energies(energy_entries, parsed_energy_filenames[i], arms, conformation, temp_condition, salt_concentration))

        avg_energy_df = average_energy_files(parsed_energy_dfs, averaged_energy_filename, arms, conformation, temp_condition, salt_concentration)

        #print(avg_energy_df)
    else:
        print(f"☑️ INFO: Energy files already parsed and averaged. Reading in the averaged energy file.")
        avg_energy_df = pd.read_csv(folder / f"/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_energy_files/{averaged_energy_filename}.csv")
    
    data_df["Potential Energy (SU)"] = avg_energy_df["Potential Energy (SU)"]
    data_df["Kinetic Energy (SU)"] = avg_energy_df["Kinetic Energy (SU)"]
    data_df["Total Energy (SU)"] = avg_energy_df["Total Energy (SU)"]

    print("☑️INFO: Energy values have been processed and added to the dataframe.")

    return data_df