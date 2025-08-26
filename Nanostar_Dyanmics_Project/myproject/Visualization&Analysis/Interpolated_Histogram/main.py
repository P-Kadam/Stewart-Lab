import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import statistics
from scipy.interpolate import interp1d

# Seaborn style
sns.set(style="whitegrid")


def plot_interpolated_histogram(dfs, theta_value, condition_list, filename, armNums):
    """
    Produces an interpolated histogram plot for selected data points and prints statistics.

    Args:
        dfs (list[pd.DataFrame]): List of DataFrames containing angle data
        theta_value (int): the angle (between which arms) to plot
        condition_list (list): Conditions corresponding to each df in dfs
        filename (str): Filename to save the graph under

    Returns:
        A saved interpolated histogram figure
    """

    # Plotting setup
    plt.figure(figsize=(8, 5))
    # plt.rcParams['font.family'] = ['serif', 'Times New Roman']

    # creating lists to hold all statistical data
    mean = []
    stdev = []
    min_val = []
    max_val = []

    #keeps track of the index, and extracts the exact dataframe
    for i, df in enumerate(dfs):
        
        # Extract relevant angle column
        angle_col = _select_theta(theta_value)
        angles = df[[angle_col]]

        # Calculate statistics

        #gets rid of any NaN columns - extracts rest of the data
        data = angles[angle_col].dropna()

        #stats: mean, standard devication, min, max
        mean.append(data.mean())
        stdev.append(data.std())
        min_val.append(round(data.min(), 4))
        max_val.append(round(data.max(), 4))

        # Create histogram with forced range

        #Dividing the data into 6 equally spaced bins --> bins divided between the range of 1 and 180
        #bins: [0, 30, 60, 90, 120, 150, 180]
       
        #hist_counts: counts how many data points fall within a specified bin
        #ex. if data was [15, 25, 40, 60, 70, 85, 95, 110, 150, 170], hist counts = [2, 1, 3, 2, 0, 2]
        hist_counts, bin_edges = np.histogram(data, bins=8, range=(0, 180))


        #finds the midpoint of each bin
        #will take each end of the bin and then finds the mindpoint
        #ex. for the bin: (0, 30] --> bin_center = 0+30/2 = 15
        #for an interpolated histogram, this shows you the data
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

        #
        hist_frequencies = hist_counts / len(data)  # Normalize

        # Interpolation
        interpolator = interp1d(
            bin_centers, hist_frequencies, kind='quadratic', fill_value="extrapolate"
        )

        # will plot 30 points on each interpolated line
        x_dense = np.linspace(0, 180, 30)
        y_dense = np.clip(interpolator(x_dense), 0, None)  # Clamp negatives

        # Plot style selector
        marker_styles = ['s-', 'D-', 'o-', '*-', 'x-', 'p-']
        plotstyle = marker_styles[i % len(marker_styles)]

        # Plot
        # °C
        plt.plot(
            x_dense, y_dense,plotstyle, markerfacecolor='none', zorder=4, label=f"{condition_list[i]} °C")

    plt.rcParams["font.family"] = "Times New Roman"
    # Axis labels and legend
    label = _legend_label(theta_value, armNums)
    plt.xlabel(label)
    plt.ylabel(f"P({label})")
    plt.legend(loc="upper left", frameon = True)
    plt.grid(True)
    plt.xlim(0, 180)

    # Print statistics
    for i in range(len(mean)):
        print(f"i: {i}\nmean: {mean[i]:.4f}\nstdev: {stdev[i]:.4f}\nmin: {min_val[i]}\nmax: {max_val[i]}")
        print("_________________")

    # Save figure as an svg and png
    plt.tight_layout()
  
    plt.savefig(f"interpolated_Hist_{filename}.svg", dpi=300)
    plt.savefig(f"interpolated_Hist_{filename}.png", dpi=200)
    plt.close()
