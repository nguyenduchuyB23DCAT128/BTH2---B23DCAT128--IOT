import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

url = "http://localhost:8086"
token = "VuaTrader:D"
org = "PTIT"
bucket = "IOT_DATA"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

query = f'''
from(bucket: "{bucket}")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "sensor_data")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
'''

print("Dang doc du lieu tu InfluxDB...")
df = query_api.query_data_frame(query)

if isinstance(df, list):
    if len(df) == 0:
        df = pd.DataFrame()
    else:
        df = df[0]

if df.empty:
    print("Khong co du lieu tho de xu ly!")
else:
    df['_time'] = pd.to_datetime(df['_time'])
    df = df.sort_values('_time')

    df = df.ffill().bfill()

    if 'temperature' in df.columns:
        Q1 = df['temperature'].quantile(0.25)
        Q3 = df['temperature'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df['temperature'] = np.clip(df['temperature'], lower_bound, upper_bound)

    df.set_index('_time', inplace=True)
    df_resampled = df.resample('1min').mean(numeric_only=True)

    if 'temperature' in df_resampled.columns:
        df_resampled['temp_rolling_mean'] = df_resampled['temperature'].rolling(window=3, min_periods=1).mean()
        df_resampled['temp_delta'] = df_resampled['temperature'].diff().fillna(0)

    df_resampled = df_resampled.dropna()

    print("Dang ghi du lieu da tien xu ly vao measurement moi...")

    for index, row in df_resampled.iterrows():
        point = (
            Point("sensor_processed")
            .tag("student", "B23DCAT128")
            .field("temperature_clean", float(row.get('temperature', 0)))
            .field("humidity_clean", float(row.get('humidity', 0)))
            .field("temp_rolling_mean", float(row.get('temp_rolling_mean', 0)))
            .field("temp_delta", float(row.get('temp_delta', 0)))
            .time(index)
        )
        write_api.write(bucket=bucket, org=org, record=point)

    print("Hoan thanh qua trinh tien xu ly va day len measurement sensor_processed thanh cong!")

client.close()