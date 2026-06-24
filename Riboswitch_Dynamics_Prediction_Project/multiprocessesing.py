import pandas as pd
from data_compilation import compile_data
from save_dataframe import save_dataframe_to_csv
from multiprocessing.pool import ThreadPool
from pathlib import Path
import multiprocessing

def process_condition(args):
    arm, conf, salt, temp = args
    trajectory_filepaths = []
    energy_filepaths = []
    parsed_traj_names = []
    aligned_traj_names = []
    parsed_energy_names = []
    
    for i in [1, 2, 3]:
        trajectory_filepaths.append(f"/Volumes/Pradnya_Research_Data/Stewart_Lab_Data/{arm}RNC/{conf}/{temp}C_{salt}M/trajectory_files/trajectory_{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}.dat")
        parsed_traj_names.append(f"{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}_parsed.dat")
        aligned_traj_names.append(f"{arm}RNC_{conf}_{temp}C_{salt}M_parsed_aligned_traj{i}.dat")
        energy_filepaths.append(f"/Volumes/Pradnya_Research_Data/Stewart_Lab_Data/{arm}RNC/{conf}/{temp}C_{salt}M/energy_files/energy_{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}.dat")
        parsed_energy_names.append(f"{arm}RNC_{conf}_{temp}C_{salt}M_sim_{i}.dat")
    
    return compile_data(trajectory_filepaths, parsed_traj_names, aligned_traj_names,
                       energy_filepaths, parsed_energy_names,
                       f"{arm}RNC_{conf}_{temp}C_{salt}M_compiled_data.csv",
                       arm, conf, temp, salt)

if __name__ == '__main__':
    temps = ["5"]      
    salt_concentrations = [ "0.1", "0.5", "1.0"]
    confs = ["ON", "OFF"]
    arms = ["3"]

    conditions = [(arm, conf, f"{salt}", f"{temp}")
                  for arm in arms
                  for conf in confs
                  for salt in salt_concentrations
                  for temp in temps]

    print(f"Running {len(conditions)} conditions on {3} cores")

    with ThreadPool(processes=3) as pool:
        results = pool.map(process_condition, conditions)
    
    print("All conditions completed!")