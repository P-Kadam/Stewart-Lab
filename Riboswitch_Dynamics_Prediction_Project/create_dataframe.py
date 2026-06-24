import pandas as pd

def create_dataframe(arms, conformation, temp_condition, salt_concentration, traj_length):
    """
    Creates a pandas DataFrame to store compiled simulation data.

    Args:
        arms (str): The arms of the riboswitch.
        conformation (str): The conformation of the riboswitch.
        temp_condition (int): The temperature condition.
        salt_concentration (float): The salt concentration.
        traj_length (int): The length of the trajectory.

    Returns:
        pd.DataFrame: The created DataFrame.
    """

    data_df = pd.DataFrame({
        "Simulation Code": [f"{arms}NS_{conformation}_{temp_condition}_{salt_concentration}"] * traj_length,
        "Arms": [arms] * traj_length,
        "Configuration": [conformation] * traj_length,
        "Temperature Condition (°C)": [temp_condition] * traj_length,
        "Salt Concentration (M)": [salt_concentration] * traj_length
    })

    print("INFO: Dataframe has been created with the simulation parameters.")

    return data_df