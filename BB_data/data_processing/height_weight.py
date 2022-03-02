from functions import data_functions as data
import pandas as pd
import numpy as np

dropindex = [72, 136, 138, 139, 141, 143, 144, 152, 156, 158, 159, 160, 176, 178, 181]
df = data.data('questionnaire_data.csv','t2', clean=True, drop_index=dropindex)
weight_check_null = df[df['19.'].isnull()]
weight = df['19.'].dropna()

#filters kilograms and turns to float 
kg = weight[weight.str.contains('g')]
kg.replace(regex=True, inplace=True, to_replace=r'[a-zA-Z\'\?\(\)\,]', value='')
kg.replace(regex=True, inplace=True, to_replace=r'^\D', value='')
index = kg.loc[kg.str.contains('-')]
kg.loc[index.index[1]] = '41.5'
kg.loc[index.index[2]] = '45'
kg.replace(regex=True, inplace=True, to_replace=r'-', value='')
kg.replace(regex=True, inplace=True, to_replace=' ', value='')
kg.replace(regex=True, inplace=True, to_replace='', value=np.nan)
kg = kg.dropna().astype(float)

#filters stone, converts to float and then kilograms
stone = weight[weight.str.contains('tone')]
stone.replace(regex=True, inplace=True, to_replace=r'[a-zA-Z\'\?\(\)]|\s\s|\.', value='')
stone.replace(regex=True, inplace=True, to_replace=r'\s\s', value='.')
stone.replace(regex=True, inplace=True, to_replace=r'.$', value='')
stone.loc[82] = '7.6'
stone = stone.astype(float)
stone = stone.apply(lambda stone: stone * 6.35029318)

#filters out leftovers from other two regexs, converts to float and then kilograms
to_drop_index = pd.concat([kg, stone])
leftovers = weight.drop(index=to_drop_index.index)
leftovers.replace(regex=True, inplace=True, to_replace=r'[a-zA-Z\'\?\(\)-]', value='')
leftovers.replace(regex=True, inplace=True, to_replace=r' ', value='')
leftovers.replace(regex=True, inplace=True, to_replace='', value=np.nan)
leftovers = leftovers.dropna().astype(float)
leftovers.loc[34] = leftovers.loc[34] * 6.35029318
leftovers.loc[63] = leftovers.loc[63] * 6.35029318
leftovers.loc[24] = leftovers.loc[24] * 0.4535924
leftovers.loc[71] = leftovers.loc[71] * 0.4535924
leftovers.loc[98] = 53.5


height_check_null = df[df['20.'].isnull()]
height = df['20.'].dropna()

#Filters out cms and converts to float
cm = height[height.str.contains('cm')]
cm.replace(regex=True, inplace=True, to_replace=r'cm', value='')
cm = cm.astype(float)

#Filters out meters, converts to float and then cm
meters_df = height.drop(index=cm.index)
meters = meters_df[meters_df.str.contains('m')]
meters.replace(regex=True, inplace=True, to_replace=r'm.*?', value='.')
meters.replace(regex=True, inplace=True, to_replace=r'.$', value='')
meters.replace(regex=True, inplace=True, to_replace=r' ', value='')
meters = meters.astype(float)
meters = meters.apply(lambda meter: meter * 100)

#work on this section
ft = height[height.str.contains('ft')]
ft.replace(regex=True, inplace=True, to_replace=r'[A-Za-z]', value='')
print(ft)