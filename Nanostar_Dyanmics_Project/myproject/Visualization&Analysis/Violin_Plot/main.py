def plot_violin(dataset, condition, filename):

    """
    Produces violin plot with given dataset for specified condition.

    Args:
    
        dataset (pd.Dataframe): typically would be a dataframe of ALL temperature and salt data 
        condition (str): Either 'Temperature' OR 'Salt', specifies the condition the violin plot will subset
        filename (str): name that the user intends to call the file

    Returns:
        return type, none. --> A saved violin plot figure.
    """


    #Define figure size & generate plot
    plt.figure(figsize=(10, 10))
    sns.violinplot(x = condition, y = 'Angle', data= dataset, split = False, inner = "box", width = 0.5,  palette = "Blues")
    sns.set(font_scale= 1.5)
    
    # Beautify the plot
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['text.usetex'] = False
    
    # condition: Temperature (°C) OR Monovalent Salt Concentration (M)
    #chooses correct label
    unit = ""
    if condition == 'Temperature':
        unit = "(°C)"
    elif condition == 'Salt':
        unit = "(M)"
    else:
        raise ValueError("Incorrect condition provided. Please choose either 'Temperature' OR 'Salt'.")
        
    
    #Figure labels
    plt.xlabel(f"{condition}{unit}", fontsize=20, labelpad = 15)
    plt.ylabel("Angle (degrees)", fontsize=20, labelpad = 15)
    plt.xticks(rotation=15)

    #bound data on y-axis
    plt.ylim(0)
    

    #Save figure as svg and png
    plt.tight_layout()
    # plt.show()
    
    plt.savefig(f"Violin_{filename}.svg", dpi=300)
    plt.savefig("Violin_{filename}.png", dpi=200)
    plt.close()
