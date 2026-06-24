from prep_trajectory import prep_trajectory_data
from Calc_COM import calc_COM_nonuniform_structure
from Radius_of_Gyration import calc_radius_of_gyration
from RMSD import calc_RMSD
from oxDNA_analysis_tools.UTILS.RyeReader import describe
from contact_map import contact_map
from calc_switching_distance import calc_switching_distance
from create_dataframe import create_dataframe
from energy_main import process_energies
from save_dataframe import save_dataframe_to_csv
from pathlib import Path

def compile_data(trajectory_filepaths, parsed_trajectory_filenames, aligned_trajectory_filenames, 
         energy_filepaths, parsed_energy_filenames, averaged_energy_filename, 
         arms, conformation, temp_condition, salt_concentration):

    try:
    # Step 1: Prepare the trajectory data
        trajectory = prep_trajectory_data(trajectory_filepaths, parsed_trajectory_filenames, aligned_trajectory_filenames, arms, conformation, temp_condition, salt_concentration)

        #get length of the trajectory
        traj_length = len(trajectory)
    except TypeError as e:
        print(f"ERROR: TypeError in Step 1 (prep_trajectory_data) for inputs "
              f"'{trajectory_filepaths}': {e}. Cannot continue without trajectory data.")
        return None
    
    try:
        # Step 2: Calculate the center of mass
        COM_df = calc_COM_nonuniform_structure(trajectory, arms)
    except TypeError as e:
        print(f"ERROR: TypeError in Step 2 (calc_COM) for trajectory '{trajectory_filepaths}': {e}. "
              f"Skipping COM calculation — Radius of Gyration will also be unavailable.")
        COM_df = None

    try:
        # Step 3: Create a dataframe to store the data
        data_df = create_dataframe(arms, conformation, temp_condition, salt_concentration, traj_length)
    
    except TypeError as e:
        print(f"ERROR: TypeError in Step 3 (create_dataframe): {e}. Cannot continue without a DataFrame.")
        return None
    
    try:
        dist_trajectory_filepaths = []
        processed_trajectories_folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/compiled_data_files/parsed_aligned_trajectory_files")
        for f in aligned_trajectory_filenames:
            f = processed_trajectories_folder / f
            dist_trajectory_filepaths.append(str(f))

        # Step 4: Calculated the distance to the switching point and add to dataframe
        data_df = calc_switching_distance(dist_trajectory_filepaths, data_df)

    except TypeError as e:
        print(f"ERROR: TypeError in Step 4 (calc_switching_distance) for files "
              f"'{dist_trajectory_filepaths}': {e}. Skipping switching distance calculation.")
        
    try:
        # Step 5: Prepare energy data and add to dataframe
        data_df = process_energies(energy_filepaths, parsed_energy_filenames, averaged_energy_filename, 
                                data_df, arms, conformation, temp_condition, 
                               salt_concentration)
    except TypeError as e:
        print(f"ERROR: TypeError in Step 5 (process_energies) for files '{energy_filepaths}': {e}. "
              f"Skipping energy data processing.")
    
    try:
        # Step 6: Calculate the average contact map value and add to dataframe
        data_df = contact_map(trajectory_filepaths, 
                          f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arms}RNC/{conformation}/{temp_condition}C_{salt_concentration}M/{arms}NS_RNC_{conformation}_{temp_condition}C_{salt_concentration}M_relaxed_3.top", 
                          data_df,
                          traj_length)
    except TypeError as e:
        print(f"ERROR: TypeError in Step 6 (contact_map) for files '{trajectory_filepaths}': {e}. "
              f"Skipping contact map calculation.")
        
    if COM_df is not None:
        try:
            # Step 7: Calculate the radius of gyration and add to dataframe
            data_df = calc_radius_of_gyration(trajectory, COM_df, data_df)
        except TypeError as e:
            print(f"ERROR: TypeError in Step 7 (calc_radius_of_gyration): {e}. "
                  f"Skipping radius of gyration calculation.")
            
    else:
        print("WARNING: Skipping Step 7 (calc_radius_of_gyration) because COM_df is unavailable.")

    try:
    
        save_dataframe_to_csv(data_df, f"compiled_data_{arms}RNC_{conformation}_{temp_condition}C_{salt_concentration}M.csv", 
                          arms, conformation, temp_condition, salt_concentration) # Save the dataframe before adding energy data so that we have a record of the trajectory-based data before adding energy data (in case there are any issues with the energy data processing)
    except TypeError as e:
        print(f"ERROR: TypeError saving DataFrame after Step 7: {e}.")
    
    
    try:
        # Step 8: Calculate the RMSD and add to dataframe
        data_df = calc_RMSD(trajectory, data_df)
        
    except TypeError as e:
        print(f"ERROR: TypeError in Step 8 (calc_RMSD): {e}. Skipping RMSD calculation.")
    
    # Final save
    try:
        save_dataframe_to_csv(data_df, f"compiled_data_{arms}RNC_{conformation}_{temp_condition}C_{salt_concentration}M.csv",
                              arms, conformation, temp_condition, salt_concentration)
    except TypeError as e:
        print(f"ERROR: TypeError during final save: {e}.")

    print("INFO: Data compilation complete. 🎉")
    return data_df
    

  