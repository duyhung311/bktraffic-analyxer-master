import pandas as pd
import re
import os

os.makedirs('los_dataset/dataset', exist_ok=True)

A = '[106.6290559, 10.8042433]'
def extract(s):
    coords = re.findall(r"[-+]?[0-9]*\.[0-9]*|[-+]?[0-9]+", s)
    return float(coords[0]), float(coords[1])

data = pd.read_csv('los_dataset/data_origin/nodes.csv', index_col='_id')
data.rename(columns={'location.coordinates':'location'}, inplace=True)


longs = pd.Series(0, index=data.index)
lats = pd.Series(0, index=data.index)
for index, row in data.iterrows():
    long, lat = extract(row['location'])
    longs.loc[index] = long
    lats.loc[index] = lat

df = pd.concat([longs, lats], axis=1).rename(columns={0: 'long', 1: 'lat'})
df.to_csv('los_dataset/dataset/nodes.csv')