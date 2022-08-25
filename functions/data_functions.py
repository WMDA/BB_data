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
    datapath:str of name of variable for datapath in the .env file.

    Returns
    -------
    data_path:str of datapath from .env file 
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

    csv:str conntaining name of csv to load.
    datapath:str: containing the name of variable for datapath in the .env file.
    simplify:Boolean that renames columns in dataframe to numbers (str) rather than the long format.
    stright_import: Boolean that loads csvs and does no processing to the data.

    Returns
    -------
    final_df:pandas dataframe of data with removed multiple responses from participants.
    df:pandas dataframe of data with no processing. Returned with stright_import=True.
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

    except Exception as e:
        final_df = df
        print('unable to remove duplicates due to the following error:', e)

    if simplify == True:
        final_df.rename(columns=lambda name: re.sub(
            r'\D([^\s]+)', '', name), inplace=True)

    return final_df


def connect_to_database(database: str):
    '''
    Function to connect to an mysql/mariaDB database. Credential and host need to be stored in a
    .env file

    Parameters: 
    -----------
    Database:str  Name of database

    Returns:
    -------
    engine:sqlalchemy engine connection
    '''

    # Username and password are not stored on github!
    cred = {
        'user': b64decode(load_enviornment('user')).decode(),
        'password': b64decode(load_enviornment('password')).decode(),
    }

    user = cred['user']
    passwd = cred['password']
    host = load_enviornment('host')

    connector = create_engine(
        f'mysql+mysqlconnector://{user}:{passwd}@{host}/{database}')

    return connector


def load_data(database: str, table: str, show_tables: bool = False) -> pd.DataFrame:

    '''
    Function to load sql tables as dataframes.

    Parameters
    ---------
    database: str of database name.
    table: str of table name.
    show_tables: boolean which if set to true prints all the tables in the database.

    Returns
    -------
    pd.Dataframe of requested table
    '''

    connector = connect_to_database(database)
    
    if show_tables == False:
        return pd.read_sql(table, connector)
    else:
        print(pd.read_sql("Show tables;", connector))


