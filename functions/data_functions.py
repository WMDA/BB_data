import pandas as pd
from decouple import config
import os
import re
import sys


def load_enviornment(datapath):
    
    '''
    Function to load information from .env file.

    Parameters
    ----------
    datapath: str. Name of variable for datapath in the .env file.

    Returns
    -------
    data_path: str. Datapath from .env file 
    '''
    
    try:
        data_path = config(datapath)
        
    except Exception:
        
        #This is an extremely hacky way to get the .env file if decouple fails. 
        
        filepath = []
        env_file_path = os.path.split(os.path.split(os.environ['PWD'])[0])[0]
    
        if os.path.exists(os.path.join(env_file_path, '/.env')) == True:
            env_file_location = os.path.join(env_file_path, '/.env')
    
        elif os.path.exists(os.path.join(env_file_path, 'BB_data/.env')) == True: 
            env_file_location = os.path.join(env_file_path, 'BB_data/.env')
        
        with open(env_file_location, 'r') as env:
           for line in env:
               if datapath in line:
                   filepath.append(line)
                    
        data_path = re.findall(r'/.*/*',filepath[0])[0]
    
    return data_path

def data(csv, datapath, simplify=True, clean=False, drop_index=False):
    
    '''
    Function to load csv and remove multiple responses from participants. 

    Parameters
    ----------
    csv: str. Name of csv to load.
    datapath: str. Name of variable for datapath in the .env file.
    simplify: Boolean. Renames columns in dataframe to numbers (str) rather than the long format.
    clean: Boolean. Clean the dataframe further by dropping values in an index
    drop_index: list of int. List of int of index values to drop, to use with clean.

    Returns
    -------
    final_df = pandas dataframe with removed multiple responses from participants.
    '''

    t2 = load_enviornment(datapath)
    df = pd.read_csv(f'{t2}/{csv}')

    if simplify == True:
        df.rename(columns=lambda x: re.sub(r'\D', '', x), inplace=True)

    if clean == True:
        
        if drop_index == False:
            raise Exception('No index provided. Please provide an index with drop_index= parameter')
        
        try:
            df = df.drop(index=drop_index)
        
        except Exception:
            print('Unable to use index provided. Please make sure index is a list of int that are in range of the dataframe')
            sys.exit(1)


    df_bnumber =  df['7'].apply(lambda value: str(value))
    repeat_values = df[df_bnumber.str.contains('_2')]
    final_df = df.drop(index=repeat_values.index)

    return final_df

