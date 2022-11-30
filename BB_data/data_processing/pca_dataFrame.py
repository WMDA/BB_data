'''
Script to create a pca dataframe with all participants on the correct rows
'''

from functions.data_functions import load_data, connect_to_database
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')

# Load in the data
##################################################################################
t1 = load_data('BEACON', 'pca_t1').rename(columns={'comp_1': 'comp_1_t1', 'comp_2': 'comp_2_t1', 'comp_3': 'comp_3_t1' })
t2 = load_data('BEACON', 'pca_t2').rename(columns={'comp_1': 'comp_1_t2', 'comp_2': 'comp_2_t2', 'comp_3': 'comp_3_t2' })
index = load_data('BEACON', 'participant_index').replace('\n','')

# Make dictionary of participant indexes as keys and values
#################################################################################
g_number_participant_dict =dict(zip(index['t1'].to_list(), index['t2'].to_list()))
b_number_participant_dict =dict(zip(index['t2'].to_list(), index['t1'].to_list()))

# Loop through dataframes getting G-Numbers and the corresponding B-Numbers and applying to dataframes.  
#######################################################################################################
t1_order = index['t1'].to_list()
t2_order = index['t2'].to_list()

t1_df_list = []
for particpant in t1_order:
   row = t1[t1['G-Number']==particpant]
   row['B-Number'] = g_number_participant_dict[particpant]
   t1_df_list.append(row)

t2_df_list = []
for particpant in t2_order:
   row = t2[t2['B-Number']==particpant]
   row['G2-Number'] = b_number_participant_dict[particpant]
   t2_df_list.append(row)

t1_ordered_df = pd.concat(t1_df_list).reset_index(drop=True).drop(['index'], axis=1)
t2_ordered_df = pd.concat(t2_df_list).reset_index(drop=True).drop(['index'], axis=1)

# Merge dataframes on B-Number
##########################################################################################
combined_df = t2_ordered_df.merge(t1_ordered_df, how='left', on='B-Number').drop(['G-Number', 'group_x', 'group_y'], axis=1).rename(columns={'G2-Number': 'G-Number'})

# concat the rest of missing participants 
##########################################################################################
missing_values = t1[~t1["G-Number"].isin(combined_df["G-Number"])]
missing_values
added_missing_values = pd.concat([missing_values, combined_df]).sort_values(by='G-Number').drop(['group', 'index', 'B-Number'], axis=1).reset_index(drop=True)

# Label groups
##########################################################################################
hc = added_missing_values[added_missing_values['G-Number'].str.contains('G1')]
hc['group'] = 'HC'
an = added_missing_values[added_missing_values['G-Number'].str.contains('G2')]
an['group'] = 'AN'

# Save to Mysql database
#########################################################################################
pca_df = pd.concat([hc,an]).rename(columns={'G-Number': 'participant'})
connector = connect_to_database('BEACON')
pca_df.to_sql('pca_data', connector)
