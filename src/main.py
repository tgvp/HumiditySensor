'''
Created on Mar 28, 2022

@author: tg
'''
import os
import sys
import glob
import pandas as pd
from math import nan

def getMin_Without_NaN(L: list):
    notNaNs = [item for item in L if not pd.isnull(item) == True]
    if (notNaNs):
        return int(min(notNaNs))
    return nan

def getAvg_Without_NaN(L: list):
    notNaNs = [item for item in L if not pd.isnull(item) == True]
    if (notNaNs):
        return int(sum(notNaNs)/len(notNaNs))
    return nan

def getMax_Without_NaN(L: list):
    notNaNs = [item for item in L if not pd.isnull(item) == True]
    if (notNaNs):
        return int(max(notNaNs))
    return nan

def orderBy_AvgList(D: dict):
    sorted_sensors = sorted(D.items(), key=lambda x: x[1][1], reverse=True)
    res = ""
    for i in sorted_sensors:
        res += f"{i[0]},{','.join(map(str, i[1]))}\n"
    return res

def is_AllNaNs(humidity: list):
    if (not humidity):
        if (pd.isnull(humidity[0]) and humidity.all()):
            return True
        
def main():

    FILES_PROCESSED = 0
    SUCCEDED_MEASUREMENTS = 0
    FAILED_MEASUREMENTS = 0

    path = sys.argv[1]

    if os.path.exists(path):

        D = {} # Dictionary that contains sensors' humidity values
        Sensor_Statistics = {} # Dictionary containing sensors' min, avg, max

        for filename in glob.glob(path + '*.csv'): # matching csv files

            FILES_PROCESSED += 1
            df = pd.read_csv(filename)

            print(df.head()) # printing a sample

            # Aggregates into the same sensor's id
            agg_sensors = df.groupby('sensor-id')['humidity'].apply(list)
            print(agg_sensors)

            # Adds to dictionary containing every sensor-id and their humidity values
            for sensor_id in  agg_sensors.to_dict():
                if sensor_id in D:
                    D[sensor_id] += agg_sensors[sensor_id]
                else:
                    D[sensor_id] = agg_sensors[sensor_id]

            print(D)

            SUCCEDED_MEASUREMENTS += df['humidity'].count()
            FAILED_MEASUREMENTS  += sum(pd.isnull(df['humidity']))

        # Calculates each sensor statistics ignoring NaN values read
        for sensor_id in D:
            if (not is_AllNaNs(D[sensor_id])):
                Sensor_Statistics[sensor_id] = [getMin_Without_NaN(D[sensor_id]),
                                                getAvg_Without_NaN(D[sensor_id]),
                                                getMax_Without_NaN(D[sensor_id])]

            else: # All sensor's readings from given sensor-id are NaN
                Sensor_Statistics[sensor_id] = [nan,nan,nan]

            print(orderBy_AvgList(Sensor_Statistics))


        print(f'Files Processed: {FILES_PROCESSED}')
        print(f'Succeded Measurements: {SUCCEDED_MEASUREMENTS}')
        print(f'Failed Measurements: {FAILED_MEASUREMENTS}') 
        print(f"\nSorted by highest averages:\n\nsensor-id,min,avg,max")
        print(orderBy_AvgList(Sensor_Statistics))

    else:
        print("Path not found! Path: " + str(path))


if __name__ == '__main__':
    main()