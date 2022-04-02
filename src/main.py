"""
Created on Mar 28, 2022

@author: tg
"""

import os
import sys
import glob
import pandas as pd
from math import nan


def min_without_nan(sensor_humidity: list) -> int:
    not_NaNs = [item for item in sensor_humidity if not pd.isnull(item)]
    if not_NaNs:
        return int(min(not_NaNs))


def avg_without_nan(sensor_humidity: list) -> int:
    not_NaNs = [item for item in sensor_humidity if not pd.isnull(item)]
    if not_NaNs:
        return int(sum(not_NaNs) / len(not_NaNs))


def max_without_nan(sensor_humidity: list) -> int:
    not_NaNs = [item for item in sensor_humidity if not pd.isnull(item)]
    if not_NaNs:
        return int(max(not_NaNs))


def order_by_avg(sensor_statistics: dict) -> str:
    sorted_sensors = sorted(sensor_statistics.items(), key=lambda x: x[1][1], reverse=True)
    res = ""
    for i in sorted_sensors:
        res += f"{i[0]},{','.join(map(str, i[1]))}\n"
    return res


def all_nans(humidity: list) -> bool:
    if [x for x in humidity if not pd.isnull(x)]:
        return False

    return True


def main():
    files_processed = 0
    succeeded_measurements = 0
    failed_measurements = 0

    try:
        path = sys.argv[1]
    except Exception as e:
        print(f"Exception: {e}.")
    finally:
        print("Path not found!\nSetting Path to default testing directory!")
        # Default Directory containing test files
        path = "../rsc/"
        print(f"Path: {path}\n")

    D = {}  # Dictionary that contains sensors' humidity values
    sensor_statistics = {}  # Dictionary containing sensors' min, avg, max

    for filename in glob.glob(path + '*.csv'):  # matching csv files

        files_processed += 1
        df = pd.read_csv(filename)

        print(df.head())  # printing a sample

        # Aggregates into the same sensor's id
        agg_sensors = df.groupby('sensor-id')['humidity'].apply(list)
        print(agg_sensors)

        # Adds to dictionary containing every sensor-id and their humidity values
        for sensor_id in agg_sensors.to_dict():
            if sensor_id in D:
                D[sensor_id] += agg_sensors[sensor_id]
            else:
                D[sensor_id] = agg_sensors[sensor_id]

        print(D)

        succeeded_measurements += df['humidity'].count()
        failed_measurements += sum(pd.isnull(df['humidity']))

    # Calculates each sensor statistics ignoring NaN values read
    for sensor_id in D:
        if not all_nans(D[sensor_id]):
            sensor_statistics[sensor_id] = [min_without_nan(D[sensor_id]),
                                            avg_without_nan(D[sensor_id]),
                                            max_without_nan(D[sensor_id])]

        else:  # All sensor's readings from given sensor-id are NaN
            sensor_statistics[sensor_id] = [nan, nan, nan]

    print(f"Unordered: {sensor_statistics.items()}\n\n# RESULTS:\n")

    print(f"Files Processed: {files_processed}")
    print(f"Succeeded Measurements: {succeeded_measurements}")
    print(f"Failed Measurements: {failed_measurements}")
    print(f"\nSorted by highest averages:\n\nsensor-id,min,avg,max")
    print(order_by_avg(sensor_statistics))


if __name__ == '__main__':
    main()
