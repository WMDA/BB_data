from functions.data_functions import data
from functions.behavioural_functions import scoring
import pandas as pd


def main(measure: str, verbose=False) -> pd.DataFrame:
    '''
    main function for oci/wsas scoring.

    Parameters
    ----------
    measure: str, to calculate oci or wsas
    verbose: boolean, prints out number of null values and null values.

    Returns
    -------
    oci_results: pandas df of oci results
    wsas_results: pandas df of wsas results.
    '''

    df = data('questionnaire_data.csv', 't2')

    if measure == 'oci':

        oci_df = df.loc[:, '55.':'72.']
        null_index = oci_df[oci_df.isnull().any(axis=1)]
        oci_scores = scoring(oci_df)
        oci_results = pd.concat(
            [df['7.'], oci_scores], axis=1).dropna()
        hc = oci_results[oci_results['7.'].str.contains('B1')]
        an = oci_results[oci_results['7.'].str.contains('B2')]
        hc['group'] = 'HC_t2'
        an['group'] = 'AN_t2'
        oci_results = pd.concat([hc, an])

        if verbose == True:
            print('\nNumber of null values:', '\n',
                  oci_df.isnull().sum(), '\n')
            print('\nParticipants with null values:\n',
                  df['7.'].iloc[null_index.index])

        return oci_results

    else:

        wsas_df = df.loc[:, '97.':'101.']
        null_index = wsas_df[wsas_df.isnull().any(axis=1)]
        wsas_scores = scoring(wsas_df)
        wsas_results = pd.concat(
            [df['7.'], wsas_scores], axis=1).dropna()
        hc = wsas_results[wsas_results['7.'].str.contains('B1')]
        an = wsas_results[wsas_results['7.'].str.contains('B2')]
        hc['group'] = 'HC_t2'
        an['group'] = 'AN_t2'
        wsas_results = pd.concat([hc, an])

        if verbose == True:
            print('\nNumber of null values:', '\n',
                  wsas_df.isnull().sum(), '\n')
            print('\nParticipants with null values:\n',
                  df['7.'].iloc[null_index.index])

        return wsas_results


if __name__ == '__main__':
    oci = main('oci', verbose=True)
    wsas = main('wsas', verbose=True)