from functions.data_functions import data
import pandas as pd
import numpy as np
import re
import warnings
# To ignore all pandas .loc slicing suggestions
warnings.filterwarnings(action='ignore')


def main():
    '''
    Main function to calculate length of time between time point and time point 2

    Parameters
    ----------
    None

    Returns
    -------
    time_df:pandas df: Dataframe with difference in days and years between time point one and time point two.
    '''

    df_t2 = data('questionnaire_data.csv', 't2')
    df_t1 = data('participant_index.csv', 't2', straight_import=True)

    time = df_t2[''].iloc[:, 1]
    time = time.rename('finished')
    group = pd.concat([df_t2['7.'], time], axis=1)


    hc = group[group['7.'].str.contains('B1')]
    an = group[group['7.'].str.contains('B2')]
    hc['group'] = 'HC'
    an['group'] = 'AN'
   
    time_t2 = pd.concat([hc, an])
    time_t2.sort_values(by=['7.'], inplace=True)
    time_t2 = time_t2.reset_index(drop=True)

    time_points = pd.concat([df_t1, time_t2['finished']], axis=1)
    time_points['finished'] = time_points['finished'].apply(
        lambda value: re.sub(r'..:..:.. UTC', '', value))
    t1_dates = pd.to_datetime(time_points['initial'], dayfirst=True)
    t2_dates = pd.to_datetime(time_points['finished'])

    difference = pd.DataFrame()
    difference['days'] = t2_dates - t1_dates
    difference['years'] = difference['days'] / np.timedelta64(1, 'Y')

    time_df = pd.concat([time_points[['t1', 't2']], difference[[
                        'days', 'years']], time_t2['group']], axis=1)
    time_df = time_df.drop(axis=0, index=[133])
    return time_df

if __name__ == '__main__':
    time_df = main()
    