'''
Script to upload raw data and calculated data to remote mysql server. 
Uploads all the raw data as well as calculated scores as well as indexes into BEACON database.
'''

# Package uploads
from functions.data_functions import connect_to_database, data
from BB_data.data_processing.hads import main as hads
from BB_data.data_processing.oci_wsas import main as oci_wsas
from BB_data.data_processing.height_weight import main as bmi
from BB_data.data_processing.edeq import main as edeq
from BB_data.data_processing.aq10 import main as aq10
from BB_data.data_processing.time import main as time
from BB_data.data_processing.t1_data import main as t1

# External uploads
import pandas as pd
import re

connector = connect_to_database('BEACON')

functions_time_point_2 = {
    'hads_t2': hads(),
    'oci_t2': oci_wsas('oci'),
    'wsas_t2': oci_wsas('wsas'),
    'bmi_t2': bmi(),
    'edeq_t2': edeq(),
    'aq10_t2': aq10(),
    'time_difference': time()
}

functions_time_point_1 = {
    "edeq_t1": t1('edeq'),
    "hads_t1": t1('hads'),
    "bmi_t1": t1('bmi'),
    "oci_t1": t1('oci'),
    "aq10_t1": t1('aq10'),
    "wsas_t1": t1('wsas')
}

raw_data = {
    "raw_edeq_t1": data('ede-q_individual_scores.csv', 't1', straight_import=True),
    "raw_t1": data('BEACON_participants.csv', 't1', straight_import=True),
    "participant_index": data('participant_index.csv', 't2', straight_import=True),
    "raw_hads_t1": data('HADS_individual_scores.csv', 't1', straight_import=True)
}

df_t2_raw = data('questionnaire_data.csv', 't2', simplify=False)
df_t2_raw = df_t2_raw.drop('Unique Response Number', axis=1)
df_t2_columns = df_t2_raw.columns
df_t2_raw.rename(columns=lambda name: re.sub(
    r'\D([^\s]+)', '', name), inplace=True)

df_t2_raw.rename(
    columns={df_t2_raw.columns[177]: 'time_finished'}, inplace=True)

df_t2_raw.rename(columns=lambda name: re.sub(
    r'\.', '', name), inplace=True)

column_index = pd.DataFrame(df_t2_columns)


column_index.to_sql('raw_t2_question_index', connector)
df_t2_raw.to_sql('raw_t2', connector)


for key, val in functions_time_point_2.items():
    t2_df = val
    try:
        t2_df.to_sql(key, connector)
    except Exception as e:
        print(key, e)

for key, val in functions_time_point_1.items():
    t1_df = val
    try:
        t1_df.to_sql(key, connector)
    except Exception as e:
        print(key, e)

for key, val in raw_data.items():
    raw_df = val
    try:
        raw_df.to_sql(key, connector)
    except Exception as e:
        print(key, e)
