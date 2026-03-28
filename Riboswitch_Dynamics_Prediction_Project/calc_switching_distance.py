from oxDNA_analysis_tools.distance import distance
from oxDNA_analysis_tools.UTILS.RyeReader import describe

def calc_switching_distance(traj_filepath, data_df):

    """
        Calculate the distance between specified NTs in the P1 and anti-P1 stems for each frame of the trajectory, and add these distances as new columns to the provided DataFrame.

        Args:
            traj_filepath (str): The file path to the trajectory data.
            data_df (pd.DataFrame): The DataFrame to which the distance columns will be added

        Returns:
            pd.DataFrame: The updated DataFrame with new columns for the P1 stem NT distance and the anti-P1 stem NT distance.
    """
    # Use the describe function to get the top_info and traj_info from the trajectory file
    top_info, traj_info = describe(None, traj_filepath)

    distances = distance(
        [traj_info],        # list of TrajInfo objects
        [top_info],         # list of TopInfo objects
        [[56, 62]],        # p1ss — list of lists of nucleotide indices -- change the NTs based on desired distances
        [[150, 209]]        # p2ss — list of lists of nucleotide indices -- change the NTs based on desired distances
    )

    # Add the calculated distances to the DataFrame as new columns
    data_df["P1 stem NT distance (nm)"] = (distances[0])[0]
    data_df["anti-P1 stem NT distance (SU)"] = (distances[0])[1]

    #returns the updated DataFrame with the new distance columns
    return data_df