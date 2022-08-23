from functions.data_functions import data
import pandas as pd
import warnings
# To ignore all pandas .loc slicing suggestions
warnings.filterwarnings(action='ignore')


def main(verbose=False):
    '''
    Main function for AQ10 scoring

    Parameters
    ----------
    verbose:Boolean: Print out null value index.

    Returns
    -------
    aq_final_df:pandas datframe: Scores for AQ10. 
    '''
    df = data('questionnaire_data.csv', 't2', simplify=True)
    aq_df = df.loc[:, '87.':'96.']
    aq_df['7.'] = df['7.']

    if verbose == True:
        null = aq_df[aq_df.isnull().any(axis=1)]
        print(aq_df.isnull().sum())
        print(null)

    aq_df = aq_df.dropna()

    disagree = {
        'definitely disagree': 1,
        'slightly disagree': 1,
        'slightly agree': 0,
        'definitely agree': 0
    }

    agree = {
        'definitely disagree': 0,
        'slightly disagree': 0,
        'slightly agree': 1,
        'definitely agree': 1
    }

    agree_df = aq_df[['87.', '93.', '94.', '96.']]
    disagree_df = aq_df[['88.', '89.', '90.', '91.', '92.', '95.']]

    for column in agree_df.columns:
        agree_df[column +
                 'SCORE'] = agree_df[column].apply(lambda value: agree[value])

    for column in disagree_df.columns:
        disagree_df[column +
                    'SCORE'] = disagree_df[column].apply(lambda value: disagree[value])

    aq_score = pd.concat([agree_df, disagree_df], axis=1)

    aq_score = aq_score.filter(regex=r'SCORE')
    aq_score['overall_score'] = aq_score.sum(axis=1)

    aq_group = pd.concat([aq_df['7.'], aq_score['overall_score']], axis=1)
    hc = aq_group[aq_group['7.'].str.contains('B1')]
    an = aq_group[aq_group['7.'].str.contains('B2')]
    hc['group'] = 'HC'
    an['group'] = 'AN'
    aq_final_df = pd.concat([hc, an])

    return aq_final_df


if __name__ == '__main__':
    aq10 = main(verbose=True)
    print(aq10.shape)
