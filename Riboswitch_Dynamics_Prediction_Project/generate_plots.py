import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##### CREATING FIGURES ####

dataset = pd.read_csv("/Volumes/Pradnya_Research_Data/Stewart_Lab_Data/combined_data/combined_data.csv")
print(dataset.head())

#plotting the RMSD for each condition group

print(dataset.columns)

# RMSD_df = pd.DataFrame({'Configuration': dataset["Configuration"],
#                         'Temperature Condition (°C)': dataset["Temperature Condition (°C)"],
#                         'Salt Concentration (M)': dataset["Salt Concentration (M)"],
#                         'RMSD (Å)': dataset["RMSD (Å)"]})


# ON_37C_05M = RMSD_df[(RMSD_df["Configuration"] == "ON") & (RMSD_df["Temperature Condition (°C)"] ==37) & (RMSD_df["Salt Concentration (M)"] == 0.5)]
# OFF_37C_05M = RMSD_df[(RMSD_df["Configuration"] == "OFF") & (RMSD_df["Temperature Condition (°C)"] == 37) & (RMSD_df["Salt Concentration (M)"] == 0.5)]

# mean_ON = ON_37C_05M["RMSD (Å)"].mean()
# mean_OFF = OFF_37C_05M["RMSD (Å)"].mean()

# mean_array_ON = np.repeat(np.array([mean_ON]), len(ON_37C_05M), axis=0)
# mean_array_OFF = np.repeat(np.array([mean_OFF]), len(OFF_37C_05M), axis=0)

# plt.rcParams['svg.fonttype'] = 'none'

# plt.figure(figsize=(10, 6))
# plt.plot(ON_37C_05M["RMSD (Å)"].values, label="ON", alpha = 0.4)
# plt.plot(OFF_37C_05M["RMSD (Å)"].values, label="OFF",  alpha = 0.4)
# plt.plot(mean_array_ON, label=f"$σ_{{ON}}$ = {mean_ON:.2f}", linestyle='--', color = "blue")
# plt.plot(mean_array_OFF, label=f"$σ_{{OFF}}$ = {mean_OFF:.2f}", linestyle='--', color = "orange")
# plt.xlabel("Frame Index")
# plt.ylabel("RMSD (Å)")
# plt.title("RMSD 37°C 0.5M")
# plt.legend()
# plt.grid()
# plt.savefig("37C_0.5M_RMSD_plot.svg")
# plt.savefig("37C_0.5M_RMSD_plot.png")


Rg_df = pd.DataFrame({'Configuration': dataset["Configuration"],
                        'Temperature Condition (°C)': dataset["Temperature Condition (°C)"],
                        'Salt Concentration (M)': dataset["Salt Concentration (M)"],
                        'Standard Rg (nm)': dataset["Standard Rg (nm)"]})


ON_5C_05M = Rg_df[(Rg_df["Configuration"] == "ON") & (Rg_df["Temperature Condition (°C)"] ==5) & (Rg_df["Salt Concentration (M)"] == 0.5)]
OFF_5C_05M = Rg_df[(Rg_df["Configuration"] == "OFF") & (Rg_df["Temperature Condition (°C)"] == 5) & (Rg_df["Salt Concentration (M)"] == 0.5)]

mean_ON = ON_5C_05M["Standard Rg (nm)"].mean()
mean_OFF = OFF_5C_05M["Standard Rg (nm)"].mean()

mean_array_ON = np.repeat(np.array([mean_ON]), len(ON_5C_05M), axis=0)
mean_array_OFF = np.repeat(np.array([mean_OFF]), len(OFF_5C_05M), axis=0)

plt.rcParams['svg.fonttype'] = 'none'

plt.figure(figsize=(10, 6))
plt.plot(ON_5C_05M["Standard Rg (nm)"].values, label="ON", alpha = 0.4)
plt.plot(OFF_5C_05M["Standard Rg (nm)"].values, label="OFF",  alpha = 0.4)
plt.plot(mean_array_ON, label=f"$σ_{{ON}}$ = {mean_ON:.2f}", linestyle='--', color = "blue")
plt.plot(mean_array_OFF, label=f"$σ_{{OFF}}$ = {mean_OFF:.2f}", linestyle='--', color = "orange")
plt.xlabel("Frame Index")
plt.ylabel("Standard Rg (nm)")
plt.title("Rg 5°C 0.5M")
plt.legend()
plt.grid()
plt.savefig("5C_0.5M_Rg_plot.svg")
plt.savefig("5C_0.5M_Rg_plot.png")