from Calc_COM import *
import math

def calc_radius_of_gyration(averaged_dfs, COM_df, arms, conformation, temp_condition, salt_concentration):

    """
    Calculates the Radius of Gyration for each time point 

    Args:
    
        averaged_dfs (list): list of averaged data frames corresponding to each simulation timepoint --> returned from prep_trajectory_data function
        COM_df (pd.DataFrame): Dataframe outputted from calc_COM_nonuniform_structure

    Returns:

        pd.DataFrame of all the data 

    """
    #Note: mass values changed for each NT, use a list instead of a constant value [A, U, G, C]
    #Also, when formatting the df, create a separate column with the NT identity prior to using this equation
    NT_mass = 315.56

    #Note: when mass values for each NT change, mass_summation will need to count the number of each NTs and multiply the respective mass
    #values to each for the calculation
    mass_summation = NT_mass * len(averaged_dfs[0])

    temp_Rg = []

    for tp_df in averaged_dfs:
    
        # Calculate the position of each NT relative to the center of mass quantity squared
        r_i = (tp_df - COM_df) ** 2
    
        #radius of gyration calculation for each axis
        Rg_x = math.sqrt(( NT_mass * (r_i['Y']**2 + r_i['Z']**2)).sum() / mass_summation)
    
        Rg_y = math.sqrt(( NT_mass * (r_i['X']**2 + r_i['Z']**2)).sum() / mass_summation)
    
        Rg_z = math.sqrt(( NT_mass * (r_i['Y']**2 + r_i['X']**2)).sum() / mass_summation)

        #calculating the standard radius of gyration
        x = r_i['X']
        y = r_i['Y']
        z = r_i['Z']

        series_sum = x + y + z

        std_Rg = math.sqrt( ((NT_mass * series_sum).sum()) / mass_summation)

        #account for simulation units -- 1 SU = 0.8518 nm = 8.518 Å
        std_Rg *= 0.8518
        Rg_x *= 0.8518
        Rg_y *= 0.8518
        Rg_z *= 0.8518

        #store the values of interest along with simulation code, number of arms, temperature condition, and salt concentration in a list
        temp_Rg.append([f"{arms}NS_{conformation}_{temp_condition}_{salt_concentration}", arms, conformation, temp_condition, salt_concentration, std_Rg, Rg_x, Rg_y, Rg_z])
    
    # Use list of coordinates to create a df for the trajectory
    Rg_df = pd.DataFrame(temp_Rg)
   
    #add column names
    Rg_df.columns = ['Simulation Code', 'Arms', 'Configuration', 'Temperature Condition (°C)', 'Salt Concentration (M)', 'Standard Rg (nm)', 'Rg_X (nm)', 'Rg_Y (nm)', 'Rg_Z (nm)']

    # Rg_df.to_csv(f"{arms}NS_{conformation}_{temp_condition}_{salt_concentration}_test.csv")

    return Rg_df
    
