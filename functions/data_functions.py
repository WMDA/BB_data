import pandas as pd
from decouple import config
from sqlalchemy import create_engine
from base64 import b64decode
import os
import re

def load_enviornment(datapath: str):
    '''
    Function to load information from .env file.

    Parameters
    ----------
    datapath:str: Name of variable for datapath in the .env file.

    Returns
    -------
    data_path:str: Datapath from .env file 
    '''

    try:
        data_path = config(datapath)

    except Exception:

        # This is an extremely hacky way to get the .env file if decouple fails.

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

        data_path = re.findall(r'/.*/*', filepath[0])[0]

    return data_path


def data(csv: str, datapath: str, simplify: bool = True, straight_import: bool = False) -> pd.DataFrame:
    '''
    Function to load csv and remove multiple responses from participants. 

    Parameters
    ----------

    csv:str: Name of csv to load.
    datapath:str: Name of variable for datapath in the .env file.
    simplify:Boolean: Renames columns in dataframe to numbers (str) rather than the long format.
    stright_import:Boolean: Loads csvs and does no processing to the data.

    Returns
    -------
    final_df:pandas dataframe: Data with removed multiple responses from participants.
    df:pandas dataframe: Data with no processing. Returned with stright_import=True.
    '''

    t2 = load_enviornment(datapath)
    df = pd.read_csv(f'{t2}/{csv}')

    if straight_import == True:
        return df

    try:
        df_bnumber = df['7. What is your B number?'].apply(
            lambda value: str(value))
        repeat_values = df[df_bnumber.str.contains('_')]
        dropped_known_repeats_df = df.drop(
            index=repeat_values.index).reset_index(drop=True)
        duplicates = dropped_known_repeats_df.loc[dropped_known_repeats_df['7. What is your B number?'].duplicated(
        )]
        final_df = dropped_known_repeats_df.drop(
            index=duplicates.index).reset_index(drop=True)

    except Exception:
        final_df = df

    if simplify == True:
        final_df.rename(columns=lambda name: re.sub(
            r'\D([^\s]+)', '', name), inplace=True)

    return final_df


def connect_to_database(host: str, database: str, credentials: dict = {'user': 'Default', 'password': 'Default'}):
    '''
    Function to connect to an mysql/mariaDB database.

    Parameters: 
    -----------
    host:str Host either IP or localhost 
    Database:str  Name of database
    credentials:dict dict of username and password details. If left to default will search for enviormental variables.

    Returns:
    -------
    engine:sqlalchemy engine connection
    '''

    if credentials['user'] == 'Default' and credentials['password'] == 'Default':

        # Username and password are not stored on github!!

        cred = {
            'user': b64decode(load_enviornment('user')).decode(),
            'password': b64decode(load_enviornment('password')).decode()
        }

    else:
        cred = credentials

    user = cred['user']
    passwd = cred['password']

    engine = create_engine(
        f'mysql+mysqlconnector://{user}:{passwd}@{host}/{database}')

    return engine
