from functions.data_functions import data
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings(action='ignore')# To ignore all pandas .loc slicing suggestions

edeq_df = data('ede-q_individual_scores.csv', 't1', straight_import=True)
t1_df = data('BEACON_participants.csv', 't1', straight_import=True)
key_df = data('participant_index.csv', 't2', straight_import=True)
hads_df = data('HADS_individual_scores.csv', 't1', straight_import=True)

key_df['t1'].iloc[38] = 'G1089'
key_df['t1'].iloc[126] = 'G2142'

key = re.compile('|'.join(key_df['t1'].to_list()))

t1 = t1_df[t1_df['G-Number'].str.contains(key, regex=True)]
edeq = edeq_df[edeq_df['PPT ID'].str.contains(key, regex=True)]
#hads = hads_df[hads_df['PPT ID'].str.contains(key, regex=True)]
hc = t1[t1['G-Number'].str.contains('G1')]
an = t1[t1['G-Number'].str.contains('G2')]
hc['group'] = 'HC'
an['group'] = 'AN'

t1 = pd.concat([hc, an])
