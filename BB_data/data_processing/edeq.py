from functions.data_functions import data
from functions.behavioural_functions import edeq, score, imputate
import pandas as pd
import warnings
# To ignore all pandas .loc slicing suggestions
warnings.filterwarnings(action='ignore')


def edeq_scoring() -> pd.DataFrame:
   
    '''
    Main function for EDEQ scoring

    Parameters
    ----------
    None

    Returns
    -------
    edeq_scores: pd.DataFrame: Scores for ede-q. 
    
    '''

    df = data('questionnaire_data.csv', 't2')

    edeq_df = df[['7.', '25.', '26.', '27.', '28.', '29.', '30.', '31.', '33.', '34.', '35.', '36.',
                  '37.', '38.', '39.', '47.', '48.', '49.', '50.', '51.', '52.', '53.', '54.']]
    
    edeq_df = edeq(edeq_df)
    edeq_df = imputate(edeq_df).rename(columns={'B_Number' : '7.'})

    restraint = edeq_df[['7.','group', '25.', '26.', '27.', '28.', '29.']]
    eating_concern = edeq_df[['7.','group', '30.', '31.', '33.', '52.', '39.']]
    shape_concern = edeq_df[['7.','group','34.', '35.', '48.',
                         '36.', '51.', '53.', '54.', '37.']]
    weight_concern = edeq_df[['7.','group','47.', '49.', '35.', '50.', '38.']]
    
    restraint_score = score(restraint)
    restraint_score['restraint'] = restraint_score['overall_score'] / 5
    
    eating_concern_score = score(eating_concern)
    eating_concern_score['eating_concern'] = eating_concern_score['overall_score'] / 5

    shape_concern_score = score(shape_concern)
    shape_concern_score['shape_concern'] = shape_concern_score['overall_score'] / 8
    
    weight_concern_score = score(weight_concern)
    weight_concern_score['weight_concern'] = weight_concern_score['overall_score'] / 5
    

    edeq_scores = pd.concat([restraint_score[['B_Number','restraint']], eating_concern_score['eating_concern'],
                             shape_concern_score['shape_concern'], weight_concern_score['weight_concern']], axis=1)

    edeq_scores['global_score'] = edeq_scores.drop('B_Number', axis=1).sum(axis=1)/4
    edeq_scores['group'] = weight_concern_score['group']

    return edeq_scores


if __name__ == '__main__':
    edeq_score = edeq_scoring()
    print(edeq_score)
    
