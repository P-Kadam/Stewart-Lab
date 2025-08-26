#################################
# HELPER FUNCTION 1
################################

def _select_theta(theta):

    """
        Matches the inputted theta value to the corresponding bond angle.

    Args:
        theta (int): integer from 1 to 5 that corresponds to the specific bond angle within the nanostar conformation

    Returns:
        (string): the theta number
    """

    
    match theta:

        case 1:
            return "θ1"
        case 2:
            return "θ2"
        case 3:
            return "θ3"
        case 4:
            return "θ4"
        case 5:
            return "θ5"
        

#################################
# HELPER FUNCTION 1
################################

def _legend_label(theta, armNums):

    """
        Matches the inputted theta value to the corresponding legend label for the graphs produced.

    Args:
        theta (int): integer from 1 to 5 that corresponds to the specific bond angle within the nanostar conformation
        
        armNums (int): integer from 3 to 5 that corresponds to the nanostar valency

    Returns:
        (string): unicode letters for correct sub & superscripts
    """

    match theta:

        case 1:
            return r'$\theta_{12}$'
        case 2:
            return r'$\theta_{23}$'
        case 3:
            if armNums == 3:
                return r'$\theta_{13}$'
            return r'$\theta_{34}$'
        case 4:
            if armNums == 4:
                return r'$\theta_{14}$'
            return r'$\theta_{45}$'
        case 5:
            return r'$\theta_{15}$'
