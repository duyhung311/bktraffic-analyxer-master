import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timezone, timedelta
import numpy as np
import pickle
import torch
from os import listdir
from os.path import join
from src.velocity_estimator import *
from src.utils.path import VelocityEstimatorPath


def get_period(timestamp):
    dt = datetime.fromtimestamp(timestamp, tz=timezone(timedelta(hours=7)))
    period = time_to_period(dt.hour, dt.minute)
    
    return period


class VelocityEstimator():
    def __init__(self, start_date, end_date):
        self.path_helper = VelocityEstimatorPath()

        self.periods = ['period_00_00', 'period_00_30', 'period_01_00',
                        'period_01_30', 'period_02_00', 'period_02_30',
                        'period_03_00', 'period_03_30', 'period_04_00',
                        'period_04_30', 'period_05_00', 'period_05_30',
                        'period_06_00', 'period_06_30', 'period_07_00',
                        'period_07_30', 'period_08_00', 'period_08_30',
                        'period_09_00', 'period_09_30', 'period_10_00',
                        'period_10_30', 'period_11_00', 'period_11_30',
                        'period_12_00', 'period_12_30', 'period_13_00',
                        'period_13_30', 'period_14_00', 'period_14_30',
                        'period_15_00', 'period_15_30', 'period_16_00',
                        'period_16_30', 'period_17_00', 'period_17_30',
                        'period_18_00', 'period_18_30', 'period_19_00',
                        'period_19_30', 'period_20_00', 'period_20_30',
                        'period_21_00', 'period_21_30', 'period_22_00',
                        'period_22_30', 'period_23_00', 'period_23_30']

        self.segment_df, self.dummy_segment_row = self.load_segments_df(segment_csv_path=self.path_helper.segment_csv_filename())
        self.velocity_df, self.period_array, self.weekday_array, self.dummy_velocity_row = self.load_velocity_df(
            start_date=start_date,
            end_date=end_date,
            data_folder=self.path_helper.segment_status_folder_path()
        )
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = Net()

        self.model.load_state_dict(torch.load(self.path_helper.model_filename(), map_location=self.device))
        

    def load_segments_df(self, segment_csv_path):
        # Read segments csv
        segment_df = pd.read_csv(segment_csv_path)
        self.length_df = segment_df.set_index('_id')[['length']]
        self.dummy_length = self.length_df.mean(axis=0)[0]

        # Standard scaling features
        scaling_feature = ['length', 'long_snode', 'lat_snode', 'long_enode', 'lat_enode']
        segment_df[scaling_feature] = StandardScaler().fit_transform(segment_df[scaling_feature])

        # Load pickled one-hot encoder
        with open(self.path_helper.segment_id_encoder_path(), 'rb') as f:
            segment_id_encoder = pickle.load(f)
        with open(self.path_helper.street_level_encoder_path(), 'rb') as f:
            street_level_encoder = pickle.load(f)
        with open(self.path_helper.street_type_encoder_path(), 'rb') as f:
            street_type_encoder = pickle.load(f)
        
        # One-hot encoding features
        segment_df = one_hot_encoding(segment_df, '_id', segment_id_encoder, False)
        segment_df = one_hot_encoding(segment_df, 'street_type', street_type_encoder)
        segment_df = one_hot_encoding(segment_df, 'street_level', street_level_encoder)

        # Drop unneccessary columns
        segment_df = segment_df.drop(columns=['s_node_id', 'e_node_id', 'street_id', 'max_velocity', 'street_name'])
        dummy_segment_row = segment_df.drop(columns=['_id']).mean(axis=0)
        return segment_df, dummy_segment_row


    def load_velocity_df(self, start_date, end_date, data_folder):
        
        df = pd.DataFrame()
        period_array = []
        weekday_array = []
        
        for date in pd.date_range(start=start_date, end=end_date):
            date = str(date).split(' ')[0]
            for period_file in sorted(listdir(join(data_folder, date))):
                if period_file[:-4] in self.periods:
                    period_array.append(period_file[:-4])
                    period_df = pd.read_csv(join(data_folder, date, period_file), usecols=['segment_id', 'velocity', 'weekday']).set_index('segment_id')
                    period_df = period_df.astype({'velocity':'float64'})
                    weekday_array.append(period_df['weekday'].iloc[0])
                    period_df = period_df.drop(columns=['weekday'])
                    df = pd.concat([df, period_df], axis=1)

        dummy_row = df.mean(axis=0)
        return df, period_array, weekday_array, dummy_row


    def _build_dataset(self, df, period_array, weekday_array):

            # Create encoders
            weekday_encoder = OneHotEncoder()
            period_encoder = OneHotEncoder()

            weekday_encoder.fit([[0],[1],[2],[3],[4],[5],[6]])
            period_encoder.fit(np.expand_dims(np.array(self.periods), axis=1))

            # transform period list to numpy array
            period_array = np.array(period_array)
            period_array = np.expand_dims(period_array, axis=1)
            period_array = period_encoder.transform(period_array).toarray()

            # transform weekday list to numpy array
            weekday_array = np.array(weekday_array)
            weekday_array = np.expand_dims(weekday_array, axis=1)
            weekday_array = weekday_encoder.transform(weekday_array).toarray()

            spatial_feature = df.iloc[:, :1297]
            temporal_feature = df.iloc[:, 1297:]

            spatial_feature = spatial_feature.to_numpy() # (N, 1297)
            temporal_feature = temporal_feature.to_numpy() # (N, 1297:-1)

            temporal_feature = np.expand_dims(temporal_feature, axis=2) # (N, L, feat)
            period_array = np.tile(period_array, (temporal_feature.shape[0],1,1)) # (N, L, feat)
            weekday_array = np.tile(weekday_array, (temporal_feature.shape[0],1,1)) # (N, L, feat)
            temporal_feature = np.concatenate((temporal_feature, period_array, weekday_array), axis=2).astype('float32')

            # zeros = np.zeros((spatial_feature.shape[0], spatial_feature.shape[1], temporal_feature.shape[2]-1))
            # spatial_feature = np.concatenate((np.expand_dims(spatial_feature, axis=2), zeros), axis=2)
            # feature = np.concatenate((spatial_feature, temporal_feature), axis=1)

            spatial_feature = spatial_feature.astype('float32')
            temporal_feature = temporal_feature.astype('float32')

            return spatial_feature, temporal_feature


    def _preprocess(self, df, timestamp):
        # df = pd.DataFrame.from_dict({'segment_id': data['segment_id']})
        period = get_period(timestamp)
        period = period_to_number(period)

        #
        df = pd.merge(left=df, right=self.velocity_df.iloc[:, period:period+48].reset_index(), on='segment_id')
        # na_index = df[df.isna().any(axis=1)].index
        # df.iloc[na_index, 1:] = self.dummy_velocity_row[period:period+48].tolist()
        # append dummy row representing unmatch segment ids to the end of the dataframe
        matched_segment = list(map(lambda x: x.item(), list(df['segment_id'].unique())))
        df.loc[len(df)] = [np.int64(1)] + self.dummy_velocity_row[period:period+48].tolist()
        df["segment_id"] = df["segment_id"].astype(np.int64)

        #
        df = pd.merge(left=self.segment_df, right=df, how='right', left_on='_id', right_on='segment_id').drop(columns=['segment_id', '_id'])
        # na_index = df[df.isna().any(axis=1)].index
        df.iloc[-1, :1297] = self.dummy_segment_row.tolist()

        #
        spatial_feature, temporal_feature = self._build_dataset(df, self.period_array[period:period+48], self.weekday_array[period:period+48])
        return matched_segment, spatial_feature, temporal_feature

    
    def inference(self, data):
        if type(data['timestamp']) == list:
            d = {}
            for ts in data['timestamp']:
                period = get_period(ts)
                df = pd.DataFrame.from_dict({'segment_id': data['segment_id']})
                matched_segment, spatial_feature, temporal_feature = self._preprocess(df, ts)
                spatial_feature, temporal_feature = torch.from_numpy(spatial_feature).to(self.device), torch.from_numpy(temporal_feature).to(self.device)
                preds = self.model(spatial_feature, temporal_feature)
                preds = preds.squeeze(dim=1).tolist()
                df.loc[df["segment_id"].isin(matched_segment), "velocity"] = preds[:-1]
                df.loc[~df["segment_id"].isin(matched_segment), "velocity"] = preds[-1]
                df["LOS"] = df["velocity"].apply(velocity_to_los)
                d[period] = {'segment_id': data['segment_id'], 'velocity': df["velocity"].tolist(), 'LOS': df["LOS"].tolist()}
            return d
        else:
            df = pd.DataFrame.from_dict({'segment_id': data['segment_id']})
            matched_segment, spatial_feature, temporal_feature = self._preprocess(df, data["timestamp"])
            spatial_feature, temporal_feature = torch.from_numpy(spatial_feature).to(self.device), torch.from_numpy(temporal_feature).to(self.device)
            preds = self.model(spatial_feature, temporal_feature)
            preds = preds.squeeze(dim=1).tolist()
            df.loc[df["segment_id"].isin(matched_segment), "velocity"] = preds[:-1]
            df.loc[~df["segment_id"].isin(matched_segment), "velocity"] = preds[-1]
            df["LOS"] = df["velocity"].apply(velocity_to_los)
            return {'segment_id': data['segment_id'], 'velocity': df["velocity"].tolist(), 'LOS': df["LOS"].tolist()}

    
    def sequence_inference(self, data):
        curr_time = data['timestamp']
        times = []
        velocity = []
        for segment in data['segment_id']:
            df = pd.DataFrame.from_dict({'segment_id': [segment]})
            _, spatial_feature, temporal_feature = self._preprocess(df, curr_time)
            spatial_feature, temporal_feature = torch.from_numpy(spatial_feature).to(self.device), torch.from_numpy(temporal_feature).to(self.device)
            preds = self.model(spatial_feature, temporal_feature)
            est_velocity = los_to_velocity(preds) / 3.6 # to m/s
            
            try:
                # If segment exists in segments.csv
                segment_length = self.length_df.loc[segment][0]
            except Exception as e:
                # If segment does not exist in segments.csv
                segment_length = self.dummy_length

            est_time = float(segment_length) * 1000 / est_velocity

            times.append(est_time)
            velocity.append(preds.squeeze(dim=1).tolist()[0])
            
            curr_time += est_time

        LOS = list(map(velocity_to_los, velocity))
        return {'segment_id': data['segment_id'], 'velocity': velocity, 'ETA': times, 'LOS': LOS}
