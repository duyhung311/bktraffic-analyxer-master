import pandas as pd

rename_cols = {
    'createdAt': 'created_at',
    'updatedAt': 'updated_at',
    'start_node': 's_node_id',
    'end_node': 'e_node_id',
    'street': 'street_id'
}
segments_df = pd.read_csv('los_dataset/data_origin/segments.csv').rename(columns=rename_cols)
streets_df = pd.read_csv('los_dataset/data_origin/streets.csv').rename(columns={'_id': 'street_id'})

new_df = segments_df.merge(streets_df[['street_id', 'max_velocity']], on='street_id')


result_cols = ['_id', 'created_at', 'updated_at', 's_node_id', 
               'e_node_id', 'length', 'street_id', 'max_velocity',
               'street_level', 'street_name', 'street_type']

new_df[result_cols].to_csv('los_dataset/dataset/temp_segments.csv', index=False)