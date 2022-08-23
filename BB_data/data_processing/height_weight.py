from functions.data_functions import data, connect_to_database, load_enviornment
from functions.behavioural_functions import calculating_bmi
import pandas as pd
import numpy as np
import math
import warnings
# To ignore all pandas .loc slicing suggestions
warnings.filterwarnings(action='ignore')


def main():
    '''
    Main function. Takes no parameters and returns calculated BMI dataframe
    '''

    df = data('questionnaire_data.csv', 't2')
    bmi_df = df[['7.', '19.', '20.']].dropna()

    # filters kilograms and turns to float
    kg = bmi_df.loc[bmi_df['19.'].str.contains('g')]
    kg['19.'].replace(regex=True, inplace=True,
                      to_replace=r'[a-zA-Z\'\?\(\)\,]', value='')
    kg['19.'].replace(regex=True, inplace=True, to_replace=r'^\D', value='')
    index = kg.loc[kg['19.'].str.contains('-')]
    kg['19.'].loc[index.index[1]] = '41.5'
    kg['19.'].loc[index.index[2]] = '45'
    kg['19.'].replace(regex=True, inplace=True, to_replace=r'-', value='')
    kg['19.'].replace(regex=True, inplace=True, to_replace=' ', value='')
    kg['19.'].replace(regex=True, inplace=True, to_replace='', value=np.nan)
    kg = kg.dropna()
    kg['19.'] = kg['19.'].astype(float)

    # filters stone, converts to float and then kilograms
    stone = bmi_df.loc[bmi_df['19.'].str.contains('tone')]
    stone['19.'].replace(regex=True, inplace=True,
                         to_replace=r'[a-zA-Z\'\?\(\)]|\s\s|\.', value='')
    stone['19.'].replace(regex=True, inplace=True,
                         to_replace=r'\s\s', value='.')
    stone['19.'].replace(regex=True, inplace=True, to_replace=r'.$', value='')
    stone_index = stone.loc[stone['19.'].str.contains('/')]
    stone['19.'].loc[stone_index.index[0]] = '7.7'
    stone['19.'] = stone['19.'].astype(float)
    # Convert pounds to a fraction and then to kilos
    stone['19.'] = stone['19.'].apply(lambda stone: (
        (math.modf(stone)[0]/14) * 10 + math.modf(stone)[1]) * 6.350293)

    # filters out leftovers from other two regexs, converts to float and then kilograms.
    # no stone values need to be transformed as they are all .0
    to_drop_index = pd.concat([kg, stone])
    leftovers = bmi_df.drop(index=to_drop_index.index)
    leftover_kg_index = leftovers['19.'].loc[leftovers['19.'].str.contains(
        '-')]
    leftovers['19.'].loc[leftover_kg_index.index[1]] = 53.5

    leftovers['19.'].replace(regex=True, inplace=True,
                             to_replace=r'[a-zA-Z\'\?\(\)-]', value='')
    leftovers['19.'].replace(regex=True, inplace=True,
                             to_replace=r' ', value='')
    leftovers['19.'].replace(regex=True, inplace=True,
                             to_replace='', value=np.nan)
    leftovers = leftovers.dropna()
    leftovers['19.'] = leftovers['19.'].astype(float)

    leftovers['19.'].loc[34] = leftovers['19.'].loc[34] * \
        6.35029318  # stone to kgs
    leftovers['19.'].loc[63] = leftovers['19.'].loc[63] * 6.35029318
    leftovers['19.'].loc[24] = leftovers['19.'].loc[24] * \
        0.4535924  # pound to kg
    leftovers['19.'].loc[71] = leftovers['19.'].loc[71] * 0.4535924

    height = pd.concat([kg, stone, leftovers])

    # Filters out cms and converts to float
    cm = height[height['20.'].str.contains('cm')]
    cm['20.'].replace(regex=True, inplace=True, to_replace=r'cm', value='')
    cm['20.'] = cm['20.'].astype(float)

    # Filters out meters, converts to float and then cm
    meters_df = height.drop(index=cm.index)
    meters = meters_df[meters_df['20.'].str.contains('m')]
    meters['20.'].replace(regex=True, inplace=True,
                          to_replace=r'm.*?', value='.')
    meters['20.'].replace(regex=True, inplace=True, to_replace=r'.$', value='')
    meters['20.'].replace(regex=True, inplace=True, to_replace=r' ', value='')
    meters['20.'] = meters['20.'].astype(float)
    meters['20.'] = meters['20.'].apply(lambda meter: meter * 100)

    # Filters out feet, converts to float and then cm
    ft = height[height['20.'].str.contains(r'f.*?', regex=True)]
    ft['20.'].replace(regex=True, inplace=True, to_replace=r' ', value='')
    ft['20.'].replace(regex=True, inplace=True,
                      to_replace=r'ft|foot|for', value='.')
    ft['20.'].replace(regex=True, inplace=True,
                      to_replace=r'in.*|Approx', value='')
    ft['20.'].loc[120] = '5'
    ft['20.'] = ft['20.'].astype(float)
    ft['20.'] = ft['20.'].apply(lambda feet: (
        (math.modf(feet)[0]/12) * 10 + math.modf(feet)[1]) * 30.48)

    # Filters out undefined, converts to float and then cm
    height_to_drop = pd.concat([ft, meters, cm])
    height_leftovers = height.drop(index=height_to_drop.index)
    height_leftovers['20.'].replace(
        regex=True, inplace=True, to_replace=r'�|[\'\"]|[\’\”]', value='.')
    height_leftovers['20.'].replace(
        regex=True, inplace=True, to_replace=r'[A-Za-z]', value='')
    height_leftovers['20.'].replace(
        regex=True, inplace=True, to_replace=r'\.\.|\s|\.$', value='')

    height_leftovers['20.'] = height_leftovers['20.'].astype(float)

    height_leftovers['20.'] = height_leftovers['20.'].apply(lambda height: ((math.modf(height)[0]/12) * 10 + math.modf(height)[1]) * 30.48
                                                            if height < 100 and height > 2
                                                            else (height * 100 if height > 1 and height < 2
                                                            else height))

    final_df = pd.concat([cm, ft, height_leftovers])
    final_df['bmi'] = calculating_bmi(final_df['19.'], final_df['20.'])
    hc = final_df[final_df['7.'].str.contains('B1')]
    an = final_df[final_df['7.'].str.contains('B2')]
    hc['group'] = 'HC'
    an['group'] = 'AN'
    final_df = pd.concat([hc, an])

    return final_df


if __name__ == '__main__':
    bmi_df = main()
    df = bmi_df.sort_values(by='7.').reset_index(drop=True).rename(
        columns={'7.': 'b-number', '19.': 'kg', '20.': 'cm'})
    print(df)
