import unittest

import requests
import pymongo
import json

class TestLOSAPI(unittest.TestCase):

    # def test_all_segment_inference_by_period(self):
    #     segments_collection = pymongo.MongoClient('localhost', 27017).bktraffic['Segments']
    #     segment_id = []
    #     for doc in segments_collection.find():
    #         segment_id.append(doc['_id'])
    #     URL = 'http://192.168.1.3:8000/period_inference'
    #     data = {
    #         'segment_id': segment_id,
    #         'period': 'period_1_30',
    #         'date': 'Thu Feb 17 2022'
    #     }
    #     res = json.loads(requests.post(URL, json=data).content.decode('utf-8'))
    #     LOS_res = res['LOS']
    #     self.assertEqual(len(LOS_res), len(segment_id))

    # def test_time_inference_with_time_list(self):
    #     URL = 'http://192.168.1.3:8000/time_inference'
    #     data = {
    #         'segment_id': [1,2,3],
    #         'time': [1852405,1852405,1852405]
    #     }
    #     res = json.loads(requests.post(URL, json=data).content.decode('utf-8'))
    #     LOS_res = res['LOS']
    #     self.assertEqual(len(LOS_res), 3)

    # def test_error_code_sending_period_to_time_route(self):
    #     URL = 'http://192.168.1.3:8000/time_inference'
    #     data = {
    #         'segment_id': [1,2,3],
    #         'period': ['period_0_30', 'period_0_30', 'period_0_30'],
    #         'date': 'Thu Feb 17 2022'
    #     }
    #     res = json.loads(requests.post(URL, json=data).content.decode('utf-8'))

    def test_time_inference_with_single_timestamp(self):
        URL = 'http://192.168.1.5:8000/inference'
        data = {
            'segment_id': [1,2,3],
            'time': 1852405
        }
        res = json.loads(requests.post(URL, json=data).content.decode('utf-8'))
        velocity_res = res['LOS']
        self.assertEqual(len(velocity_res), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    