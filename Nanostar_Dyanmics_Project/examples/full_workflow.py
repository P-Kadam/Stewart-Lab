from myproject import prep_trajectory_data, calc_angles, merge_data, plot_interpolated_histogram, plot_violin

# Step 1: Read in trajectory data from configuration files
# Note: You may average as many trajectories as you want

### ADD FILEPATHS
averaged_traj = prep_trajectory_data(["/Volumes/Stewart_Lab_External_Drive_PK/3_Arm/20C_0.1M/trajectory_files/trajectory_20C_0.1M_sim_revised_1.dat","/Volumes/Stewart_Lab_External_Drive_PK/3_Arm/20C_0.1M/trajectory_files/trajectory_20C_0.1M_sim_revised_2.dat", "/Volumes/Stewart_Lab_External_Drive_PK/3_Arm/20C_0.1M/trajectory_files/trajectory_20C_0.1M_sim_revised_3.dat"])

print(averaged_traj)

# Step 2: Calculate angles between the nanostar arms
#angles = calc_angles(averaged_traj, "/Volumes/Stewart_Lab_External_Drive_PK/3_Arm_INPUT_FILES/3m1_6NT1_2bp.top", 6, 3, 1, 2)


# Step 3: Produce visual - interpolated histogram
#plot_interpolated_histogram(angles, 1, [0.15])

