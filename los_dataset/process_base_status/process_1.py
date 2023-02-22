from pymongo import MongoClient
import pandas as pd

uri = 'mongodb://bktraffic:v%5B%21WH7BZbL7~L5y.@api.bktraffic.com:27017/bktraffic?authSource=bktraffic&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
db = MongoClient(uri)['bktraffic']

basicTrafficStatus = db['Basic_Traffic_Status']

segment_dict = dict()

for x in basicTrafficStatus.find():
    segment_dict[x['segmentId']] = x['segmentStatus']

df = pd.DataFrame(segment_dict)
df = df.drop(labels='sdfsdf', axis=0) # this line is very important, no jokes
df.index.name = 'period'

df.to_csv('los_dataset/dataset/temp_base_status.csv')