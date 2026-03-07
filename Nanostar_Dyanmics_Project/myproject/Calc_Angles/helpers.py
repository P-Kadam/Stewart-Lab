#################################
# HELPER FUNCTION 1
################################

def _read_topology_data(filepath):
    
    """Reads topology data from a .top file.

    Args:
        filepath (str): Path to the .top file containing trajectory data.

    Returns:
        pd.DataFrame of the topology file
    """
    
    # Load your dataset
    df = pd.read_csv(filepath, header = None)
    
    # Remove the first row
    df = df.iloc[1:].reset_index(drop=True)
    df = df.iloc[:, 0]


    #returns the formatted topology file
    return df


#################################
# HELPER FUNCTION 2
################################

def _find_arm_indecies(filepath, SE, armNum, SEspacer, coreSpacer):

    """
    Finds the index numbers that correspond to a single arm. Will append these indecies to core and end lists

    Args:
        filepath (str): Path to the .top file containing trajectory data.
        SE (int): The number of sticky ends on a strand
        armNum (int): The number of arms the nanostar has
        SEspacer (int): The number of nucleotides that make up the spacer before the SE
        starting_indecies (list)
        ending_indecies (list)

    Returns:
        core and end indeciex list
    """
    #reads in the topology data
    topology = _read_topology_data(filepath)

    # print(topology)

    strandCount = 0
    index_count = 0

    #Calculate the length of the strand
    strandLength = (topology.size)/armNum
    # print(strandLength)
    seq_length = int(strandLength-SE-SEspacer-coreSpacer)/2

    i = 0

    #defines a single strand that makes up the double stranded arm
    s = 0

    #defines whether the end of the double stranded arm has been reached
    end = False


    #list holds all the indecies for the core and ends
    indecies = []

    #continues to loop
    while True:

        #appends each index, will start by appending an index of 0
        # print(topology.iloc[i])
        indecies.append(i)

        #if the stand number is even
        #checks for the start of a single strand
        if s%2 == 0:

            #single strands have a length of 15 nucleotides
            #this will find the ending of the single strand
            #seqlengh -1
            i+= 14

        #if instead at the end of the single strand
        elif end == False:

            #add 3 to account for the core spacers and to move to the start of the next single strand
            #that makes up the double stranded arm
            #coreSpacer + 1
            i+= 3
            

            #also sents end to TRUE since the end of the double strand is approaching
            end = True

        #when the end of the double stranded arm is reached (end = TRUE)
        else:

            #accounts for the spacer and the SE to go to the next strand
            #SE + SEspacer + 1
            i+= 8

            #sets end to FALSE again since a new strand has started
            end = False

        #exit condition
        if i >= topology.size:
            break

        #incremented each time an index is added
        s+= 1

    #creating core and end indecies list
    core_indecies = []
    end_indecies = []

    #appends the first element to the end_indecies list
    end_indecies.append(indecies[0])

    #used to append every 2 elements from indecies into respective list
    loop = 1

    #round - used to alternate appending to the end or core indecies lists
    rnd = 0

    #continues to run
    while True:

        #if the loop index exceeds the bound for the index
        if (loop + 2) >= len(indecies):
            #break the while loop
            break

        #if the round is even
        if rnd % 2 == 0:
            #append the indecies to core_indecies list
            core_indecies.append((indecies[loop], indecies[loop+1]))

        #if the round is odd
        else:
            #append the idencies to end_indecies list
            end_indecies.append(indecies[loop+1])

        #increment the loop by 2 to account for appending every 2 elements to a different list
        loop += 2
        #increment the loop by 1 to do binary list selection
        rnd +=1

    

    avg_core = []

    #Take averages of the core index pairs
    for pair in core_indecies:
        avg_core.append(int(statistics.mean(pair)))

    #

    return avg_core, end_indecies


#################################
# HELPER FUNCTION 3
################################

def _core_NTs(dfs, SE, armNum, seq_len, core_len, SEspacer):

    """
    Calculates the indecies of the core nucleotides

    Args:
        dfs (df of dfs): data frame containing dataframes of nucleotide positions corresponding to each time point
        SE (int): the number of sticky ends in a strand
        seq_len (int): the length of a sequence
        core_len (int): the number of core nucleotides in a strand
        SEspacer (int): the number of sticky end spacers on a strand

    Returns:
        The core indecies
        
    """
    
    #list stores core NT line #s
    core = []
    
    jump = 0
    
    #calcs the # of NTs in each arm, excluding SE + spacer
    arm_len = (seq_len - core_len - SEspacer - SE)/2
    
    for c in range(0, arms):
        
        line = int(arm_len) + jump
        
        core.append(int(line))
        
        
        core.append(int(line + 1))
        
        jump += seq_len
        
    return core


#################################
# HELPER FUNCTION 4
################################

def _find_center_of_mass(dataframes, core_indecies):
    """Calculates the average center of mass for core nucleotides at each timestamp.

    Args:
        dataframes (list[pd.DataFrame]): List of DataFrames containing particle positions.
        core_nucleotides (int): Number of core nucleotides in the nanostar.
        arms (int): Number of arms in the nanostar.
        sequence_length (int): Total sequence length of the nanostar.

    Returns:
        pd.DataFrame: Dataframe containing average center of mass (COM) for each timestamp.
        Each row of the Dataframe corresponds to a new timestamp.
    """

    #creates a list to store average X, Y, and Z center of mass coordinates
    x_avg, y_avg, z_avg = [], [], []
    
    # arm_length = int((sequence_length - core_nucleotides) / (2 * armNum))

    #iterates through each time point's dataframe
    for df in dataframes:

        #creates lists to store the coordinates corresponding to each index in core_indecies list
        #stores the x, y, and z coordinates separately
        x_centers, y_centers, z_centers = [], [], []

        #iterates through the indecies in the core_indecies list
        for index in core_indecies:

            #adds the corresponding positional coordinate to its respective list
            x_centers.append(float(df.iloc[index, 0]))
            y_centers.append(float(df.iloc[index, 1]))
            z_centers.append(float(df.iloc[index, 2]))
                

        #averages the positional coordinates stored in the x, y, and z centers lists
        #this will provide the average center of mass at a single time point
        x_avg.append(statistics.mean(x_centers))
        y_avg.append(statistics.mean(y_centers))
        z_avg.append(statistics.mean(z_centers))

    return pd.DataFrame({"COM_X": x_avg, "COM_Y": y_avg, "COM_Z": z_avg})

#################################
# HELPER FUNCTION 5
################################

def _calculate_angle_between_arms(dataframes, com_dataframe, arm1_index, arm2_index):
    """Calculates the angle between two specified arms at each timestamp.

    Args:
        dataframes (list[pd.DataFrame]): List of DataFrames containing particle positions.
        com_dataframe (pd.DataFrame): Dataframe containing center of mass (COM) positions.


    Returns:
        list of angles formed by the selected arms over all the time points
    """

    #variable to iterate through each line of the center of mass df
    #as mentioned above each line of the com_dataframe represents a single timestamp of the simulation
    #this will ensure that each starting point is at the center of mass for the specific timestamp
    com_df = 0

    #list to hold all the angles created between two arms
    angles_list = []

    #iterates through each time point's dataframe
    for df in dataframes:

        #defines the starting point as the coordinates position associated with the particular timestamp
        #refernce comment above for more info.
        start_pt = np.array([com_dataframe.iloc[com_df, 0], com_dataframe.iloc[com_df, 1], com_dataframe.iloc[com_df, 2]])
#         print("start: ", start_pt)

        #defining vector 1 end point based on the provided index
        end_pt_1 = np.array([float(df.iloc[arm1_index, 0]), float(df.iloc[arm1_index, 1]), float(df.iloc[arm1_index, 2])])
#         print("ep1: ", end_pt_1)

        #defining vector 2 end point based on the other provided index
        end_pt_2 = np.array([float(df.iloc[arm2_index, 0]), float(df.iloc[arm2_index, 1]), float(df.iloc[arm2_index, 2])])
#         print("ep2: ", end_pt_2)

        #increment the com_df variable to go to the next timestamp's ceneter of mass
        com_df += 1

        #defining vectors 1 & 2 based on their corresponding end points
        v1 = end_pt_1 - start_pt
        v2 = end_pt_2 - start_pt

        #using the equation mathematical equation:
        
        #calculating the dot product of the two vectors
        dot_product = np.dot(v1, v2)

        #calculating both vectors' magnitudes
        magnitude1 = np.linalg.norm(v1)
        magnitude2 = np.linalg.norm(v2)

        calc = dot_product / (magnitude1 * magnitude2)

        if calc > 1 or calc < -1:
            calc = 0

        #calculating the angle created between the two vectors (in radians)
        angle_radians = np.arccos(calc)

        #converting that value to degrees
        angle_degrees = np.degrees(angle_radians)
        
#         print("angle degrees: ", angle_degrees)

        #appending the calculated angle (based on the timestamp) to the list creeated above
        angles_list.append(angle_degrees)
        
#         print("done")
    
    return angles_list
