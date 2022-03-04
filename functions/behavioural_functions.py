def calculating_bmi(weight:float, height:float, cm=True):

    '''
    Function to calculate body mass index.

    Parameters
    ----------
    height : float. Height either in cm or meters
    weight: float. Weight in kilograms

    Returns
    -------
    BMI: float. Body mass index.
    '''
    if cm == True:
        height = height / 100
    
    bmi = weight/(height **2)
    return bmi