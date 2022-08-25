import base_functions as fun
import pandas as pd


df = pd.read_csv()

clean = df['10. What is your ethnicity?']

'''
This should work now leave the first '' and you can put in as many words etc afterwards.
'''

fun.clean(clean, '', 'white', '/', 'British')

print(clean)
