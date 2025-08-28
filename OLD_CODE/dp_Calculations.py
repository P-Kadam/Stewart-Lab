import pandas as pd
import numpy as np
import statistics


##=====================
##TRAJECTROY PREP
##=====================

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


##=====================
##ARM INDEX
##=====================

def find_arm_indecies(filepath, SE, armNum, SEspacer, coreSpacer):

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
    topology = read_topology_data(filepath)

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



##=====================
##DF CREATION
##=====================

def create_dataframes_by_timestamp(data):
    """Creates separate DataFrames for each timestamp in the data.

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

    #
    for i in range(len(data)):

        comx = data.iloc[i, 0]

        if comx == "t":
            timestamp_counter += 1
            xrows.append([])
            yrows.append([])
            zrows.append([])
            continue
        
        if comx == "t" or comx == "b" or comx == "E":
            skiplist = i
        
        if skiplist != i:
            
            xrows[timestamp_counter].append(comx)
            yrows[timestamp_counter].append(comy := data.iloc[i, 1])
            zrows[timestamp_counter].append(comz := data.iloc[i, 2])

    for x, y, z in zip(xrows, yrows, zrows):
        dataframes.append(pd.DataFrame({"X": x, "Y": y, "Z": z}))

    return dataframes


##=====================
## DF AVG
##=====================


def average_values(df1, df2, df3):
    
    avg_dfs = []
    for i in range(len(df1)):
        # print(df1[i])
        
        X_avg, Y_avg, Z_avg = [], [], []

        for j in range(len(df1[0])):

            X_avg.append(statistics.mean([float(df1[i].iloc[j, 0]), float(df2[i].iloc[j, 0]), float(df3[i].iloc[j, 0])]))
            Y_avg.append(statistics.mean([float(df1[i].iloc[j, 1]), float(df2[i].iloc[j, 1]), float(df3[i].iloc[j, 1])]))
            Z_avg.append(statistics.mean([float(df1[i].iloc[j, 2]), float(df2[i].iloc[j, 2]), float(df3[i].iloc[j, 2])]))
            
        avg_dfs.append(pd.DataFrame({"X": X_avg, "Y": Y_avg, "Z" : Z_avg}))
    
    return avg_dfs


##=====================
## PUBLIC FUNCTION
##=====================


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


##=====================
## READ TOP
##=====================


def read_topology_data(filepath):
    
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


##=====================
## FIND COM
##=====================


def find_center_of_mass(dataframes, core_indecies):
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


##=====================
## TEST DATA
##=====================


traj_50C_75M = prep_trajectory_data(["/Users/pradnyakadam/Downloads/ACS_Manuscript/Simulation_Output_Files/3_Arm/50C_0.75M/trajectory_files/trajectory_50C_0.75M_sim_revised_1.dat",
                                   "/Users/pradnyakadam/Downloads/ACS_Manuscript/Simulation_Output_Files/3_Arm/50C_0.75M/trajectory_files/trajectory_50C_0.75M_sim_revised_2.dat",
                                   "/Users/pradnyakadam/Downloads/ACS_Manuscript/Simulation_Output_Files/3_Arm/50C_0.75M/trajectory_files/trajectory_50C_0.75M_sim_revised_3.dat"])

##=====================
## DISTANCE CALC
##=====================

def point_plane_distance(A, B, C, D, point):
    """
    Computes the distance from a point to the plane Ax + By + Cz + D = 0
    """
    x0, y0, z0 = point
    numerator = abs(A*x0 + B*y0 + C*z0 + D)
    denominator = np.sqrt(A**2 + B**2 + C**2)
    return numerator / denominator


import numpy as np
import statistics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Import for 3D plotting

dist = []

dataframes = traj_50C_75M
topFile = "/Users/pradnyakadam/Downloads/ACS_Manuscript/3_arm_INPUT_FILES/3m1_6NT1_2bp.top"

avg_core_indecies, end_indecies = find_arm_indecies(topFile, 6, 4, 1, 2)
com_dfs = find_center_of_mass(dataframes, avg_core_indecies)

# print(com_dfs)

for df in dataframes:
    
    #defines the starting point as the coordinates position associated with the particular timestamp
    #refernce comment above for more info.
    start_pt = np.array([com_dfs.iloc[0, 0], com_dfs.iloc[0, 1], com_dfs.iloc[0, 2]])
    
    
    #defining vector 1 end point based on the provided index
    pt_1 = np.array([float(df.iloc[0, 0]), float(df.iloc[0, 1]), float(df.iloc[0, 2])])
    
    
    # #defining vector 2 end point based on the other provided index
    pt_2 = np.array([float(df.iloc[39, 0]), float(df.iloc[39, 1]), float(df.iloc[39, 2])])
    
    # #defining vector 2 end point based on the other provided index
    pt_3 = np.array([float(df.iloc[78, 0]), float(df.iloc[78, 1]), float(df.iloc[78, 2])])
    
    # end_pt_4 = np.array([float(df.iloc[39, 0]), float(df.iloc[39, 1]), float(df.iloc[39, 2])])


    # CURRENTLY ONLY THE LAST TIME POINT SURFACE
    # #defining each vector to represent an arm of the nanostar
    
    v1 = pt_2 - pt_1
    v2 = pt_3 - pt_1
    
    
    #calculate the cross product
    #|v1 x v2| = |v1||v2|sin(theta)n
    
    cross = np.cross(v1, v2)
    
    A, B, C = cross
    
    D = -np.dot(cross, pt_1)

    # print(f"Plane equation: {A}x + {B}y + {C}z + {D} = 0")

    distance = point_plane_distance(A, B, C, D, start_pt)
    dist.append(distance)
    
    # x = np.linspace(-10, 10, 10)
    # y = np.linspace(-10, 10, 10)
    
    # X, Y = np.meshgrid(x, y)
    
    # Example: Plane equation x + y + 2z = 9
    # Z = (9 - X - Y) / 2
    
    #Ax + By + Cz + D = 0
    
    # Z = (-D - B*Y - A*X)
    
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(X, Y, Z, alpha=0.7) # alpha controls transparency
    
    # ax.set_xlabel('X-axis')
    # ax.set_ylabel('Y-axis')
    # ax.set_zlabel('Z-axis')
    # ax.set_title('Graph of a Plane')
    
    # plt.show()

x = np.array(range(0, 10000, 1))

fig, ax  = plt.subplots(1)
plt.plot(x, dist)


    #Calculating the distance between the point and the plane
    

avg_distance = statistics.mean(dist)
dp = avg_distance/100

print("The dp for 3 NS 50C 0.75M simulation is:", round(dp, 1))