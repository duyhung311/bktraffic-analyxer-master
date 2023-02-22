from pymongo import MongoClient
import pandas as pd
from os import getcwd, makedirs
from os.path import join

uri = 'mongodb://bktraffic:v%5B%21WH7BZbL7~L5y.@api.bktraffic.com:27017/bktraffic?authSource=bktraffic&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
db = MongoClient(uri)['bktraffic']

makedirs('los_dataset/data_origin', exist_ok=True)

def create_df_from_collection(collection, attributes):
    d = {}

    for a in attributes:
        if a == 'location':
            d['location.coordinates'] = []
        else:
            d[a] = []
    
    for x in collection.find():
        for a in attributes:
            try:
                if a == 'location':
                    d['location.coordinates'].append(x['location']['coordinates'])
                else:
                    d[a].append(x[a])
            except Exception as e:
                d[a].append(None)

    return pd.DataFrame.from_dict(d).reset_index(drop=True)

segment_reports_collection = db['SegmentReports']
segments_collection = db['Segments']
streets_collection = db['Streets']
nodes_collection = db['Nodes']

# Export segment_reports
segment_reports_dict = create_df_from_collection(segment_reports_collection, ['_id', 'createdAt', 'segment', 'updatedAt', 'velocity'])
segment_reports_dict.to_csv('los_dataset/data_origin/segment_reports.csv', index=False)
print('Finised exporting segment_reports.csv!')

# Export segment_reports
segments_dict = create_df_from_collection(segments_collection, ['_id', 'createdAt', 'end_node', 'length', 'start_node', 'street', 'street_level', 'street_name', 'street_type', 'updatedAt'])
segments_dict.to_csv('los_dataset/data_origin/segments.csv', index=False)
print('Finised exporting segments.csv!')

# Export streets
streets_dict = create_df_from_collection(streets_collection, ['_id', 'level', 'max_velocity', 'name', 'type'])
streets_dict.to_csv('los_dataset/data_origin/streets.csv', index=False)
print('Finised exporting streets.csv!')

# Export nodes
nodes_dict = create_df_from_collection(nodes_collection, ['_id', 'location'])
nodes_dict.to_csv('los_dataset/data_origin/nodes.csv', index=False)
print('Finised exporting nodes.csv!')