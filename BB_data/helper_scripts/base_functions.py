'''
This is a set of basic functions that can be used for data cleaning.
It is very basic but we will aim to make it more sophisticated as we go along. 

Usage:
Create a script then 
import base_functions as fun

fun.remove_str()
Function to read in data amd remove a lot of common string values.
Needs filepath to data and column name.
Also needs type of data being cleaned. Use psych for past psychiatric histories or meds for medication

fun.clean()
Write into the fun.clean():
Needs data
column that you want to clean
values you want to replace in the dataframe
value you want to change to.

fun.extract() Use this function to extract data from column.
Write into function
filepath
column

fun.check_column_values() Use this function to check what data type (i.e int, float etc)

fun.sum_up_values_in_df() Use this function to sum up all unique values in a column

Suggested workflow. fun.remove_str() then use the output of this to go into func.clean()
'''

import pandas as pd
import numpy as np
import re
import sys
import seaborn as sns
sns.set_theme(style="dark")

def data_overview(file:str, column:str, verbose:bool):
    
    '''
    Function that reads in data,  prints to terminal null values, data types of column and description

    Parameters
    ----------
    file:str filepath to data
    column:str column to clean
    verbose:bool if set to true will print out the data type of each column

    Returns
    -------
    nothing: prints to terminal null values, data types of column and description
    '''
    
    df = pd.read_csv(file)
    column = df[['7. What is your B number?', column]] 
    print('Datatypes of column:\n', column.dtypes)
    print('Description of column:\n', column.describe())
    
    null = column[column.isnull().any(axis=1)]
    print('Number of null values in:\n', column.isnull().sum())
    print(null)
    
    if verbose == True:
        df[column].apply(lambda value: print(type(value)))
    
    
def clean(file:object, column:str, to_replace:str, replace:str):

    '''
    Function to remove string from column.

    Parameters
    ----------
    columns_to_clean:object dataframe
    column:str column name to clean
    to_replace:str strig to replace in column
    replace:str string to add into column
    
    Returns
    -------
    columns_to_clean:dataframe cleaned column
    '''
    
    columns_to_clean = columns_to_clean.dropna()
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
    plotting = pd.DataFrame([hc_df.sum(), an_df.sum()], index=['HC','AN'], columns=[column])
    return plotting

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

def compile_type(type:str) -> object:
    
    '''
    Function to return re compile type. Will only accept psych or meds
    
    Parameters
    ----------
    type:str Either psych or meds
    
    Returns
    -------
    data:re.compile object 
    '''      
    if type == 'meds':
        data = re.compile(r'[0-9]|mg|mcg|\(.*\)|\bo.\b|\bt..\b|\.|\bd.*y\b|once|twice|morning|evening|currently|taking|for|inhaler|\b\w\b|', re.I)
    
    elif type == 'psych':
        data = re.compile(r'[0-9]|\(.*\)|\ba..\b|,|\.|�|diagno.*?\b|clin.*?\b|\)|not|offi.*?\b|\bi\b|\bnever\b|\bform.*?\b|\bmy\b|\bprevi.*?\b|\bha.*?\b|\bo.\b|with|:|\bhistor.*?\b|been|\bcurren.*?\b|yes|past', 
                          re.I)
    else:
        print('Unknown type. Please choose from meds, psych or weight')
        sys.exit(1) 
    
    return data
    
def remove_str(data:str, col:str, type:str):
    
    '''
    Function to remove common str in data. Replaces str with empty values for further processing by clean function.
    
    Parameters
    ----------
    data:str filepath to data
    col:str column name
    type:str compile type only accepts psych or meds
    
    Returns
    -------
    column:pd.Series column of cleaned values
    '''
    
    df = pd.read_csv(data)
    column = df[col].dropna().str.lower()
    data = compile_type(type) 
    
    if type == 'psych':
        anorexia = re.compile(r'anorexia|anorexia nervosa|nervosa')
        column.replace(regex=True, inplace=True, to_replace=anorexia, value='')
        column.replace(regex=True, inplace=True, to_replace=r'^\s', value=np.NaN)
        column = column.dropna()
        
    column.replace(regex=True, inplace=True, to_replace=data, value='')
    column.replace(regex=True, inplace=True, to_replace=r'^\s', value='')
    return column
