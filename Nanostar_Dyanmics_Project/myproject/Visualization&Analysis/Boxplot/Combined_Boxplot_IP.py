import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set style and context
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)
# sns.set_palette("Set2")

# Combine all DataFrames (same as your code)
dfs = [theta_65C_01M, theta_65C_25M, theta_65C_5M, theta_65C_75M, theta_65C_1M]
columns = ["0.1M", "0.25M", "0.5M", "0.75M", "1.0M"]

all_dfs = []

for i, df in enumerate(dfs):
    temp_df = pd.concat([
        pd.DataFrame({'angle_value': df['θ1'], 'angle_type': 'θ1'}),
        pd.DataFrame({'angle_value': df['θ2'], 'angle_type': 'θ2'}),
        pd.DataFrame({'angle_value': df['θ3'], 'angle_type': 'θ3'}),
        pd.DataFrame({'angle_value': df['θ4'], 'angle_type': 'θ4'}),
    ])
    temp_df['condition'] = columns[i]
    all_dfs.append(temp_df)

final_df = pd.concat(all_dfs, ignore_index=True)
final_df = final_df.dropna(subset=['angle_value'])

final_df['angle_type'] = final_df['angle_type'].replace({
    'θ1': r'$\theta_1$',
    'θ2': r'$\theta_2$',
    'θ3': r'$\theta_3$',
    'θ4': r'$\theta_4$',
})


# Plot
plt.figure(figsize=(10, 6))

sns.boxplot(x = 'condition', y = 'angle_value', hue = 'angle_type', data=final_df)

# Optional: overlay swarmplot for data points
# sns.swarmplot(x='condition', y='angle_value', hue='angle_type', data=final_df, dodge=True, color=".25", size=2)

# Beautify the plot
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['text.usetex'] = False

plt.title("Angle Distributions Across Conditions", fontsize=25, fontname = 'Times New Roman', pad = 20)
plt.xlabel("Condition", fontsize=20, labelpad = 15)
plt.ylabel("Angle Value (°)", fontsize=20, labelpad = 15)
plt.xticks(rotation=15)
plt.legend(title="Angle Type", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()

plt.show()

