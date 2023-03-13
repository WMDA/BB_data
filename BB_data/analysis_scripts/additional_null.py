from functions.data_functions import load_data, save_pickle
import pandas as pd
import bambi as bmb

print('Initialising script to run mixed effect models\n')
print('\nLoading in data')
# Load in data
pca_df = load_data('BEACON', 'pca_df')

#Define number of components to loop over
comp = ['comp_1', 'comp_2','comp_3']

print('\nOrganising data into long form')
# Build a dictionary of re-organised dataframes
dfs = {}

for component in comp:
    comp_df = pca_df[['G_Number', 
           f'{component}_t2', f'{component}_t1','group', 
           ]].rename(columns={f'{component}_t1':'t1', f'{component}_t2':'t2', 'G_Number':'participants'})
           
    comp_df['id'] = comp_df.index
    comp_df = pd.melt(comp_df, value_vars=['t2','t1'], id_vars='participants').sort_values(by=['participants'], ascending=True).reset_index(drop=True)
    comp_df['group'] = comp_df['participants'].apply(lambda group: 'HC' if 'G1' in group else 'AN')

    dfs[component] = comp_df

# Model parameters
draw_numb = 2000
tune_numb = 4000
target_accept_numb = 0.95

# Define two model dictionaries, one to save as pickle (needs to be str) and one to use in the analysis
models = {

}

saved_models = {

}

# Define the models
print('Defining the models\n')
for component in comp:

    null_model = bmb.Model('value ~ variable + (1|participants)', dfs[component])
    models[component] = null_model
    saved_models[component] = str(null_model)

print('\nSaving models to pickle file')
save_pickle('saved_additional_null_models', saved_models)

# Fit the models
fitted_models = {

}

print('Building the models\n')
for component in comp:
    print('\nRunning model', models[component].formula, component)
    fitted = models[component].fit(draws=draw_numb, tune=tune_numb, target_accept=target_accept_numb)
    fitted_models[component] = fitted
    print('\nFinshed calculating model')

print('\nSaving fitted models')
save_pickle('fitted_models_additional_null_models', fitted_models)