from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from functions.data_functions import load_data


# Call dataframes
t1_ede_q_df = load_data('BEACON', 'edeq_t1')
t1_hads_df = load_data('BEACON', 'hads_t1')
t1_oci_df = load_data('BEACON', 'oci_t1')
t1_bmi_df = load_data('BEACON', 'bmi_t1')

#Merge dataframes into one dataframe
edeq_hads = t1_hads_df.merge(t1_ede_q_df, on='PPT ID', how='left')
edeq_hads = edeq_hads.rename(columns={'PPT ID':'G-Number'})
oci_bmi = t1_oci_df.merge(t1_bmi_df, on='G-Number', how='left')
t1_df = oci_bmi.merge(edeq_hads, on='G-Number', how='left')

# Divide dataframe into AN and HC and drop not needed columns
hc_t1 = t1_df[t1_df['G-Number'].str.contains('G1')].drop(['G-Number', 'group_x_x', 'group_x_y', 'group_y_x', 'group_y_y'], axis=1)
an_t1 = t1_df[t1_df['G-Number'].str.contains('G2')].drop(['G-Number', 'group_x_x', 'group_x_y', 'group_y_x', 'group_y_y'], axis=1)

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
'''
Preprocessing Standardize features by removing the mean and scaling to unit variance.

z = (x - u) / s

where u is the mean and s is the standard deviation
'''

scaler = StandardScaler()
hc_t1_std = scaler.fit_transform(hc_t1.dropna())
an_t1_std = scaler.fit_transform(an_t1.dropna())

# PCA analysis
pca_hc = PCA()
pca_hc.fit(hc_t1_std)
print(pca_hc.explained_variance_ratio_)
hc_scores = pca_hc.transform(hc_t1_std)

pca_an = PCA()
pca_an.fit(an_t1_std)
#print(pca_an.explained_variance_ratio_)

wcss = []

for cluster_number in range(1,21):
    kmeans_pca = KMeans(n_clusters=cluster_number, random_state=42)
    kmeans_pca.fit(hc_scores)
    wcss.append(kmeans_pca.inertia_)

plt.plot(range(1,21), wcss, marker='o', linestyle='--')
plt.show()
