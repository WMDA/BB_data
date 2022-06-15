'''
Template function to clean medication history.
'''

import base_functions as fun

data ="" #Put filepath to csv between "" here

df = fun.remove_str(data, "11.a. If yes please give details", "meds") 

updated_df = fun.clean(df, "", ) #After "", put all the words you want to remove from the data. Make sure they are all in "" and seperated by a , 
updated_df.replace(regex=True, inplace=True, to_replace=r"^\s.*?\b", value='') # Don't mess with can break everything
updated_df.apply(lambda x: print(x)) #put a # before this to stop printing out to the terminal
