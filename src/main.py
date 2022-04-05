"""
Created on Mar 28, 2022

@author: tg
"""

import sys
import glob
import pandas as pd
from math import nan
from dataclasses import dataclass, field


@dataclass(order=True)
class SensorStats:
    id: str
    humidity: list[str]
    humidity_not_nans: list[str]
    min_humidity: float = nan
    avg_humidity: float = nan
    max_humidity: float = nan
    sort_index: int = -1

    def __init__(self, id, humidity):
        """Constructor takes dictionary pair of key, values and calculates stats of each sensor's id."""
        self.id = id
        self.humidity = humidity
        self.humidity_not_nans = [item for item in self.humidity if not pd.isnull(item)]

        if self.humidity_not_nans:
            self.min_humidity = self.min_without_nan()
            self.avg_humidity = self.avg_without_nan()
            self.max_humidity = self.max_without_nan()
            self.sort_index = self.avg_humidity

    def min_without_nan(self) -> int:
        """Retrieves the minimum humidity read while ignoring NaN values."""
        return int(min(self.humidity_not_nans))

    def avg_without_nan(self) -> int:
        """Retrieves the average humidity read while ignoring NaN values."""
        return int(sum(self.humidity_not_nans) / len(self.humidity_not_nans))

    def max_without_nan(self) -> int:
        """Retrieves the maximum humidity read while ignoring NaN values."""
        return int(max(self.humidity_not_nans))

    def __repr__(self):
        return f"{self.id},{self.humidity},{self.min_humidity},{self.avg_humidity},{self.max_humidity}"

    def __str__(self):
        return f"{self.id},{self.min_humidity},{self.avg_humidity},{self.max_humidity}"


def order_by_avg(sensor_stats: list[SensorStats]) -> list[SensorStats]:
    """Order each Sensor by the highest average humidity read."""
    return sorted(sensor_stats, key=lambda x:x.sort_index, reverse=True)


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

    D = {}  # Dictionary that contains sensors' humidity values. Being used as placeholder for the aggregation.

    for filename in glob.glob(path + '*.csv'):  # matching csv files

        files_processed += 1
        df = pd.read_csv(filename)

        print(f"Dataframe sample {files_processed}\n{df.head()}\n")  # printing a sample

        # Aggregates into the same sensor's id
        agg_sensors = df.groupby('sensor-id')['humidity'].apply(list)
        print(f"Aggregation\n{agg_sensors}\n")

        # Adds to dictionary containing every sensor-id and their humidity values
        for sensor_id in agg_sensors.to_dict():
            if sensor_id in D:
                D[sensor_id] += agg_sensors[sensor_id]
            else:
                D[sensor_id] = agg_sensors[sensor_id]

        succeeded_measurements += df['humidity'].count()
        failed_measurements += sum(pd.isnull(df['humidity']))

    # List of Sensors' objects containing humidity, min, avg and max values
    sensor_stats = [SensorStats(sensor_id, D[sensor_id]) for sensor_id in D]

    print(f"Unordered: {sensor_stats}\n\n# RESULTS:\n")

    print(f"Files Processed: {files_processed}")
    print(f"Succeeded Measurements: {succeeded_measurements}")
    print(f"Failed Measurements: {failed_measurements}")
    print(f"\nSorted by highest averages:\n\nsensor-id,min,avg,max")
    print('\n'.join(map(str, order_by_avg(sensor_stats))))


if __name__ == '__main__':
    main()
