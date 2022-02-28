import pandas as pd
from decouple import config
import re




t2 = config('t2')

df = pd.read_csv(f'{t2}/questionnaire_data.csv')
df.rename(columns=lambda x: re.sub(r'\D','', x), inplace=True)
df_bnumber =  df['7'].apply(lambda value: str(value))
df_index = df[df_bnumber.str.contains('_2')]



final_df = df.drop(index=df_index.index)

print(df.shape)
print(final_df.shape)