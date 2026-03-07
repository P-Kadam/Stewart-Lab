from .helpers import _read_trajectory, _create_dataframes_by_timestamp, _average_values

def prep_trajectory_data(filepaths):

    """

    Creates a properly formatted dataframe with all 3 averaged trajectory datas in a single data frame

    Args:
        filepaths (list): list of filepaths --> SHOULD ONLY CONTAIN 3 FILEPATHS

    Returns:
        pd.DataFrame containing averaged positional values of all 3 trajectories
    
    """

    #create a list to store all the formatted trajectories
    trajectories = []
    
    #iterates through specific range to produce correct numbers corresponding to trail number
    for fp in filepaths:

        #adds the unformatted trajectory to a temporary variable
        temp_traj= _read_trajectory(fp)

        #formats the trajectory and appends it to the list of trajectories
        trajectories.append(_create_dataframes_by_timestamp(temp_traj))

    #calls function to create a df with averaged positional values
    avg_traj = _average_values(trajectories[0], trajectories[1], trajectories[2])

    return avg_traj
