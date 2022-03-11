from functions.data_functions import data
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings(action='ignore')# To ignore all pandas .loc slicing suggestions

def main(measure, describe=False):
    edeq_df = data('ede-q_individual_scores.csv', 't1', straight_import=True)
    t1_df = data('BEACON_participants.csv', 't1', straight_import=True)
    key_df = data('participant_index.csv', 't2', straight_import=True)
    hads_df = data('HADS_individual_scores.csv', 't1', straight_import=True)

    key = re.compile('|'.join(key_df['t1'].to_list()))

    t1 = t1_df[t1_df['G-Number'].str.contains(key, regex=True)]
    edeq = edeq_df[edeq_df['PPT ID'].str.contains(key, regex=True)]
    hads = hads_df[hads_df['PPT ID'].str.contains(key, regex=True)]
    
    hc = t1[t1['G-Number'].str.contains('G1')]
    an = t1[t1['G-Number'].str.contains('G2')]
    hc['group'] = 'HC_t1'
    an['group'] = 'AN_t1'
    t1 = pd.concat([hc, an])

    if describe != False:
        print(f'\n\nHC {describe}\n', hc[describe].describe(), f'\n\nAN {describe}\n', an[describe].describe(), f'\n\nCombined {describe}\n', t1[describe].describe())
        
    hads['anxiety'] = hads[['67. Tense (a)', '69. Frightened (a)', '71. Worry (a)', '73. Relaxed (a)', '75. Frightened feeling (a)', '77. Restless (a)', '79. Panic (a)']].sum(axis=1)
    hads['depression'] = hads[['68. Enjoy (d)', '70. Laugh (d)', '72. Cheerful (d)', '74. Slowed down (d)', '76. Appearance interest (d)', '78. Looking forward to things (d)', 
                               '80. Enjoy book (d)']].sum(axis=1)
    hc = hads[hads['PPT ID'].str.contains('G1')]
    an = hads[hads['PPT ID'].str.contains('G2')]
    hc['group'] = 'HC_t1'
    an['group'] = 'AN_t1'
    hads = pd.concat([hc, an])
    
    hc = edeq[edeq['PPT ID'].str.contains('G1')]
    an = edeq[edeq['PPT ID'].str.contains('G2')]
    hc['group'] = 'HC_t1'
    an['group'] = 'AN_t1'
    edeq = pd.concat([hc, an])

    if measure == 'edeq':
        return edeq[['PPT ID', 'Restraint', 'Eating Concern', 'Shape Concern', 'Weight Concern', 'Total Score', 'group']]
    elif measure == 'hads':
        return hads
    elif measure == 'bmi':
        return t1[['G-Number', 'BMI_baseline', 'group']]
    elif measure == 'aq10':
        return t1[['G-Number', 'Initial_AQ10', 'group']]
    elif measure == 'wsas':
        return t1[['G-Number', 'initial_WSAS', 'group']]
    elif measure == 'oci':
        return t1[['G-Number', 'Initial_OCI_Total_score', 'group']]
    else:
        print('unknown measure , returning nothing')



if __name__ == '__main__':
    edeq_score = main('edeq') 
    hads_score = main('hads')
    bmi_score = main('bmi')
    oci_score = main('oci')
    aq10_score = main('aq10')
    wsas_score = main('wsas')
    
    age = main('none', describe='Age')