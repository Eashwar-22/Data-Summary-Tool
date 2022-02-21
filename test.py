import pandas as pd
from analysis import data_analysis_v2

df = pd.read_csv('static/extras/Raw_FIFA_22_data.csv')
obj=data_analysis_v2(df)


