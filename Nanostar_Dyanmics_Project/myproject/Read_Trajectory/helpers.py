import pandas as pd
import statistics


#################################
# HELPER FUNCTION 1
################################

def _read_trajectory(filepath):

    """
    Reads the csv file data

    Args:
        filename (str): the path to the file

    Returns:
        pd.DataFrame containing all the data
    """

    data =  pd.read_csv(filepath, usecols=range(3), sep=" ", header = None)
    return data
    

#################################
# HELPER FUNCTION 2
################################

def _create_dataframes_by_timestamp(data):

    """
    Creates separate DataFrames for each timestamp in the data.

    Args:
        data (pd.DataFrame): Dataframe containing particle positions.

    Returns:
        list[pd.DataFrame]: List of DataFrames, each representing a single timestamp.
    """

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

#################################
# HELPER FUNCTION 3
################################

def _average_values(df1, df2, df3):

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
