from functions.data_functions import data
from functions.behavioural_functions import clean_up_columns, imputate, score
import pandas as pd


def hads_scoring(verbose=False):
    '''
    Main function for scoring hads. 

    Returns
    ------- 
    hads_scores: pandas dataframe of hads results
    '''

    df = data('questionnaire_data.csv', 't2')
    
    hads_df = df.loc[:, '73.':'86.']
    hads_df['7.'] = df['7.']

    hads_df = clean_up_columns(hads_df)
    hads_df = imputate(hads_df)

    anxiety = score(hads_df[['7.','73.', '75.', '77.',
                             '79.', '81.', '83.', '85.', 'group']]).rename(columns={'overall_score': 'anxiety'})
    depression = score(hads_df[['7.', '74.', '76.', '78.',
                                '80.', '82.', '84.', '86.', 'group']])

    hads_score = pd.concat([anxiety, depression.drop(['B_Number', 'group'], axis=1)], axis=1).rename(columns={'overall_score': 'depression'})

    hads_score = hads_score[['B_Number', 'anxiety', 'depression', 'group' ]]
    
    return hads_score


if __name__ == '__main__':
    hads = hads_scoring(verbose=True)