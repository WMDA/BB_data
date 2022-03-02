from functions import data_functions as data
import pandas as pd
import numpy as np

dropindex = [72, 136, 138, 139, 141, 143, 144, 152, 156, 158, 159, 160, 176, 178, 181]
df = data.data('questionnaire_data.csv','t2', clean=True, drop_index=dropindex)
weight_check_null = df[df['19.'].isnull()]

weight = df['19.'].dropna()

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

stone = weight[weight.str.contains('tone')]
stone.replace(regex=True, inplace=True, to_replace=r'[a-zA-Z\'\?\(\)]|\s\s|\.', value='')
stone.replace(regex=True, inplace=True, to_replace=r'\s\s', value='.')
stone.replace(regex=True, inplace=True, to_replace=r'.$', value='')
stone.loc[82] = '7.6'
stone = stone.astype(float)
stone = stone.apply(lambda stone: stone * 6.35029318)


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

