from functions.data_functions import connect_to_database
from BB_data.data_processing.hads import main as hads
from BB_data.data_processing.oci_wsas import main as oci_wsas
from BB_data.data_processing.height_weight import main as bmi
from BB_data.data_processing.edeq import main as edeq
from BB_data.data_processing.aq10 import main as aq10
from BB_data.data_processing.time import main as time
from BB_data.data_processing.t1_data import main as t1

import pandas as pd

connector = connect_to_database('BEACON')

functions_time_point_2 = {
    'hads': hads(),
    'oci': oci_wsas('oci'),
    'wsas': oci_wsas('wsas'),
    'bmi': bmi(),
    'edeq': edeq(),
    'aq10': aq10(),
    'time': time()
}


for key, val in functions_time_point_2.items():
    print(key)

# This code is just to check that the connector is working
df = pd.read_sql("Show tables;", connector)
print(df)
