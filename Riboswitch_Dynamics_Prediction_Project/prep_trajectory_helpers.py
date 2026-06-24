import pandas as pd
import statistics
import subprocess
from oxDNA_analysis_tools.align import align
from pathlib import Path

def read_trajectory(filepath):

    """
    
    Reads the csv file data

    Args:
        filename (str): the path to the file

    Returns:
        pd.DataFrame containing all the data

    """

    data =  pd.read_csv(filepath, usecols=range(3), sep=" ", header = None)
    return data


def count_lines(filepath):

    """
    Counts the number of lines in a file.

    Args:
        filepath (str | Path): the path to the file

    Returns:
        int: the number of lines, or None if the file is missing/empty.
    """

    path = Path(filepath)

    if not path.exists() or path.stat().st_size == 0:
        return None

    with open(path, 'r') as fh:
        return sum(1 for _ in fh)


def aligned_files_reusable(aligned_filepaths):

    """
    Decides whether previously generated aligned trajectory files can be reused
    so an interrupted run can resume without re-parsing and re-aligning.

    Every replicate runs for the same number of steps and the same fraction is
    parsed from each, so a complete aligned file has an identical line count
    across all three triplicates. If all files exist and share the same nonzero
    line count, none were truncated by an interrupt and they can be reused. A
    mismatch (or a missing file) means at least one is incomplete, so everything
    is rebuilt from scratch.

    Args:
        aligned_filepaths (list): paths to the aligned trajectory files

    Returns:
        bool: True if the aligned files can be safely reused.
    """

    counts = [count_lines(p) for p in aligned_filepaths]

    #any missing/empty file means we cannot reuse
    if any(c is None for c in counts):
        return False

    #all triplicates must have the same line count to be considered complete
    return len(set(counts)) == 1


#fixed - allegedly

def align_trajectory(filepath, parsed_file_name, aligned_traj_name, arms, conformation, temp_condition, salt_concentration, reuse=False):

    """ 
    
    Reads the csv file data, aligns the trajectories, and pares off the unequilibrated portion of the data

    Args:
        filename (str): the path to the file
        parsed_file_name (str): name of the parsed trajectory output file
        aligned_traj_name (str): name of the aligned trajectory output file

    Returns:
        pd.DataFrame containing all the aligned data

    """

    folder1 = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_trajectory_files")
    folder2 = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_aligned_trajectory_files")

    filename1 = parsed_file_name
    file_path1 = folder1 / filename1

    filename2 = aligned_traj_name
    file_path2 = folder2 / filename2

    #if a complete aligned file already exists, skip the expensive parse + align
    #and just read it back so an interrupted run can resume
    if reuse and file_path2.exists():
        print(f"☑️ INFO: Reusing existing aligned trajectory '{filename2}' (skipping parse + align).")
        return pd.read_csv(str(file_path2), usecols=range(3), sep=" ", header = None)

    # Create the compiled_data folder if it doesn't already exist
    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'r') as file:
        with open(file_path1, 'w') as f:

            switch = False

            #iterates through each line of content within the file
            for line in file:
        
                #modify this if (1) number of steps sims ran for changes OR (2) if you want more/less than 10% of the data parsed
                #checks whether 10% of data has been read
                if "t = 66670000" in line:
        
                    #indicates that the 10% mark has been hit
                    switch = True
        
                    #uncomment if you want new file to contain t = headers that start at the step count 10000
                    
                    # f.write("t = " + str(t_counter) + "\n")
                    # t_counter += 10000
                    # continue
        
                #if the 10% mark has been hit
                if switch == True:
        
                    #uncomment if you want new file to contain t = headers that start at the step count 10000
                    
                    # if "t =" in line:
                        # f.write("t = " + str(t_counter) + "\n")
                        # t_counter += 10000
                        # continue
        
                    #writes the content in the new file
                    f.write(line)

    #aligns the trajectory with now the reference frame being the first frame from the 10% removed data
    aligned_trajectory = align(str(file_path1), str(file_path2))

    #reads the data into a dataframe
    data =  pd.read_csv(str(file_path2), usecols=range(3), sep=" ", header = None)  

    return data

def create_dataframes_by_timestamp(data):

    """
    Creates separate DataFrames for each timestamp in the data.

    Args:
        data (pd.DataFrame): Dataframe containing particle positions.

    Returns:
        list[pd.DataFrame]: List of DataFrames, each representing a single timestamp.
    """

    # print(data)
    #creating list to hold dataframes
    dataframes = []

    #counts the number of time stamps
    timestamp_counter = -1

    #creating lists for each column on the dataframe
    xrows, yrows, zrows = [], [], []
    
    skiplist = 0

    #iterates through the indecies of the data
    for i in range(len(data)):

        #selects the first value of each row
        comx = data.iloc[i, 0]

        #if the value of the row corresponds to a time stamp
        if comx == "t":

            #increment the timestamp counter by 1
            timestamp_counter += 1

            #create new lists to store each of the data points for the x, y and z positions
            xrows.append([])
            yrows.append([])
            zrows.append([])
            
            continue

        #skip any of the header/time stamp related labels 
        if comx == "t" or comx == "b" or comx == "E":
            skiplist = i

        #if the row was not skipped
        if skiplist != i:

            #append the values of each of the positions to their corresponding list
            xrows[timestamp_counter].append(comx)
            yrows[timestamp_counter].append(comy := data.iloc[i, 1])
            zrows[timestamp_counter].append(comz := data.iloc[i, 2])

    
    for x, y, z in zip(xrows, yrows, zrows):
        dataframes.append(pd.DataFrame({"X": x, "Y": y, "Z": z}))

    return dataframes

def average_values(df1, df2, df3):

    """
    Creates an average pd.DataFrame of all the 3 pd.DataFrames for a specific condition

    Args:
        df1 (pd.DataFrame): trial 1 data frame
        df2 (pd.DataFrame): trial 2 data frame
        df3 (pd.DataFrame): trial 3 data frame

    Returns:
        pd.DataFrame that contains an average of all the values

    """

    #creates a list to store the dfs of each time point
    avg_dfs = []

    #iterates through all the dataframes (index) contained within df1 (list of dataframes)
    for i in range(len(df1)):

        #creates 3 lists to store the positional average values
        X_avg, Y_avg, Z_avg = [], [], []

        #iterates through the values of a single data frame
        for j in range(len(df1[0])):

            #takes the mean and appends the mean value of all 3 dfs positional values at a particular index for x, y and z positions
            X_avg.append(statistics.mean([float(df1[i].iloc[j, 0]), float(df2[i].iloc[j, 0]), float(df3[i].iloc[j, 0])]))
            Y_avg.append(statistics.mean([float(df1[i].iloc[j, 1]), float(df2[i].iloc[j, 1]), float(df3[i].iloc[j, 1])]))
            Z_avg.append(statistics.mean([float(df1[i].iloc[j, 2]), float(df2[i].iloc[j, 2]), float(df3[i].iloc[j, 2])]))

        #creates a complete dataframe for a time point and stores it in the avg_dfs list
        avg_dfs.append(pd.DataFrame({"X": X_avg, "Y": Y_avg, "Z" : Z_avg}))
    
    return avg_dfs