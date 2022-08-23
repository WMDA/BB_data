from functions.data_functions import data
import pandas as pd
import numpy as np
import re
import warnings
# To ignore all pandas .loc slicing suggestions
warnings.filterwarnings(action='ignore')

df = data('questionnaire_data.csv', 't2')

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

print(f'\nHC age\n', hc_age['age'].describe(), f'\n\nAN age\n', an_age['age'].describe(
), f'\n\nCombined age\n', age_df['age'].describe())
print('\nAny AN individuals not recieving/didnt have treamtent:\n',
      an['15'].isnull().sum())
