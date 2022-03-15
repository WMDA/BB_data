import re
import warnings
import math

warnings.filterwarnings(action='ignore')# To ignore all pandas .loc slicing suggestions

def behavioural_score(response:str):
    
    '''
    Function to score questionnaire response.

    Parameter
    ---------
    response:str: Response from questionnaire.

    Returns
    -------
    score:int: Score value from the questionnaire data.
    '''
    
    score = re.sub(r'\D', '', response)
    return int(score)


def calculating_bmi(weight:float, height:float, cm=True):

    '''
    Function to calculate body mass index.

    Parameters
    ----------
    height:float: Height either in cm or meters
    weight:float: Weight in kilograms

    Returns
    -------
    BMI:float: Body mass index.
    '''
    
    if cm == True:
        height = height / 100
    
    bmi = weight/(height **2)
    return bmi

def edeq_scoring_dict(response:str):

    '''
    Function to score ede-q responses where no int value is provided.

    Parameters
    ----------
    response:str: response from edeq.

    Returns
    -------
    final_score:int: score for response from edeq.
    '''
   
    scoring_sheet = {
            'Every':6,
            '23-27':5,
            'Most':5,
            '16-22':4,
            'More':4,
            '13-15':3,
            'Half':3,
            '6-12':2,
            'Less':2,
            '1-5':1,
            'A':1,
            'No':0,
            'None':0
        }
        
    stripped_respose = response[0:5]

    if stripped_respose != 'Every':
        score = re.findall(r'^[^\s]+', stripped_respose)
    else:
        score = [stripped_respose]
    final_score = scoring_sheet[score[0]]
    return int(final_score)

def edeq_score(response:str):

    '''
    Function wrapper around behavioural_score and edeq_scoring_dict functions
    dependeing on response.

    Parameters
    ----------
    Response:str: Response from the edeq

    Returns
    -------
    score:int: score for response from edeq
    '''
   
    if 'day' not in response:
        
        if 'time' not in response:
            score = behavioural_score(response)
            
        else:
            score = edeq_scoring_dict(response)

    else:
         score = edeq_scoring_dict(response)
    
    return int(score)

def scoring(df:object, edeq=False):

    '''
    Function to score behavioural questions and calculates total score.

    Parameters
    ----------
    df:pandas df str: responses to questionnaires.

    Returns
    -------
    score_df:pandas df int: values and an overall score.
    '''
    
    df = df.dropna()
    
    for column in df.columns:
        
        if edeq==True:
            df[column + 'SCORE'] = df[column].apply(lambda response: edeq_score(response))
        
        else:
            df[column + 'SCORE'] = df[column].apply(lambda response: behavioural_score(response))

    score_df = df.filter(regex=r'SCORE')
    score_df['overall_score'] = score_df.sum(axis=1)
    return score_df


def cohen_d(group1,group2):
    
    '''
    Calculate cohens d.
    
    Parameters: 
    ------------
    group1: array or pandas series to test for effect size.
    group2: array or pandas series to test for effect size.


    Returns
    -----------
    Output: int cohen's d value.
    
    '''
    
    
    diff = group1.mean() - group2.mean()
    pooledstdev = math.sqrt((group1.std()**2 + group2.std())/2)
    cohend = diff / pooledstdev
    return cohend