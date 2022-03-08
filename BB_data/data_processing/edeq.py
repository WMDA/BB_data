from functions.data_functions import data
from functions.behavioural_functions import scoring
import pandas as pd
import sys
import warnings
warnings.filterwarnings(action='ignore')# To ignore all pandas .loc slicing suggestions


def main(verbose=False):
    
    '''
    Main function for EDEQ scoring

    Parameters
    ----------
    verbose:Boolean: Print out null value index.

    Returns
    -------
    edeq_final_df:pandas datframe: Scores for ede-q. 
    '''

    dropindex = [72, 136, 138, 139, 141, 143, 144, 152, 156, 158, 159, 160, 176, 178, 181]
    df = data('questionnaire_data.csv','t2', clean=True, drop_index=dropindex)

    edeq_df = df[['7.','25.', '26.', '27.', '28.', '29.', '30.', '31.', '33.', '34.', '35.', '36.',
               '37.', '38.', '39.', '47.', '48.', '49.', '50.', '51.', '52.', '53.', '54.']]


    if verbose == True:
        null = edeq_df[edeq_df.isnull().any(axis=1)]
        print(edeq_df.isnull().sum())
        print(null)

    edeq_df = edeq_df.dropna()
    restraint = edeq_df[['25.', '26.', '27.', '28.', '29.']]
    eating_concern = edeq_df[['30.', '31.', '33.', '52.', '39.']]
    shape_concern = edeq_df[['34.','35.', '48.', '36.', '51.', '53.', '54.', '37.']]
    weight_concern = edeq_df[['47.', '49.', '35.', '50.', '38.']]

    restraint_score = scoring(restraint, edeq=True)
    eating_concern_score = scoring(eating_concern, edeq=True)
    shape_concern_score = scoring(shape_concern, edeq=True)
    weight_concern_score = scoring(weight_concern, edeq=True)

    restraint_score['restraint_score'] = restraint_score['overall_score']/5
    eating_concern_score['eating_concern_score'] = eating_concern_score['overall_score']/5
    shape_concern_score['shape_concern_score'] = shape_concern_score['overall_score']/8
    weight_concern_score['weight_concern_score'] = weight_concern_score['overall_score']/5

    edeq_scores = pd.concat([restraint_score['restraint_score'], eating_concern_score['eating_concern_score'], 
                         shape_concern_score['shape_concern_score'], weight_concern_score['weight_concern_score']], axis=1)

    edeq_scores['global_score'] = edeq_scores.sum(axis=1)/4

    edeq_group_df = pd.concat([edeq_df['7.'], edeq_scores], axis=1)
    hc = edeq_group_df[edeq_group_df['7.'].str.contains('B1')]
    an = edeq_group_df[edeq_group_df['7.'].str.contains('B2')]
    hc['group'] = 'HC'
    an['group'] = 'AN'


    edeq_final_df = pd.concat([hc, an])
    return edeq_final_df


if __name__ == '__main__':
    edeq_score = main(verbose=True) 
        
