import pandas as pd

import sys
sys.path.append("/Users/hungluong/opt/anaconda3/lib/python3.9/site-packages")

from sklearn.preprocessing import OneHotEncoder

def period_to_number(period):
    hour, min = period.split('_')[1:]
    return int(hour)*2 + (min != '00')

def time_to_period(hour, minute):
    m = '00' if minute < 30 else '30'
    return f"period_{hour}_{m}"

def velocity_to_los(velocity):
    """
    Taken from getLOSFromVelocity() function in bktraffic-server
    """
    if velocity < 15:
        return 'F'
    elif velocity >= 15 and velocity < 20:
        return 'E'
    elif velocity >= 20 and velocity < 25:
        return 'D'
    elif velocity >= 25 and velocity < 30:
        return 'C'
    elif velocity >= 30 and velocity < 35:
        return 'B'
    return 'A'

def los_to_velocity(LOS):
    """
    Taken from getVelocityFromLOS() function in bktraffic-server
    """
    if LOS == 'A':
        return 35.0
    elif LOS == 'B':
        return 30.0
    elif LOS == 'C':
        return 25.0
    elif LOS == 'D':
        return 20.0
    elif LOS == 'E':
        return 15.0
    elif LOS == 'F':
        return 10.0
    return 45.0

# 6h-8h, 16h-19h
def infer_peaks(period):
    peaks = ['period_6_00', 'period_6_30',
             'period_7_00', 'period_7_30',
             'period_8_00', 'period_8_30',
             'period_16_00', 'period_16_30',
             'period_17_00', 'period_17_30',
             'period_18_00', 'period_18_30',
             'period_19_00', 'period_19_30']
    for index in range(len(peaks)):
        if peaks[index] == period:
            return index+1
    return 0

def infer_holiday(date):
    # holidays = [(day, month)]
    holidays = [(1,1), (14,2), (8,3), (30,4), 
                (1,5), (1,6), (2,9), (20,10), 
                (20,11), (24,12), (25,12), (31,12)]
    for index in range(len(holidays)):
        if date.day == holidays[index][0] and \
           date.month == holidays[index][1]:
            return index+1
    return 0

def one_hot_encoding_segment(df, col_name, range):
    encoder = OneHotEncoder(categories=range)
    transformed = encoder.fit_transform(df[col_name].to_numpy().reshape(-1, 1))
    new_col_name = list(map(lambda x: col_name + '_' + x.split('_')[1], encoder.get_feature_names_out()))
    ohe_df = pd.DataFrame(transformed.toarray(), columns=new_col_name)
    new_df = pd.concat([ohe_df, df], axis=1).drop([col_name], axis=1)
    return new_df, encoder

def one_hot_encoding(df, col_name, encoder, drop_orig_col=True):
    transformed = encoder.transform(df[col_name].to_numpy().reshape(-1, 1))
    new_col_name = list(map(lambda x: col_name + '_' + x.split('_')[1], encoder.get_feature_names_out()))
    ohe_df = pd.DataFrame(transformed.toarray(), columns=new_col_name)
    new_df = pd.concat([ohe_df, df], axis=1)
    if drop_orig_col:
        new_df = new_df.drop([col_name], axis=1)
    return new_df
