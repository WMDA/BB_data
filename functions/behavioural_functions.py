import re
import warnings
warnings.filterwarnings(action='ignore')# To ignore all pandas .loc slicing suggestions

def behavioural_score(response:str):
    
    '''
    Function to score questionnaire response.

    Parameter
    ---------
    response: str. Response from questionnaire.

    Returns
    -------
    score: int. Score value from the questionnaire data.
    '''
    
    score = re.sub(r'\D', '', response)
    return int(score)


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

def scoring(df):

    '''
    Function to score behavioural questions and calculates total score.

    Parameters
    ----------
    df: pandas df of str responses to questionnaires.

    Returns
    -------
    score_df: pandas df of int values and an overall score.
    '''
    
    df = df.dropna()
    
    for column in df.columns:
        df[column + 'SCORE'] = df[column].apply(lambda response: behavioural_score(response))

    score_df = df.filter(regex=r'SCORE')
    score_df['overall_score'] = score_df.sum(axis=1)
    return score_df