import pandas as pd
from data_compilation import compile_data
from save_dataframe import save_dataframe_to_csv
from pathlib import Path


if __name__ == '__main__':

    temps = ["5"]   
    salt_concentrations = ["1.0"]
    confs = [ "ON" ]
    arms = ["3"]

    for arm in arms:
        for conf in confs:
            for salt in salt_concentrations:
                for temp in temps:
                #    combo = []

                   trajectory_filepaths = []
                   energy_filepaths = []
                   parsed_traj_names = []
                   aligned_traj_names = []
                   parsed_energy_names = []
                   
                   for i in [1, 2, 3]:

                    #Preparing files for generating the data table
                    trajectory_filepaths.append(f"/Volumes/Seagate Backup Plus Drive/Pradnya_Research/Riboswitch_Manuscript/{arm}RNC/{conf}/{temp}C_{salt}M/trajectory_files/trajectory_{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}.dat")
                    parsed_traj_names.append(f"{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}_parsed.dat")
                    aligned_traj_names.append(f"{arm}RNC_{conf}_{temp}C_{salt}M_parsed_aligned_traj{i}.dat")
                    energy_filepaths.append(f"/Volumes/Seagate Backup Plus Drive/Pradnya_Research/Riboswitch_Manuscript/Volumes/Pradnya_Research_Data/{arm}RNC/{conf}/{temp}C_{salt}M/energy_files/energy_{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}.dat")
                    parsed_energy_names.append(f"{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}_parsed.dat")

                    # combo.append((arm, conf, temp, salt, i))
  
                # print(combo)
                data = compile_data(trajectory_filepaths, parsed_traj_names, aligned_traj_names,
                                    energy_filepaths, parsed_energy_names, f"{arm}RNC_{conf}_{temp}C_{salt}M_compiled_data.csv",
                                        arm, conf, temp, salt) 
                   
        # save_dataframe_to_csv(data, f"compiled_data.csv")