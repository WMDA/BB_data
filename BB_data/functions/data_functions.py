import pandas as pd
from decouple import config
import os
import re


def data(csv):
    
    '''
    Function to load csv and  multiple responses from participants 

    Parameters
    ----------
    csv: str. Name of csv to load

    Returns
    -------
    final_df = pandas dataframe with removed multiple responses from participants.
    '''
    
    try:
        t2 = config('t2')
        
    except Exception:
        
        #This is an extremely hacky way to get the .env file when using juptyer notebooks. 
        
        filepath = []
        env_file_location = os.path.split(os.path.split(os.environ['PWD'])[0])[0]
        
        with open(f'{env_file_location}/.env', 'r') as env:
            for line in env:
                
                if 't2' in line:
                    filepath.append(line)
                    
    t2 = re.findall(r'/.*/*',filepath[0])[0]


    df = pd.read_csv(f'{t2}/{csv}')
    df.rename(columns=lambda x: re.sub(r'\D','', x), inplace=True)

    df_bnumber =  df['7'].apply(lambda value: str(value))
    repeat_values = df[df_bnumber.str.contains('_2')]

    final_df = df.drop(index=repeat_values.index)

    return final_df

