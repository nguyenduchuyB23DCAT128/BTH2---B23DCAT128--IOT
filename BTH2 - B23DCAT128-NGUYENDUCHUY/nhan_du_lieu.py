import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

token = "huydeptrai"
org = "PTIT"
bucket = "IOT_DATA"
db_client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = db_client.write_api(write_options=SYNCHRONOUS)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    
    t = float(data["temperature"])
    h = float(data["humidity"])
    l = int(data["light"])
    
    point = Point("sensor_data")
    point.tag("student", "NguyenDucHuy_B23DCAT128")
    point.field("temperature", t)
    point.field("humidity", h)
    point.field("light", l)
    
    write_api.write(bucket=bucket, org=org, record=point)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "NguyenDucHuy_B23DCAT128_sub")
mqtt_client.on_message = on_message
mqtt_client.connect("broker.hivemq.com", 1883, 60)
mqtt_client.subscribe("IoT/NguyenDucHuy_B23DCAT128/data")
mqtt_client.loop_forever()