'''
Template to calculate the lowest weight.
Currently very messy but we can clean it up later.
This script so far removes all the annoying strig and turns all the data types to floats.
column '21.' is the lowerst ever weight column and column '7.' is the BMI column 
'''

import pandas as pd
import re
import warnings
warnings.filterwarnings(action='ignore')# To ignore all pandas .loc slicing suggestions

csv_name = '/home/wmda/data/questionnaire_data.csv' #Put name of the csv here. Remember the .csv extension.

dropindex = [72, 136, 138, 139, 141, 143, 144, 152, 156, 158, 159, 160, 167, 176, 178, 181, 182]
df = pd.read_csv(csv_name).drop(index=dropindex)
df.rename(columns=lambda name: re.sub(r'\D([^\s]+)', '', name), inplace=True)
bmi_df = df[['7.','21.']].dropna()

kg = bmi_df[bmi_df['21.'].str.contains('kg', regex=True)]
stone = bmi_df[bmi_df['21.'].str.contains('tone')]
com = pd.concat([kg, stone])
left_overs = bmi_df.drop(index=com.index).reset_index(drop=True)

kg = pd.concat([kg, left_overs.iloc[[0, 1, 3, 4, 6, 7, 8, 9, 10, 13, 16, 17, 18, 19, 20], [0, 1]]])
kg['21.'].replace(regex=True, inplace=True, to_replace=r'[a-zA-Z\'\?\(\)\,\~]|\/.', value='')
kg['21.'].replace(regex=True, inplace=True, to_replace=r'^\s.*?\b', value='')
kg['21.'].iloc[75] = 60
kg['21.'].loc[kg.index[61]] = 36.5 
kg['21.'].replace(regex=True, inplace=True, to_replace=r'[^0-9\.]\d+', value='')
kg['21.'].replace(regex=True, inplace=True, to_replace=r'\s', value='')
kg['21.'] = kg['21.'].astype(float)

stone = pd.concat([stone, left_overs.iloc[[11, 14], [0, 1]]])
stone['21.'].replace(regex=True, inplace=True, to_replace=r'[a-zA-Z\'\?\(\)\,\~]|\/.', value='')
stone['21.'].iloc[3] = 5.7
stone = stone.drop(stone.index[4])
stone['21.'].replace(regex=True, inplace=True, to_replace=r'\s.*?\b', value=r' ')
stone['21.'].replace(regex=True, inplace=True, to_replace=r'[^0-9\.]\D', value=r'')
stone['21.'].replace(regex=True, inplace=True, to_replace=r'\s$', value=r'')
stone['21.'].replace(regex=True, inplace=True, to_replace=r'\s', value=r'.')
stone['21.'] = stone['21.'].astype(float)

lb = left_overs.iloc[[2, 12]]
lb['21.'].replace(regex=True, inplace=True, to_replace=r'[a-z]', value='')
lb['21.'] = lb['21.'].astype(float)


'''
Your code goes below this. What we needs to turn stone and pounds into kg. 
In hight_weight.py there are single lines of code to do this and just needs to be copied over and
the column name changing.
'''
