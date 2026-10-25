# Plot the contact map with the averaged trajectory data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics
from sys import stderr
from oxDNA_analysis_tools.contact_map import contact_map
from oxDNA_analysis_tools.UTILS.RyeReader import describe

# guard the executable body so multiprocessing "spawn" (used by contact_map)
# does not re-run the whole script when it re-imports this module in child processes
if __name__ == '__main__':

    temp = ["5", "37", "65"]
    salt = ["1.0"]
    config = ["OFF", "ON"]
    arms = ["5"]

    plot_cm = []
    labels = []   # record each panel's label in the same order as plot_cm
    meta = []     # (conf, t) for each panel, used to place it in the grid

    for t in temp:
        for conf in config:
            for arm in arms:
                for s in salt:

                    cm_values = []

                    for sim_num in [1, 2, 3]:

                        print(f"ℹ️ Processing {arm}RNC_{conf}_{t}C_{s}M simulation {sim_num}")

                        top_filepath = f"/Volumes/Seagate_Backup_Plus_Drive/Pradnya_Research/Riboswitch_Manuscript/{arm}RNC/{conf}/{t}C_{s}M/{arm}NS_RNC_{conf}_{t}C_{s}M_relaxed_3.top"
                        traj_filepath = f"/Volumes/Seagate_Backup_Plus_Drive/Pradnya_Research/Riboswitch_Manuscript/{arm}RNC/{conf}/{t}C_{s}M/compiled_data_files/parsed_aligned_trajectory_files/{arm}RNC_{conf}_{t}C_{s}M_parsed_aligned_traj{sim_num}.dat"
                        graph_name = f"{arm}RNC_{conf}_{t}C_{s}M_contact_map"

                        top_info, traj_info = describe(top_filepath, traj_filepath)

                        cm = contact_map(traj_info, top_info)
                        print("\n")

                        # gets the upper triangle of the contact matrix - since it is symmetric
                        indecies = np.triu_indices_from(cm, k=0)
                        vals = cm[indecies] #extract correpsonding values

                        #append the values to a list to store for later
                        cm_values.append(vals)

                    avg_vals = np.mean(cm_values, axis=0) #average the upper-triangle values across the simulations

                    mean_check = statistics.mean(avg_vals)
                    print(f"Mean of the averaged contact map values: {mean_check}")

                    #scatter the averaged values back into an n x n matrix to rebuild the contact map
                    n = cm.shape[0]
                    avg_cm = np.zeros((n, n))
                    avg_cm[np.triu_indices(n, k=0)] = avg_vals

                    #mirror the upper triangle into the lower triangle for a full symmetric heatmap
                    #(subtract the diagonal so k=0 cells are not counted twice)
                    avg_cm = avg_cm + avg_cm.T - np.diag(np.diag(avg_cm))
                    plot_cm.append(avg_cm)
                    labels.append(f"{arm}RNC_{conf}_{t}C_{s}M")   # matches plot_cm order
                    meta.append((conf, t))


    #plot the contact maps
    print("ℹ️ INFO: plotting figure")

    # set styling before creating the figure so it applies to the new axes
    plt.rcParams.update({
        'axes.labelsize': 16,     # X and Y axis labels
        'xtick.labelsize': 14,    # X axis tick labels
        'ytick.labelsize': 14,    # Y axis tick labels
        'axes.titlesize': 20,     # Plot title
        'legend.fontsize': 12     # Legend text
    })

    fig, ax = plt.subplots(2, 3, figsize=(15, 10), constrained_layout=True)

    # shared color scale across all panels so a given color means the same value everywhere
    vmin = min(m.min() for m in plot_cm)
    vmax = max(m.max() for m in plot_cm)

    for i in range(len(plot_cm)):
        conf, t = meta[i]
        row = config.index(conf)   # top row = OFF, bottom row = ON (order of `config`)
        col = temp.index(t)        # columns follow the order of `temp` (increasing)
        im = ax[row, col].imshow(plot_cm[i], cmap='viridis', origin='lower', vmin=vmin, vmax=vmax)
        ax[row, col].set_title(labels[i])   # label recorded alongside the data
        ax[row, col].set_xlabel("Nucleotide Index")
        ax[row, col].set_ylabel("Nucleotide Index")

    fig.colorbar(im, ax=ax.ravel().tolist(), shrink=0.6)

    grid_name = f"{arms[0]}RNC_{salt[0]}M_contact_map_grid"
    plt.savefig(f"{grid_name}.png")
    plt.savefig(f"{grid_name}.svg")
