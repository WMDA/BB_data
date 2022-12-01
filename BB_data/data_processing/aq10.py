from functions.data_functions import data
from functions.behavioural_functions import aq10_dict, imputate, score
import pandas as pd
import warnings
# To ignore all pandas .loc slicing suggestions
warnings.filterwarnings(action='ignore')


def aq10_scoring() -> pd.DataFrame:

    '''
    Main function for AQ10 scoring

    Parameters
    ----------
    None

    Returns
    -------
    aq_score: pd.DataFrame Scores for AQ10. 
    '''
    
    df = data('questionnaire_data.csv', 't2', simplify=True)
    scores = aq10_dict()
    
    aq_df = df.loc[:, '87.':'96.']
    aq_df['7.'] = df['7.']
    
    agree_df = aq_df[['7.','87.', '93.', '94.', '96.']]
    disagree_df = aq_df[['7.','88.', '89.', '90.', '91.', '92.', '95.']]
    
    for column in agree_df.columns:
        if column != '7.':
            agree_df[column] = agree_df[column].apply(lambda value: scores['agree'][value] if type(value) == str else value )
    
    for column in disagree_df.columns:
        if column != '7.':
            disagree_df[column] = disagree_df[column].apply(lambda value: scores['disagree'][value] if type(value) == str else value)
    
    aq_score = pd.concat([agree_df, disagree_df.drop('7.', axis=1)], axis=1)
    
    aq_score = imputate(aq_score)
    aq_score = score(aq_score)
    
    return aq_score[['B_Number', 'overall_score', 'group']]


if __name__ == '__main__':
    aq10 = aq10_scoring()

