import pandas as pd
from decouple import config
import re
import os

print(os.environ)

t2 = config('t2')

df = pd.read_csv(f'{t2}/questionnaire_data.csv')
df.rename(columns=lambda x: re.sub(r'\D','', x), inplace=True)