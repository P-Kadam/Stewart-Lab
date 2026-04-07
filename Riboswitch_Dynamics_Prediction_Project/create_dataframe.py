import pandas as pd

def create_dataframe(arms, conformation, temp_condition, salt_concentration):
    """
    
    """

    data_df = pd.DataFrame({
        "Simulation Code": [f"{arms}NS_{conformation}_{temp_condition}_{salt_concentration}"] * 9000,
        "Arms": [arms] * 9000,
        "Configuration": [conformation] * 9000,
        "Temperature Condition (°C)": [temp_condition] * 9000,
        "Salt Concentration (M)": [salt_concentration] * 9000
    })

    return data_df