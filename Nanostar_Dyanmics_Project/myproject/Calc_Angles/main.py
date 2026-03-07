from .helpers import _find_arm_indecies, _find_center_of_mass, _calculate_angle_between_arms

def calc_angles(dataframes, topFile, SE, armNums, SEspacer, coreSpacer):

    """
    Returns the angles for each theta at all the different time points.

    Args:
        dataframes (list[pd.DataFrames]): List of DataFrames containing particle positions.

    Returns:
        list of angles for each theta value at each time point
    """

    avg_core_indecies, end_indecies = _find_arm_indecies(topFile, SE, armNums, SEspacer, coreSpacer)
    com_dfs = _find_center_of_mass(dataframes, avg_core_indecies)


    #stores arm indecies for different valency nanostars
    arm_indecies = {
                    3 : [0, 39, 78, 0],
                    4 : [0, 78, 117, 39, 0],
                    5 : [0, 78, 117, 157, 39, 0]
                    }

    #Raise value error for invalid NS valency
    if(armNums < 3 or armNums > 5):
        raise ValueError("Incorrect valency nanostar inputted. Please input valencies between 3 and 5 in the 'armNums' parameter.")

    #determines which indecies should be used
    use = arm_indecies[armNums]

    theta_values = {}
    for i in range(len(use) - 1):
        theta = _calculate_angle_between_arms(dataframes, com_dfs, use[i], use[i + 1])
        theta_values[f"θ{i+1}"] = theta

    return pd.DataFrame(theta_values)
