'''
This is a base script that can be used for data cleaning.
It is very basic but we will aim to make it more sophisticated as we go along. 

Usage:
Write into the clean() function:
filepath to data
column that you want to clean
values you want to replace in the dataframe
value you want to change to.
Only call this function once

further_clean. Use this function as many times as it takes to clean. Usage
column that you want to clean
values you want to replace in the dataframe
value you want to change to.
'''

import pandas as pd

def clean(file:str, column:str, to_replace:str, replace:str):
    df = pd.read_csv(file)
    
    columns_to_clean = df[['7. What is your B number?', column]] 
    print('Datatypes of column:\n', columns_to_clean.dtypes)
    
    null = columns_to_clean[columns_to_clean.isnull().any(axis=1)]
    print('Number of null values in:\n', columns_to_clean.isnull().sum())
    print(null)

    columns_to_clean = columns_to_clean.dropna()
    columns_to_clean[column].replace(regex=True, inplace=True, to_replace=rf'{to_replace}', value=f'{replace}')

    return columns_to_clean

def further_clean(columns_to_clean:object, column:str, to_replace:str, replace:str):
    columns_to_clean[column].replace(regex=True, inplace=True, to_replace=rf'{to_replace}', value=f'{replace}')
    return columns_to_clean

df = clean()
print(df)

#df_further_clean = further_clean(df, ) DELETE the # if you want to run this code.
#print(df_further_clean)