"""CODE IN PROGRESS"""


def plot_single_box(dfs, columns):

    """
    Produces a single box plot.

    Args:
        dfs (list[pd.DataFrame]): List of DataFrames containing angle data
        columns (list[str]): List of strings containing different conditions

    Returns:
        return type, none. --> shows the figure.
    """

    all_dfs = []

    for i, df in enumerate(dfs):
        temp_df = pd.concat([
            pd.DataFrame({'angle_value': df['θ1'], 'angle_type': 'θ1'})
        ])
        temp_df['condition'] = columns[i]
        all_dfs.append(temp_df)

    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df = final_df.dropna(subset=['angle_value'])
    
    final_df['angle_type'] = final_df['angle_type'].replace({
        'θ1': r'$\theta_1$',
    })

    # Plot
    plt.figure(figsize=(10, 6))
    
    sns.boxplot(x = 'condition', y = 'angle_value', data=final_df)

    # Beautify the plot
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['text.usetex'] = False
    
    plt.title("Angle Distributions Across Conditions", fontsize=25, fontname = 'Times New Roman', pad = 20)
    plt.xlabel("Condition", fontsize=20, labelpad = 15)
    plt.ylabel("Angle Value (°)", fontsize=20, labelpad = 15)
    plt.xticks(rotation=15)

    plt.tight_layout()

    plt.show()
