import statistics
import numpy as np
from contact_map_helpers import calculate_contact_map

def contact_map(traj_filepaths, top_filepath, data_df, traj_length):

    means = []

    for f in traj_filepaths:
        mean = calculate_contact_map(f, top_filepath)
        means.append(mean)

    m = statistics.mean(means)

    mean_array = np.full(shape=(traj_length,), fill_value=m)

    data_df["Average Contact Map"] = mean_array

    print("INFO: Contact map calculation complete.")

    return data_df