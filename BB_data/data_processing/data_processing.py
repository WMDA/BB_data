from functions import data_functions as data

dropindex = [72, 136, 138, 139, 141, 143, 144, 152, 156, 158, 159, 160, 176, 178, 181]
df = data.data('questionnaire_data.csv','t2', clean=True, drop_index=dropindex)
print(df.shape)