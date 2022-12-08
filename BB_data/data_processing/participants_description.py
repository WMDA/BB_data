from functions.data_functions import data, load_enviornment
import pandas as pd
import numpy as np
import re
import warnings
# To ignore all pandas .loc slicing suggestions
warnings.filterwarnings(action='ignore')


t1  = load_enviornment('t1')
t2 = load_enviornment('t2')


df = data('questionnaire_data.csv', 't2')
df_t1 = pd.read_csv(f'{t1}/BEACON_participants_behavioural_analysis.csv')
participant_index = pd.read_csv(f'{t2}/participant_index.csv').rename(columns={'t1': 'G-Number'})
df_t1 = pd.merge(df_t1, participant_index[['G-Number', 't2']], on='G-Number', how='right')

time = df[''].iloc[:, 1]
time = time.rename('finished')
treatment = df['15'].iloc[:, 1]
age_group = pd.concat([df[['7.', '8.']], time, treatment], axis=1)


hc = age_group[age_group['7.'].str.contains('B1')]
an = age_group[age_group['7.'].str.contains('B2')]
hc['group'] = 'HC'
an['group'] = 'AN'

age = pd.concat([hc, an])
age.sort_values(by=['7.'], inplace=True)
age = age.reset_index(drop=True)


age['finished'] = age['finished'].apply(
    lambda value: re.sub(r'..:..:.. UTC', '', value))
dob = pd.to_datetime(age['8.'], dayfirst=True)
questionaire_dates = pd.to_datetime(age['finished'])

age_df = pd.DataFrame(age[['7.', 'group']])
age_df['age'] = (questionaire_dates - dob) / np.timedelta64(1, 'Y')

hc_age = age_df[age_df['7.'].str.contains('B1')]
an_age = age_df[age_df['7.'].str.contains('B2')]

time_point = pd.concat([participant_index[['G-Number', 't2']], pd.to_datetime(participant_index['initial'], dayfirst=True)], axis=1)
time_point = pd.merge(time_point, age.rename(columns={'7.': 't2'}), on='t2', how='left').drop(['15', '8.'], axis=1).dropna()
time_point['follow_up'] = (pd.to_datetime(time_point['finished'], dayfirst=True) - time_point['initial'] ) / np.timedelta64(1, 'Y')

illness_duraton_at_t2 = pd.merge(df_t1[['G-Number', 'Illness_duration']], time_point[['follow_up', 'G-Number']], on='G-Number', how='right')
illness_duraton_an = illness_duraton_at_t2['Illness_duration'] + illness_duraton_at_t2['follow_up'] 

print(f'\nHC age at T1 mean and std', df_t1[df_t1['G-Number'].str.contains('G1')]['Age'].mean(), df_t1[df_t1['G-Number'].str.contains('G1')]['Age'].std())
print(f'\nHC age at T2 mean and std', hc_age['age'].mean(), hc_age['age'].std())  
print(f'\nAN age at T1 mean and std', df_t1[df_t1['G-Number'].str.contains('G2')]['Age'].mean(), df_t1[df_t1['G-Number'].str.contains('G2')]['Age'].std())
print(f'\nAN age at T1 mean and std', df_t1[df_t1['G-Number'].str.contains('G2')]['Age'].mean(), df_t1[df_t1['G-Number'].str.contains('G2')]['Age'].std())
print(f'\nAN age at T2 mean and std', an_age['age'].mean(), an_age['age'].std())  
print(f'\nAN illness duration at T1 mean and std', df_t1[df_t1['G-Number'].str.contains('G2')]['Illness_duration'].mean(), df_t1[df_t1['G-Number'].str.contains('G2')]['Illness_duration'].std())
print(f'\nAN illness duration at T1 mean and std', illness_duraton_an.mean(), illness_duraton_an.std())
print(f'\nHC follow up mean and std', time_point[time_point['G-Number'].str.contains('G1')]['follow_up'].mean(), time_point[time_point['G-Number'].str.contains('G1')]['follow_up'].std())
print(f'\nAN follow up mean and std', time_point[time_point['G-Number'].str.contains('G2')]['follow_up'].mean(), time_point[time_point['G-Number'].str.contains('G2')]['follow_up'].std())





print('\nAny AN individuals not recieving/didnt have treamtent:\n',
      an['15'].isnull().sum())
