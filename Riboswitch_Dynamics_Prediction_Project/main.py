from helpers import *

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
        temp_traj= read_trajectory(fp)

        #formats the trajectory and appends it to the list of trajectories
        trajectories.append(create_dataframes_by_timestamp(temp_traj))

    #calls function to create a df with averaged positional values
    avg_traj = average_values(trajectories[0], trajectories[1], trajectories[2])

    return avg_traj