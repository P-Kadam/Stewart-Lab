# from prep_trajectory_helpers import *
from prep_traj_helpers import *
from pathlib import Path
import pandas as pd


def prep_trajectory_data(filepaths, parsed_traj_names, aligned_traj_names, arms, conformation, temp_condition, salt_concentration):

    """

    Creates a properly formatted dataframe with all 3 averaged trajectory datas in a single data frame

    Args:
        filepaths (list): list of filepaths --> SHOULD ONLY CONTAIN 3 FILEPATHS
        parsed_traj_names (list): list of names for the parsed trajectory output files --> SHOULD ONLY CONTAIN 3 FILEPATHS
        aligned_traj_names (list): list of names for the aligned trajectory output files --> SHOULD ONLY CONTAIN 3 FILEPATHS

    Returns:
        pd.DataFrame containing averaged positional values of all 3 trajectories
    
    """

    #create a list to store all the formatted trajectories
    trajectories = []

    #every replicate runs the same number of steps and the same fraction is
    #parsed from each, so complete aligned files share an identical line count.
    #if a prior run already produced a complete set, reuse them so an
    #interrupted run can resume without re-parsing and re-aligning.
    aligned_folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_aligned_trajectory_files")
    aligned_filepaths = [str(aligned_folder / name) for name in aligned_traj_names]
    reuse = aligned_files_reusable(aligned_filepaths)

    if reuse:
        if (aligned_folder / "averaged_trajectory.csv").is_file():
            print("☑️ INFO: Found a complete set of aligned trajectories and an averaged trajectory - reusing them.")
            #the CSV is a flattened version of the list of per-frame DataFrames,
            #with a "frame" column marking which frame each row belongs to;
            #split it back into one DataFrame per frame to restore the original structure
            flat = pd.read_csv(aligned_folder / "averaged_trajectory.csv")
            avg_traj = [group.drop(columns="frame").reset_index(drop=True)
                        for _, group in flat.groupby("frame", sort=True)]
            return avg_traj
        else:
            print("☑️ INFO: Found a complete set of aligned trajectories - reusing them.")

    #iterates through specific range to produce correct numbers corresponding to trail number
    for i in range(len(filepaths)):

        #adds the unformatted trajectory to a temporary variable
        temp_traj= align_trajectory(filepaths[i],
                                    parsed_traj_names[i],
                                    aligned_traj_names[i],
                                    arms,
                                    conformation,
                                    temp_condition,
                                    salt_concentration,
                                    reuse)

        #formats the trajectory and appends it to the list of trajectories
        trajectories.append(create_dataframes_by_timestamp(temp_traj))
        print("\n")

    print("☑️ INFO: Trajectory data has been prepared. Now averaging trajectories!")

    #calls function to create a df with averaged positional values
    avg_traj = average_values(trajectories[0], trajectories[1], trajectories[2])

    #avg_traj is a list of per-frame DataFrames; flatten it into a single CSV by
    #stacking the frames and tagging each row with its frame index so the list
    #structure can be rebuilt on reuse (a plain DataFrame.to_csv would fail on a list)
    flattened = pd.concat({i: df for i, df in enumerate(avg_traj)}, names=["frame"]).reset_index(level="frame")
    flattened.to_csv(aligned_folder / "averaged_trajectory.csv", index=False)
    print("☑️ INFO: Averaged trajectory has been created and saved.")

    return avg_traj

