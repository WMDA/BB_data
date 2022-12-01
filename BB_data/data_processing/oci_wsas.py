from functions.data_functions import data
from functions.behavioural_functions import clean_up_columns, imputate, score
import pandas as pd


def oci_scoring() -> pd.DataFrame:
    
    '''
    main function for oci scoring.

    Parameters
    ----------
    None

    Returns
    -------
    oci_score: pandas df of oci results
 
    '''

    df = data('questionnaire_data.csv', 't2')

    oci_df = df.loc[:, '55.':'72.']
    oci_df = pd.concat([df['7.'], oci_df], axis=1)
    
    oci_scores = clean_up_columns(oci_df)
    oci_scores = imputate(oci_scores)
    oci_scores = score(oci_scores)

    return oci_scores[['B_Number', 'overall_score', 'group']]

def wsas_scoring() -> pd.DataFrame:
    
    '''
    main function for wsas scoring.

    Parameters
    ----------
    None

    Returns
    -------
    wsas_rscore: pandas df of wsas results.
    '''

    df = data('questionnaire_data.csv', 't2')

    wsas_df = df.loc[:, '97.':'101.']
    wsas_df = pd.concat([df['7.'], wsas_df], axis=1)
    wsas_score = clean_up_columns(wsas_df)
    wsas_score = imputate(wsas_score)
    wsas_score = score(wsas_score)

    return wsas_score[['B_Number', 'overall_score', 'group']]


if __name__ == '__main__':
    oci = oci_scoring()
    wsas = wsas_scoring()

