from functions.data_functions import data


df = data('questionnaire_data.csv', 't2')

clean = df['10.'].str.lower()
clean.replace(regex=True, inplace=True, to_replace=r",|-", value='')
clean.replace(regex=True, inplace=True,
              to_replace=r"white british ", value='white british')
print(clean.value_counts())
#clean.apply(lambda x: print(x))
