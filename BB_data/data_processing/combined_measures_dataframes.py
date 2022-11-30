from functions.data_functions import load_data, connect_to_database
import pandas as pd

participant_index = load_data('BEACON', 'participant_index').rename(columns={'t2':'B_Number'})

# Load in data from time point 1
###########################################################################################################
t1_ede_q_df = load_data('BEACON', 'edeq_t1').rename(columns={'Restraint': 'restraint_score_t1',
                                                             'Eating Concern': 'eatinG_Nconcern_score_t1',
                                                             'Shape Concern': 'shape_concern_score_t1',
                                                             'Weight Concern': 'weight_concern_score_t1',
                                                             'Total Score': 'global_score_t1'
                                                             })
t1_hads_df = load_data('BEACON', 'hads_t1').rename(columns={'anxiety': 'anxiety_t1',
                                                            'depression': 'depression_t1'
                                                            })
t1_oci_df = load_data('BEACON', 'oci_t1').rename(
    columns={'Initial_OCI_Total_score': 'oci_score_t1'})
t1_bmi_df = load_data('BEACON', 'bmi_t1').rename(
    columns={'BMI_baseline': 'bmi_t1'})
t1_aq_df = load_data('BEACON', 'aq10_t1').rename(
    columns={'Initial_AQ10': 'aq_score_t1'})
t1_wsas_df = load_data('BEACON', 'wsas_t1').rename(
    columns={'initial_WSAS': 'wsas_score_t1'})

edeq_hads = t1_hads_df.merge(t1_ede_q_df, on='G_Number', how='left')
oci_bmi = t1_oci_df.merge(t1_bmi_df, on='G_Number', how='left')
t1_df_oci = oci_bmi.merge(edeq_hads, on='G_Number', how='left')
t1_df_aq = t1_df_oci.merge(t1_aq_df, on='G_Number', how='left')
t1_df = t1_df_aq.merge(t1_wsas_df, on='G_Number', how='left').drop(['group_x_x', 'group_x_y', 'group_y_x', 'group_y_y', 'index_x_x',
                                                                    'index_y_x', 'index_x_y', 'index_y_y', 'group_x', 'index_y', 'index_x'], axis=1).rename(columns={'group_y': 'group'})

# Load in data from time point 2
###########################################################################################################

t2_ede_q_df = pd.merge(participant_index['B_Number'], load_data('BEACON', 'edeq_t2').rename(columns={'restraint_score': 'restraint_score_t2',
                                                             'eating_concern_score': 'eating_concern_score_t2',
                                                             'shape_concern_score': 'shape_concern_score_t2',
                                                             'weight_concern_score': 'weight_concern_score_t2',
                                                             'global_score': 'global_score_t2'

                                                             }), right_on='B_Number', left_on='B_Number', how='left')


t2_hads_df = pd.merge(participant_index['B_Number'], load_data('BEACON', 'hads_t2').rename(columns={'overall_score': 'HADS_score_t2',
                                                            'anxiety': 'anxiety_t2',
                                                            'depression': 'depression_t2'
                                                            }), right_on='B_Number', left_on='B_Number', how='left')
t2_wsas_df = pd.merge(participant_index['B_Number'], load_data('BEACON', 'wsas_t2'), right_on='B_Number', left_on='B_Number', how='left')
t2_wsas_df = t2_wsas_df[['B_Number', 'overall_score']].rename(
    columns={'overall_score': 'wsas_score_t2'})

t2_oci_df = pd.merge(participant_index['B_Number'],load_data('BEACON', 'oci_t2'), right_on='B_Number', left_on='B_Number', how='left')

t2_bmi_df = pd.merge(participant_index['B_Number'], load_data('BEACON', 'bmi_t2'), right_on='B_Number', left_on='B_Number', how='left')#.sort_values('B_Number')
t2_bmi_df = t2_bmi_df[['B_Number', 'bmi']].rename(columns={'bmi': 'bmi_t2'})



t2_aq_df = pd.merge(participant_index['B_Number'], load_data('BEACON', 'aq10_t2').rename(
    columns={'overall_score': 'aq_score_t2'}),right_on='B_Number', left_on='B_Number', how='left' )
t2_oci_df = pd.merge(participant_index['B_Number'], t2_oci_df[['B_Number', 'overall_score']].rename(
    columns={'overall_score': 'oci_score_t2'}), right_on='B_Number', left_on='B_Number', how='left')


t2_df = pd.concat([participant_index['B_Number'], t2_aq_df.drop(['B_Number', 'group'], axis=1), t2_hads_df.drop(['B_Number', 'group'], axis=1), t2_bmi_df.drop(['B_Number'], axis=1), t2_oci_df.drop(['B_Number'], axis=1), t2_wsas_df.drop(['B_Number'], axis=1), t2_ede_q_df.drop(['B_Number', 'group'], axis=1), t2_aq_df['group']], axis=1).drop('index', axis=1)

t2_df['group'].loc[17] = 'HC'
t2_df['group'].loc[47] = 'HC'


# Connect amd save to database
########################################################################################################################################
connector = connect_to_database('BEACON')
t1_df.to_sql('t1_measures', connector)

t2_df.to_sql('t2_measures', connector)