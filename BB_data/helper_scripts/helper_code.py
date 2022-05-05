'''
This script is not designed to be run but rather contains basic python/pandas commands to help.
A pandas cheat sheet
'''
import pandas as pd

#Code to read in data. In between the '' put the file path to the csv
df = pd.read_csv('')

#Select a column. Put column name in between ''
column = df['']

#Get individual rows of a column. Put the row number in the []
row = column.loc[] 

#Drop null values
no_na = column.dropna()

#This is how to replace values in a column/dataframe. In between the r'' put the value you want to replace and in between the value='' put what you want to replace it with. 
#This will use regex
no_na.replace(regex=True, inplace=True, to_replace=r'', value='')

#Change column type. Put inbetween () the datatype you wish to change the data type for.
column.astype()

#Create a new dataframe from other dataframes
new_dataframe = pd.concat(no_na, df)