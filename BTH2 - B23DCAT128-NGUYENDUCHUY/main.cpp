#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(4, DHT22);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  client.setServer(mqtt_server, 1883);
  dht.begin();
  pinMode(34, INPUT);
}

void loop() {
  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("NguyenDucHuy_B23DCAT128_ESP32")) {
        break;
      } else {
        delay(2000);
      }
    }
  }
  client.loop();

  float t = dht.readTemperature();
  float h = dht.readHumidity();
  int l = analogRead(34);

  if (isnan(t) || isnan(h)) {
    delay(2000);
    return;
  }

  StaticJsonDocument<200> doc;
  doc["temperature"] = t;
  doc["humidity"] = h;
  doc["light"] = l;
  doc["student_id"] = "B23DCAT128";

  String jsonString;
  serializeJson(doc, jsonString);

  client.publish("IoT/NguyenDucHuy_B23DCAT128/data", jsonString.c_str());

  delay(5000);
}