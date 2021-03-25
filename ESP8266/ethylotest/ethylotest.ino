#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>

#include <WebSocketsClient.h>
WebSocketsClient webSocket;

int lastValue = 0;
int readValue = 0;
long lastTime = 0;

void setup() {
  WiFi.mode(WIFI_STA);

  Serial.begin(115200);
  WiFiManager wifiManager;
  wifiManager.autoConnect("ETHYLOTEST");

  webSocket.begin("bartender.local", 12345, "");
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  webSocket.loop();
  if(millis()-lastTime>100){
    readValue = analogRead(A0)/2;
    lastTime = millis();
    if(readValue != lastValue){
      Serial.println(readValue);
      lastValue = readValue;
      webSocket.sendTXT("update|ethylotest|" + String(lastValue));
    }
  }
}

#define USE_SERIAL Serial

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {

  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("déconnecté");
      break;
    case WStype_CONNECTED: {
      Serial.println("connecté");
      webSocket.sendTXT("setupAs|ethylotest");
    }
      break;
    case WStype_TEXT:
      USE_SERIAL.printf("[WSc] get text: %s\n", payload);
      break;
    }
}
