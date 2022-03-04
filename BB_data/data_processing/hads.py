from functions.data_functions import data
from functions.behavioural_functions import scoring
import pandas as pd

def main():
    
    '''
    Main function for scoring hads. Takes no parameters and returns hads results.
    '''
    
    dropindex = [72, 136, 138, 139, 141, 143, 144, 152, 156, 158, 159, 160, 176, 178, 181]
    df = data('questionnaire_data.csv', 't2', clean=True, drop_index=dropindex)
    hads_df = df.loc[:,'73.':'86.']
    print('\nNumber of null values:', '\n', hads_df.isnull().sum(), '\n')

    null_index = hads_df[hads_df.isnull().any(axis=1)]
    print(null_index)

    score_df = scoring(hads_df)
    hads_final_df = pd.concat([df['7.'].drop(index=[31,39]), score_df], axis=1)

    anxiety = hads_final_df[['73.SCORE', '75.SCORE', '77.SCORE', '79.SCORE', '81.SCORE', '83.SCORE', '85.SCORE']].sum(axis=1) 
    depression = hads_final_df[['74.SCORE', '76.SCORE', '78.SCORE', '80.SCORE', '82.SCORE', '84.SCORE', '86.SCORE']].sum(axis=1)

    hads_results = pd.concat([hads_final_df[['7.','overall_score']], anxiety, depression], axis=1).rename(columns={0:'anxiety', 1:'Depression'})

    return hads_results

if __name__ == '__main__':
    hads = main()