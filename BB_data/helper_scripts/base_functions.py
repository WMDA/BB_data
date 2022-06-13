'''
This is a set of basic functions that can be used for data cleaning.
It is very basic but we will aim to make it more sophisticated as we go along. 

Usage:
Create a script then 
import base_functions as fun

fun.clean()
Write into the fun.clean():
filepath to data
column that you want to clean
values you want to replace in the dataframe
value you want to change to.
Only call this function once

fun.further_clean(). Use this function as many times as it takes to clean. Usage
column that you want to clean
values you want to replace in the dataframe
value you want to change to.

fun.extract() Use this function to extract data from column.
Write into function
filepath
column

fun.check_column_values() Use this function to check what data type (i.e int, float etc)

fun.sum_up_values_in_df() Use this function to sum up all unique values in a column

'''

import pandas as pd
import seaborn as sns
sns.set_theme(style="dark")

def clean(file:str, column:str, to_replace:str, replace:str):
    
    '''
    Function that reads in data, prints out the number of null values in the data
    and cleans the column by changing specified string to another string.

    Parameters
    ----------
    file:str filepath to data
    column:str column to clean
    to_replace:str strig to replace in column
    replace:str string to add into column

    Returns
    -------
    columns_to_clean:dataframe Dataframe of participants id and cleaned column
    '''
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

    '''
    Function to further remove string from column.

    Parameters
    ----------
    columns_to_clean:object dataframe
    column:str column name to clean
    to_replace:str strig to replace in column
    replace:str string to add into column
    
    Returns
    -------
    columns_to_clean:dataframe Further cleaned column
    '''

    columns_to_clean[column].replace(regex=True, inplace=True, to_replace=rf'{to_replace}', value=f'{replace}')
    return columns_to_clean

def extract(file:str, column:str):
    df = pd.read_csv(file)
    columns = df[['7. What is your B number?', column]]
    
    dummies = pd.get_dummies(columns.iloc[0:,1])
    measure = pd.concat([columns.iloc[0:,0],dummies], axis=1).dropna()
    an = measure[measure.iloc[0:,0].str.contains('B2')]
    hc = measure[measure.iloc[0:,0].str.contains('B1')]
    
    dataframes ={ 
        'an' : an,
         'hc' : hc
    }

    return dataframes

def create_plotting_df(hc_df, an_df, column:str):
    plotting = pd.DataFrame([hc_df.sum(), hc_df.sum()], index=['HC','AN'], columns=[column])
    return plotting

def check_column_values(file:str, column:str):
    '''
    This is a function to describe a column. It will also loop through each value 
    
    Parameters
    ----------
    file:str filepath to data
    column:str column name to describe
    
    Returns
    -------
    Prints to terminal the descriptive values of the terminal and the 
    '''
    df = pd.read_csv(file)
    print(df[column].describe())
    df[column].apply(lambda value: print(type(value)))
    

def sum_up_values_in_df(file:str, column:str, verbose:bool=False):
    
    '''
    Function to sum up all the unique values in a dataframe.
    Prints out unique values  
    
    Parameters
    ----------
    file:str filepath to data
    column:str column name to describe
    verbose:bool Set to True if you want to print out the unique values as well.
    This option is good if there are lots of unique values
    
    Returns
    -------
    Prints out unique values
    '''
    
    df = pd.read_csv(file)
    print(df[column].value_counts())
    
    if verbose==True:
        print(df[column].unique())
