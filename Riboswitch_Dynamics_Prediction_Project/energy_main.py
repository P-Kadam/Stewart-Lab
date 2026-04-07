from energy_helpers import read_energy_file, parse_energies, average_energy_files

def process_energies(energy_filepaths, parsed_energy_filenames, averaged_energy_filename, data_df):
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

    parsed_energy_dfs = []
    
    for i, energy_filepath in enumerate(energy_filepaths):

        energy_entries = read_energy_file(energy_filepath)
        parsed_energy_dfs.append(parse_energies(energy_entries, parsed_energy_filenames[i]))

    avg_energy_df = average_energy_files(parsed_energy_dfs, averaged_energy_filename)

    data_df["Potential Energy (SU)"] = avg_energy_df["Potential Energy (SU)"]
    data_df["Kinetic Energy (SU)"] = avg_energy_df["Kinetic Energy (SU)"]
    data_df["Total Energy (SU)"] = avg_energy_df["Total Energy (SU)"]

    return data_df