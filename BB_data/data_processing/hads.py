from functions.data_functions import data
from functions.behavioural_functions import scoring
import pandas as pd


def main(verbose=False):
    '''
    Main function for scoring hads. 

    Parameters
    ----------
    verbose: boolean, prints out number of null values and null values.

    Returns
    ------- 
    hads_results: pandas dataframe of hads results
    '''

    df = data('questionnaire_data.csv', 't2')
    hads_df = df.loc[:, '73.':'86.']
    null_index = hads_df[hads_df.isnull().any(axis=1)]

    if verbose == True:
        print('\nNumber of null values:', '\n', hads_df.isnull().sum(), '\n')
        print('\nParticipants with null values:\n',
              df['7.'].iloc[null_index.index])

    score_df = scoring(hads_df)
    hads_final_df = pd.concat(
        [df['7.'], score_df], axis=1).dropna()

    anxiety = hads_final_df[['73.SCORE', '75.SCORE', '77.SCORE',
                             '79.SCORE', '81.SCORE', '83.SCORE', '85.SCORE']].sum(axis=1)
    depression = hads_final_df[['74.SCORE', '76.SCORE', '78.SCORE',
                                '80.SCORE', '82.SCORE', '84.SCORE', '86.SCORE']].sum(axis=1)

    hads_results = pd.concat([hads_final_df[['7.', 'overall_score']], anxiety, depression], axis=1).rename(
        columns={0: 'anxiety', 1: 'depression'})
    hc = hads_results[hads_results['7.'].str.contains('B1')]
    an = hads_results[hads_results['7.'].str.contains('B2')]
    hc['group'] = 'HC'
    an['group'] = 'AN'

    hads_results = pd.concat([hc, an])

    return hads_results


if __name__ == '__main__':
    hads = main(verbose=True)
    